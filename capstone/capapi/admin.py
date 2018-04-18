from django.utils import timezone
from django.contrib import admin

from . import models

def authenticate_user(modeladmin, request, queryset):
    """
    This method will override old key_expires fields by setting it to timezone.now()
    """
    for user in queryset:
        user.key_expires = timezone.now()
        user.authenticate_user(activation_nonce=user.activation_nonce)
        user.save()


authenticate_user.short_description = "Authenticate selected Users"


class CapUserAdmin(admin.ModelAdmin):
    readonly_fields = ('date_joined', 'api_key')
    list_display = (
        'email',
        'last_name',
        'first_name',
        'is_staff',
        'api_key',
        'case_allowance_remaining',
        'total_case_allowance',
    )

    fields = list_display + ('is_active', 'date_joined', 'activation_nonce', 'is_researcher')
    actions = [authenticate_user]

    def api_key(self, instance):
        return instance.get_api_key()

    api_key.short_description = "API Key"


admin.site.register(models.CapUser, CapUserAdmin)
