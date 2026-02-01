"""
Booking form with validation and error handling.
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import Appointment
from services.models import Service
from datetime import date, time, datetime


class AppointmentForm(forms.ModelForm):
    """Form for guest appointment booking (no login required)."""
    # Optional: make message a Textarea in the form
    guest_message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any special requests or notes...'})
    )

    class Meta:
        model = Appointment
        fields = ['guest_name', 'guest_phone', 'service', 'date', 'time', 'guest_message']
        widgets = {
            'guest_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'guest_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. +1 234 567 8900'
            }),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active services, grouped by category
        self.fields['service'].queryset = Service.objects.filter(
            is_active=True
        ).select_related('category').order_by('category__order', 'category__name', 'order', 'name')

    def clean_date(self):
        """Do not allow past dates."""
        d = self.cleaned_data.get('date')
        if d and d < date.today():
            raise ValidationError('Please choose today or a future date.')
        return d

    def clean(self):
        """Validate time slot and prevent double booking."""
        cleaned = super().clean()
        date_val = cleaned.get('date')
        time_val = cleaned.get('time')
        if not date_val or not time_val:
            return cleaned
        # Past datetime
        if date_val == date.today():
            from datetime import datetime
            now = datetime.now().time()
            if time_val <= now:
                self.add_error('time', 'Please choose a future time for today.')
            return cleaned
        # Check for existing booking (pending/approved) for this slot
        conflict = Appointment.objects.filter(
            date=date_val,
            time=time_val
        ).filter(status__in=['pending', 'approved'])
        if self.instance and self.instance.pk:
            conflict = conflict.exclude(pk=self.instance.pk)
        if conflict.exists():
            self.add_error(
                None,
                'This time slot is already booked. Please choose another date or time.'
            )
        return cleaned
