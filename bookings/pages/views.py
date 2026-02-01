"""
Views for static pages: home and contact.
"""
from django.shortcuts import render
from services.models import ServiceCategory, Service


def home_view(request):
    """Home page with hero section and service cards."""
    categories = ServiceCategory.objects.prefetch_related('services').order_by('order', 'name')
    # Only show categories that have at least one active service
    categories = [c for c in categories if c.services.filter(is_active=True).exists()]
    return render(request, 'pages/home.html', {
        'categories': categories,
        'page_title': 'Home',
    })


def contact_view(request):
    """Contact page with salon details."""
    return render(request, 'pages/contact.html', {
        'page_title': 'Contact Us',
    })
