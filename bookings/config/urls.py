"""
URL configuration for Salon & Spa Booking project.
"""
from django.contrib import admin
from django.urls import path, include

# Secure admin: customize branding (create superuser with: python manage.py createsuperuser)
admin.site.site_header = 'Serenity Salon & Spa Admin'
admin.site.site_title = 'Salon & Spa Admin'
admin.site.index_title = 'Appointments & Services'
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('booking/', include('booking.urls')),
    path('services/', include('services.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
