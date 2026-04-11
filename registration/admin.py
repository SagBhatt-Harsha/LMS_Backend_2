from django.contrib import admin
from .models import Registration

# Register your models here.

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):

    list_display = (
        'registration_id',
        'name',
        'mobile',
        'domain',
        'slot',
        'center',
        'registered_date',
    )

    search_fields = ('registration_id', 'name', 'mobile',)

    list_filter = ('domain', 'slot', 'center', 'registered_date',)

    ordering = ('-registered_date',)

    readonly_fields = ('registration_id', 'registered_date', 'registered_by',)