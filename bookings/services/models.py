"""
Models for service categories and individual services.
"""
from django.db import models


class ServiceCategory(models.Model):
    """Category of services (e.g. Haircut & Styling, Facial & Skincare)."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Bootstrap icon class or emoji')
    order = models.PositiveIntegerField(default=0, help_text='Display order on homepage')

    class Meta:
        verbose_name_plural = 'Service categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Service(models.Model):
    """Individual service offered by the salon (e.g. Classic Haircut, Deep Tissue Massage)."""
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='services'
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(
        default=60,
        help_text='Approximate duration in minutes'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Optional price display'
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['category', 'order', 'name']
        unique_together = [['category', 'slug']]

    def __str__(self):
        return f'{self.name} ({self.category.name})'
