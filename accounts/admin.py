from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):

    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_staff',
        'is_active',
        'created_at',
    )

    search_fields = (
        'email',
        'first_name',
        'last_name',
    )

    list_filter = (
        'role',
        'is_staff',
        'is_active',
        'created_at',
    )

    ordering = ('-created_at',)

    readonly_fields = ('created_at',)

    fieldsets = (
        ('Authentication', {
            'fields': ('email', 'password')
        }),

        ('Personal Info', {
            'fields': ('first_name', 'last_name')
        }),

        ('Role Management', {
            'fields': ('role',)
        }),

        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),

        ('Important Dates', {
            'fields': ('created_at',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'role',
                'password1',
                'password2',
                'is_staff',
                'is_active',
            ),
        }),
    )