from django.contrib import admin
from .models import Trainee

# Register your models here.

@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'registration_id', 'domain', 'slot', 'batch', 'registered_date')

    search_fields = ('name', 'registration_id', 'contact')
    list_filter = ('domain', 'slot', 'batch')

    ordering = ('-registered_date',)
    readonly_fields = ('registration_id', 'registered_date')