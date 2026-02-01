"""
Views for services (optional: service list/detail).
"""
from django.shortcuts import render, get_object_or_404
from .models import ServiceCategory, Service


def category_list_view(request):
    """List all service categories and their services."""
    categories = ServiceCategory.objects.prefetch_related('services').order_by('order', 'name')
    return render(request, 'services/category_list.html', {
        'categories': categories,
        'page_title': 'Our Services',
    })


def service_detail_view(request, category_slug, service_slug):
    """Detail view for a single service."""
    service = get_object_or_404(
        Service,
        category__slug=category_slug,
        slug=service_slug,
        is_active=True
    )
    return render(request, 'services/service_detail.html', {
        'service': service,
        'page_title': service.name,
    })
