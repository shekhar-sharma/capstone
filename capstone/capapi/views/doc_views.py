import os
import json
from django.conf import settings
from django.shortcuts import render

from capapi import serializers
from capdb import models


def home(request):
    case = models.CaseMetadata.objects.get(id=settings.API_DOCS_CASE_ID)
    reporter = case.reporter
    reporter_metadata = serializers.ReporterSerializer(reporter, context={'request': request}).data
    case_metadata = serializers.CaseSerializer(case, context={'request': request}).data
    whitelisted_jurisdictions = models.Jurisdiction.objects.filter(whitelisted=True).values('name_long', 'name')

    return render(request, 'home.html', {
        "hide_footer": True,
        "case_metadata": case_metadata,
        "case_id": case_metadata['id'],
        "case_jurisdiction": case_metadata['jurisdiction'],
        "reporter_id": reporter_metadata['id'],
        "reporter_metadata": reporter_metadata,
        "whitelisted_jurisdictions": whitelisted_jurisdictions,
    })


def data(request):
    jurisdictions = models.Jurisdiction.objects.all()
    data_dir = 'capapi/data/'

    with open(os.path.join(data_dir, 'court_count.json'), 'r') as f:
        court_count = json.load(f)

    with open(os.path.join(data_dir, 'reporter_count.json'), 'r') as f:
        reporter_count = json.load(f)

    with open(os.path.join(data_dir, 'case_count.json'), 'r') as f:
        case_count = json.load(f)

    data, jurs = {}, {}

    for jur in jurisdictions:
        jurs[jur.slug] = {
            'whitelisted': jur.whitelisted,
            'name_long': jur.name_long,
            'name': jur.name,

        }
        data[jur.slug] = {
            'slug': jur.slug,
            'name_long': jur.name_long,
            'reporters': reporter_count[jur.slug],
            'courts': court_count[jur.slug],
            'cases': case_count[jur.slug]
        }

    return render(request, 'data-viz.html', {'jurisdictions': jurs, 'data_js': json.dumps(data)})
