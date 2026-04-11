from django.contrib import admin
from .models import CounsellingLog

# Register your models here.

@admin.register(CounsellingLog)
class CounsellingAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'mobilization_record',
        'status',
        'slot',
        'domain',
        'counselled_by_name',
        'date',
    )

    search_fields = ('mobilization_record__name', 'mobilization_record__mobile', 'domain',)

    list_filter = ('status', 'slot', 'domain', 'date',)

    ordering = ('-date',)

    readonly_fields = ('date', 'counselled_by', 'counselled_by_name',)

    fieldsets = (
        ('Linked Mobilization', {'fields': ('mobilization_record',)}),
        ('Counselling Details', {'fields': ('status', 'slot', 'domain', 'notes',)}),
        ('System Fields', {'fields': ('date', 'counselled_by', 'counselled_by_name',)}),
    )