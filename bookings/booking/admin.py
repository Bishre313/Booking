"""
Admin for appointments: manage, edit, approve, or cancel.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'guest_name',
        'guest_phone',
        'service',
        'date',
        'time',
        'status_badge',
        'created_at',
    ]
    list_filter = ['status', 'date', 'service']
    search_fields = ['guest_name', 'guest_phone', 'guest_message']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('guest_name', 'guest_phone', 'guest_message', 'service', 'date', 'time', 'status')
        }),
        ('Admin', {
            'fields': ('admin_notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'date'
    ordering = ['-date', '-time']

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {'pending': 'warning', 'approved': 'success', 'rejected': 'danger'}
        c = colors.get(obj.status, 'secondary')
        return format_html(
            '<span style="background-color: var(--bs-{})" class="badge bg-{}">{}</span>',
            c, c, obj.get_status_display()
        )
