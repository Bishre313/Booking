"""
Appointment booking model with status and validation to prevent double booking.
"""
from django.db import models
from django.core.exceptions import ValidationError
from services.models import Service


class Appointment(models.Model):
    """Single appointment (no login required)."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    # Guest info (no user account required)
    guest_name = models.CharField(max_length=150)
    guest_phone = models.CharField(max_length=20)
    guest_message = models.TextField(blank=True)

    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='appointments'
    )
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f'{self.guest_name} – {self.service.name} on {self.date} at {self.time} ({self.status})'

    def clean(self):
        """Prevent double booking: no two approved/pending appointments for same date+time."""
        super().clean()
        if not self.date or not self.time:
            return
        # Exclude self when updating
        qs = Appointment.objects.filter(
            date=self.date,
            time=self.time
        ).exclude(status='rejected')
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError(
                'This time slot is already booked. Please choose another date or time.'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
