from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import (
    MobilizationRecord,
    Qualification
)


class QualificationInline(admin.TabularInline):

    model = Qualification

    extra = 1


@admin.register(MobilizationRecord)
class MobilizationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'mobile',
        'gender',
        'caste',
        'state',
        'created_by',
        'date',
    )

    search_fields = (
        'name',
        'mobile',
        'father_name',
    )

    list_filter = (
        'gender',
        'caste',
        'state',
        'date',
    )

    ordering = ('-date',)

    readonly_fields = (
        'date',
        'added_by_name',
        'created_by',
    )

    inlines = [QualificationInline]

    fieldsets = (

        ('Basic Information', {
            'fields': (
                'name',
                'father_name',
                'dob',
                'gender',
                'caste',
            )
        }),

        ('Contact Details', {
            'fields': (
                'mobile',
                'ward_no',
                'pin',
                'state',
            )
        }),

        ('System Fields', {
            'fields': (
                'date',
                'created_by',
                'added_by_name',
            )
        }),
    )


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'record',
        'sl_no',
        'exam_name',
        'board',
        'year_of_passing',
        'grade',
    )

    search_fields = (
        'exam_name',
        'board',
    )

    ordering = ('record', 'sl_no')