from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Batch

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'domain', 'slot', 'teacher', 'capacity', 'start_date', 'end_date')

    search_fields = ('name', 'domain')
    list_filter = ('domain', 'slot', 'start_date', 'end_date')

    ordering = ('-start_date',)
    readonly_fields = ('name',)