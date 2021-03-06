import re
import time
from collections import defaultdict
from contextlib import contextmanager
from urllib.parse import urlencode

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.db import transaction
from django.db.models import Q, Prefetch
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.http import is_safe_url
from django.utils.text import slugify
from rest_framework.request import Request
from elasticsearch.exceptions import NotFoundError
from natsort import natsorted

from capapi import serializers
from capapi.documents import CaseDocument
from capapi.authentication import SessionAuthentication
from capapi.renderers import HTMLRenderer
from capdb.models import Reporter, VolumeMetadata, CaseMetadata
from capweb import helpers
from cite.helpers import geolocate
from config.logging import logger


def safe_redirect(request):
    """ Redirect to request.GET['next'] if it exists and is safe, or else to '/' """
    next = request.POST.get('next') or request.GET.get('next') or '/'
    return HttpResponseRedirect(next if is_safe_url(next, allowed_hosts={request.get_host()}) else '/')

@contextmanager
def locked_session(request, using='default'):
    """
        Reload the user session for exclusive access.
        This is based on django.contrib.sessions.backends.db.SessionStore.load(), and assumes that we are using the
        db session store.
    """
    with transaction.atomic(using=using):
        session = request.session
        try:
            s = session.model.objects.select_for_update().get(session_key=session.session_key, expire_date__gt=timezone.now())
            temp_session = session.decode(s.session_data)
        except (session.model.DoesNotExist, SuspiciousOperation) as e:
            temp_session = {}
        try:
            yield temp_session
        finally:
            request.session.update(temp_session)
            request.session.save()


### views ###

def home(request):
    """ Base page -- list all of our jurisdictions and reporters. """

    # get reporters sorted by jurisdiction
    reporters = Reporter.objects.filter(is_nominative=False).exclude(start_year=None).prefetch_related('jurisdictions').order_by('short_name')
    reporters_by_jurisdiction = defaultdict(list)
    for reporter in reporters:
        for jurisdiction in reporter.jurisdictions.all():
            reporters_by_jurisdiction[jurisdiction].append(reporter)

    # prepare (jurisdiction, reporters) list
    jurisdictions = sorted(reporters_by_jurisdiction.items(), key=lambda item: item[0].name_long)

    return render(request, 'cite/home.html', {
        "jurisdictions": jurisdictions,
    })

def robots(request):
    """
        Disallow all URLs with no_index=True and robots_txt_until >= now.
    """
    return render(request, "cite/robots.txt", {
        'cases': CaseMetadata.objects.filter(robots_txt_until__gte=timezone.now()),
    }, content_type="text/plain")

def series(request, series_slug):
    """ /<series_slug>/ -- list all volumes for each series with that slug (typically only one). """
    # redirect if series slug is in the wrong format

    if slugify(series_slug) != series_slug:
        return HttpResponseRedirect(helpers.reverse('series', args=[slugify(series_slug)], host='cite'))
    reporters = list(Reporter.objects
        .filter(short_name_slug=series_slug)
        .exclude(start_year=None)
        .prefetch_related(Prefetch('volumes', queryset=VolumeMetadata.objects.exclude(volume_number=None).exclude(volume_number='').exclude(duplicate=True).exclude(out_of_scope=True)))
        .order_by('full_name'))
    if not reporters:
        raise Http404
    reporters = [(reporter, natsorted(reporter.volumes.all(), key=lambda volume: volume.volume_number)) for reporter in reporters]
    return render(request, 'cite/series.html', {
        "reporters": reporters,
    })

def volume(request, series_slug, volume_number_slug):
    """ /<series_slug>/<volume_number>/ -- list all cases for given volumes (typically only one). """

    # redirect if series slug or volume number slug is in the wrong format

    if slugify(series_slug) != series_slug or slugify(volume_number_slug) != volume_number_slug:
        return HttpResponseRedirect(helpers.reverse('volume', args=[slugify(series_slug), slugify(volume_number_slug)], host='cite'))

    cases_query = CaseDocument.search()\
        .filter("term", volume__volume_number_slug=volume_number_slug)\
        .filter("term", reporter__short_name_slug__raw=series_slug)\
        .sort('first_page')\
        .extra(size=10000)
    cases_query.aggs.bucket('vols', 'terms', field='volume.barcode')
    cases = cases_query.execute()

    if len(cases) == 0:
        raise Http404

    volume_filters = None
    for vol in cases.aggs.vols.buckets:
        if volume_filters is None:
            volume_filters = Q(barcode=vol.key)
        else:
            volume_filters = volume_filters | Q(barcode=vol.key)
    vols = VolumeMetadata.objects.select_related('reporter').filter(volume_filters).all()
    if not vols:
        raise Http404

    volumes = [(volume, [ case for case in natsorted(cases, key=lambda case: case.first_page) if case.volume.barcode == volume.barcode]) for volume in vols ]

    return render(request, 'cite/volume.html', {
        "volumes": volumes,
    })


def case_pdf(request, case_id, pdf_name):
    """
        Return the PDF for a case. This wraps citation() so that all rules about quotas and anonymous users can be
        applied before we return the case.
    """
    # check that we are at the canonical URL
    case = get_object_or_404(CaseMetadata.objects.select_related('volume').prefetch_related('citations'), pk=case_id)
    pdf_url = case.get_pdf_url()
    if request.build_absolute_uri() != pdf_url:
        return HttpResponseRedirect(pdf_url)

    return citation(request,None, None, None, case_id, pdf=True, db_case=case)


def citation(request, series_slug, volume_number_slug, page_number, case_id=None, pdf=False, db_case=None):
    """
        /<series_slug>/<volume_number>/<page_number>/                       -- show requested case (or list of cases, or case not found page).
        /<series_slug>/<volume_number>/<page_number>/<case_id>/             -- show requested case, using case_id to find one of multiple cases at this cite
    """

    # redirect if series slug or volume number slug is in the wrong format
    if not pdf and (slugify(series_slug) != series_slug or slugify(volume_number_slug) != volume_number_slug):
        if case_id:
            return HttpResponseRedirect(helpers.reverse('citation',
                                                    args=[slugify(series_slug), slugify(volume_number_slug), page_number, case_id],
                                                    host='cite'))
        else:
            return HttpResponseRedirect(helpers.reverse('citation',
                                                        args=[slugify(series_slug), slugify(volume_number_slug), page_number],
                                                        host='cite'))

    ### try to look up citation

    if case_id:
        try:
            cases = [ CaseDocument.get(id=case_id) ]
        except NotFoundError:
            raise Http404
    else:
        full_cite = "%s %s %s" % (volume_number_slug, series_slug.replace('-', ' ').title(), page_number)
        normalized_cite = re.sub(r'[^0-9a-z]', '', full_cite.lower())
        cases = CaseDocument.search().filter("term", citations__normalized_cite=normalized_cite).execute()

        ### handle non-unique citation (zero or multiple)
        if not cases or len(cases) != 1:
            reporter = Reporter.objects.filter(short_name_slug=slugify(series_slug)).first()
            series = reporter.short_name if reporter else series_slug

            return render(request, 'cite/citation_failed.html', {
                "cases": cases,
                "full_cite": full_cite,
                "series_slug": series_slug,
                "series": series,
                "volume_number_slug": volume_number_slug,
                "page_number": page_number,
            })

    ### handle case where we found a unique case with that citation
    case = cases[0]

    # handle whitelisted case or logged-in user
    if case.jurisdiction.whitelisted or request.user.is_authenticated:
        serializer = serializers.CaseDocumentSerializerWithCasebody

    # handle logged-out user with cookies set up already
    elif 'case_allowance_remaining' in request.session and request.COOKIES.get('not_a_bot', 'no') == 'yes':
        with locked_session(request) as session:
            cases_remaining = session['case_allowance_remaining']

            # handle daily quota reset
            if session['case_allowance_last_updated'] < time.time() - 60*60*24:
                cases_remaining = settings.API_CASE_DAILY_ALLOWANCE
                session['case_allowance_last_updated'] = time.time()

            # if quota remaining, serialize without checking credentials
            if cases_remaining > 0:
                session['case_allowance_remaining'] = cases_remaining - 1
                serializer = serializers.NoLoginCaseDocumentSerializer

            # if quota used up, use regular serializer that checks credentials
            else:
                serializer = serializers.CaseDocumentSerializerWithCasebody

    # handle google crawler
    elif helpers.is_google_bot(request):
        serializer = serializers.NoLoginCaseDocumentSerializer

    # if non-whitelisted case, not logged in, and no cookies set up, redirect to ?set_cookie=1
    else:
        request.session['case_allowance_remaining'] = settings.API_CASE_DAILY_ALLOWANCE
        request.session['case_allowance_last_updated'] = time.time()
        return HttpResponseRedirect('%s?%s' % (helpers.reverse('set_cookie', host='cite'), urlencode({'next': request.get_full_path()})))

    # render case using API serializer
    api_request = Request(request, authenticators=[SessionAuthentication()])
    api_request.accepted_renderer = HTMLRenderer()
    serialized = serializer(case, context={'request': api_request})
    serialized_data = serialized.data
    data = serialized_data['casebody']['data']
    case_name_with_markup = serialized_data['name']

    # handle pdf output --
    # wait until here to do this so serializer() can apply case quotas
    db_case = db_case or CaseMetadata.objects.select_related('volume').prefetch_related('citations').get(pk=case.id)
    can_render_pdf = db_case.volume.pdf_file and not db_case.no_index_redacted and settings.CASE_PDF_FEATURE
    if pdf:
        if serialized_data['casebody']['status'] != 'ok':
            return HttpResponseRedirect(db_case.get_full_frontend_url())
        if not can_render_pdf:
            raise Http404
        return HttpResponse(db_case.get_pdf(), content_type="application/pdf")

    # HTML output
    context = {'request': api_request, 'meta_tags': [], 'can_render_pdf': can_render_pdf, 'db_case': db_case}

    if not case.jurisdiction.whitelisted:
        # blacklisted cases shouldn't show cached version in google search results
        context['meta_tags'].append({"name": "googlebot", "content": "noarchive"})

    # This should probably change
    if hasattr(case, 'no_index'):
        if case.no_index:
            context['meta_tags'].append({"name": "robots", "content": "noindex"})
    else:
        if db_case.no_index:
            context['meta_tags'].append({"name": "robots", "content": "noindex"})

    # insert redactions and elisions

    if db_case.no_index_redacted:
        redaction_count = 0
        for redaction, val in db_case.no_index_redacted.items():
            # redact from case body
            data = re.sub(redaction, "<span class='redacted-text' data-redaction-id='%s'>%s</span>" %
                          (redaction_count, val), data)
            redaction_count += 1

            # redact from name
            case_name_with_markup = re.sub(redaction, "[ %s ]" % val, case_name_with_markup)
            serialized_data['name_abbreviation'] = re.sub(redaction, "[ %s ]" % val, serialized_data['name_abbreviation'])
        # Also save as name for indexing
        serialized_data['name'] = case_name_with_markup


    elision_span = "<span class='elision-help-text' style='display: none'>hide</span><span class='elided-text' data-elision-reason='%s' role='button' tabindex='0' data-hidden-text='%s' data-elision-id='%s'>...</span>"
    if db_case.no_index_elided:
        elision_count = 0
        for elision, val in db_case.no_index_elided.items():

            # elide from case body
            data = re.sub(elision, elision_span % (val, elision, elision_count), data)

            elision_count += 1

            # elide from name with html markup
            case_name_with_markup = re.sub(elision, elision_span % (val, elision, elision_count), case_name_with_markup)

            # add elisions without html markup to case name and name_abbreviation for indexing
            serialized_data['name'] = re.sub(elision, "...", serialized_data['name'])
            serialized_data['name_abbreviation'] = re.sub(elision, "...", serialized_data['name_abbreviation'])

    serialized_data['name_with_html_markup'] = case_name_with_markup

    # Add a custom footer message if redactions or elisions exist but no text is provided
    if not db_case.custom_footer_message and (db_case.no_index_redacted or db_case.no_index_elided):
        db_case.custom_footer_message = ''
        if db_case.no_index_redacted:
            db_case.custom_footer_message += "Some text has been redacted by request of participating parties. \n"
        if db_case.no_index_elided:
            db_case.custom_footer_message += "Some text has been elided by request of participating parties. \n"

    if db_case.custom_footer_message:
        custom_footer_message = re.sub(r'\n', '<br/>', db_case.custom_footer_message)
        data += "<hr/><footer class='custom-case-footer'>%s</footer>" % custom_footer_message

    serialized_data['casebody']['data'] = data

    if settings.GEOLOCATION_FEATURE and request.META.get('HTTP_X_FORWARDED_FOR'):
        # Trust x-forwarded-for in this case because we don't mind being lied to, and would rather show accurate
        # results for users using honest proxies.
        try:
            location = geolocate(request.META['HTTP_X_FORWARDED_FOR'].split(',')[-1])
            location_str = location.country.name
            if location.subdivisions:
                location_str = "%s, %s" % (location.subdivisions.most_specific.name, location_str)
            logger.info("Someone from %s read a case from %s." % (location_str, case.court.name))
        except Exception as e:
            logger.warning("Unable to geolocate %s: %s" % (request.user.ip_address, e))

    rendered = HTMLRenderer().render(serialized_data, renderer_context=context)
    return HttpResponse(rendered)


def set_cookie(request):
    """
        /set_cookie/          -- try to use javascript to set a 'not_a_bot=1' cookie
        /set_cookie/?no_js=1  -- ask user to click a button to set a 'not_a_bot=1' cookie
    """
    # user is actually a google bot
    if helpers.is_google_bot(request):
        return safe_redirect(request)

    # user already had a not_a_bot cookie and just needed a session cookie,
    # which was set when they were forwarded here -- they're ready to go:
    elif 'case_allowance_remaining' in request.session and request.COOKIES.get('not_a_bot', 'no') == 'yes':
        return safe_redirect(request)

    # user has successfully POSTed to get their not_a_bot cookie:
    elif request.method == 'POST' and request.POST.get('not_a_bot') == 'yes':
        response = safe_redirect(request)
        response.set_cookie('not_a_bot', 'yes', max_age=60 * 60 * 24 * 365 * 100)
        return response

    # user failed the JS check, so has to click the button by hand:
    elif 'no_js' in request.GET:
        return render(request, 'cite/set_cookie.html', {
            'next': request.GET.get('next', '/'),
        })

    # try to use JS to click button for user:
    else:
        return render(request, 'cite/check_js.html', {
            'next': request.GET.get('next', '/'),
        })
