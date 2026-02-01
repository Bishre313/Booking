"""
Data migration: seed the 7 service categories and sample services.
"""
from django.db import migrations


def seed(apps, schema_editor):
    ServiceCategory = apps.get_model('services', 'ServiceCategory')
    Service = apps.get_model('services', 'Service')

    categories_data = [
        {'name': 'Haircut & Styling', 'slug': 'haircut-styling', 'description': 'Classic cuts, styling, and trims.', 'icon': '✂️', 'order': 1},
        {'name': 'Facial & Skincare', 'slug': 'facial-skincare', 'description': 'Facials, cleanses, and skin treatments.', 'icon': '✨', 'order': 2},
        {'name': 'Massage & Spa', 'slug': 'massage-spa', 'description': 'Relaxing massages and spa therapies.', 'icon': '💆', 'order': 3},
        {'name': 'Manicure & Pedicure', 'slug': 'manicure-pedicure', 'description': 'Nail care and polish.', 'icon': '💅', 'order': 4},
        {'name': 'Hair Coloring', 'slug': 'hair-coloring', 'description': 'Color, highlights, and color correction.', 'icon': '🎨', 'order': 5},
        {'name': 'Bridal / Groom Packages', 'slug': 'bridal-groom-packages', 'description': 'Special day packages for brides and grooms.', 'icon': '💒', 'order': 6},
        {'name': 'Beauty Treatments', 'slug': 'beauty-treatments', 'description': 'Waxing, threading, and other beauty services.', 'icon': '🌸', 'order': 7},
    ]

    for data in categories_data:
        cat, _ = ServiceCategory.objects.get_or_create(slug=data['slug'], defaults=data)
        # Add sample services if none exist
        if not cat.services.exists():
            if data['slug'] == 'haircut-styling':
                Service.objects.bulk_create([
                    Service(category=cat, name='Classic Haircut', slug='classic-haircut', duration_minutes=45, price=45.00, order=1),
                    Service(category=cat, name='Styling & Blow Dry', slug='styling-blow-dry', duration_minutes=60, price=55.00, order=2),
                ])
            elif data['slug'] == 'facial-skincare':
                Service.objects.bulk_create([
                    Service(category=cat, name='Deep Cleansing Facial', slug='deep-cleansing-facial', duration_minutes=60, price=75.00, order=1),
                    Service(category=cat, name='Hydrating Facial', slug='hydrating-facial', duration_minutes=50, price=65.00, order=2),
                ])
            elif data['slug'] == 'massage-spa':
                Service.objects.bulk_create([
                    Service(category=cat, name='Swedish Massage', slug='swedish-massage', duration_minutes=60, price=85.00, order=1),
                    Service(category=cat, name='Aromatherapy Massage', slug='aromatherapy-massage', duration_minutes=75, price=95.00, order=2),
                ])
            elif data['slug'] == 'manicure-pedicure':
                Service.objects.bulk_create([
                    Service(category=cat, name='Classic Manicure', slug='classic-manicure', duration_minutes=45, price=35.00, order=1),
                    Service(category=cat, name='Spa Pedicure', slug='spa-pedicure', duration_minutes=60, price=50.00, order=2),
                ])
            elif data['slug'] == 'hair-coloring':
                Service.objects.bulk_create([
                    Service(category=cat, name='Full Color', slug='full-color', duration_minutes=90, price=95.00, order=1),
                    Service(category=cat, name='Highlights', slug='highlights', duration_minutes=120, price=120.00, order=2),
                ])
            elif data['slug'] == 'bridal-groom-packages':
                Service.objects.bulk_create([
                    Service(category=cat, name='Bridal Package', slug='bridal-package', duration_minutes=180, price=350.00, order=1),
                    Service(category=cat, name='Groom Package', slug='groom-package', duration_minutes=60, price=75.00, order=2),
                ])
            elif data['slug'] == 'beauty-treatments':
                Service.objects.bulk_create([
                    Service(category=cat, name='Eyebrow Wax', slug='eyebrow-wax', duration_minutes=20, price=18.00, order=1),
                    Service(category=cat, name='Full Leg Wax', slug='full-leg-wax', duration_minutes=45, price=45.00, order=2),
                ])


def reverse_seed(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    ServiceCategory = apps.get_model('services', 'ServiceCategory')
    Service.objects.all().delete()
    ServiceCategory.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed, reverse_seed),
    ]
