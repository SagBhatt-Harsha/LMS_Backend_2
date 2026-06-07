from django.contrib import admin
from .models import Trainee

# Register your models here.

@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'registration_id', 'domain', 'slot', 'get_batches', 'registered_date')

    search_fields = ('name', 'registration_id', 'contact')
    list_filter = ('domain', 'slot', 'batches')

    def get_batches(self, obj):
        return ", ".join([b.name for b in obj.batches.all()])
    get_batches.short_description = 'Batches'

    ordering = ('-registered_date',)
    readonly_fields = ('registration_id', 'registered_date')