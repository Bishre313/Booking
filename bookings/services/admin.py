"""
Admin for service categories and services.
"""
from django.contrib import admin
from .models import ServiceCategory, Service


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0
    fields = ['name', 'slug', 'duration_minutes', 'price', 'is_active', 'order']


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceInline]
    ordering = ['order', 'name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'duration_minutes', 'price', 'is_active', 'order']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'category__name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']
    ordering = ['category', 'order', 'name']
