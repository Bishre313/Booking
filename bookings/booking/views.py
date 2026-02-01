"""
Views for appointment booking and confirmation.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils import timezone
from datetime import date, time, timedelta, datetime
from .forms import AppointmentForm
from .models import Appointment
from services.models import Service


class BookingView(FormView):
    """Display booking form and handle submission (no login required)."""
    template_name = 'booking/booking_form.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('booking:confirmation')

    def form_valid(self, form):
        """Save appointment and store pk in session for confirmation page."""
        appointment = form.save()
        self.request.session['last_booking_id'] = appointment.pk
        return redirect(self.get_success_url())

    def get_success_url(self):
        """Redirect to confirmation with optional id in URL."""
        bid = self.request.session.get('last_booking_id')
        if bid:
            return reverse_lazy('booking:confirmation') + f'?id={bid}'
        return reverse_lazy('booking:confirmation')

    def get_initial(self):
        """Pre-fill service when coming from ?service=<id>."""
        initial = super().get_initial()
        service_id = self.request.GET.get('service')
        if service_id:
            try:
                from services.models import Service
                Service.objects.get(pk=int(service_id), is_active=True)
                initial['service'] = int(service_id)
            except (ValueError, Service.DoesNotExist):
                pass
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Book an Appointment'
        context['available_slots_url'] = reverse_lazy('booking:available_slots')
        return context


def confirmation_view(request):
    """Show booking confirmation after submission."""
    booking_id = request.GET.get('id') or request.session.get('last_booking_id')
    appointment = None
    if booking_id:
        try:
            appointment = Appointment.objects.select_related('service', 'service__category').get(
                pk=int(booking_id)
            )
        except (Appointment.DoesNotExist, ValueError):
            pass
    return render(request, 'booking/confirmation.html', {
        'appointment': appointment,
        'page_title': 'Booking Confirmation',
    })


def available_slots(request):
    """
    Return JSON list of available time slots for a given date.
    Used to display available times and prevent double booking on the frontend.
    """
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'slots': [], 'error': 'Missing date'}, status=400)
    try:
        chosen_date = date.fromisoformat(date_str)
    except ValueError:
        return JsonResponse({'slots': [], 'error': 'Invalid date'}, status=400)
    if chosen_date < date.today():
        return JsonResponse({'slots': []})
    # Salon hours (example: 9:00 - 18:00, 30-min slots)
    start = time(9, 0)
    end = time(18, 0)
    slot_minutes = 30
    slots = []
    t = datetime.combine(chosen_date, start)
    end_dt = datetime.combine(chosen_date, end)
    now = timezone.now()
    while t < end_dt:
        slot_time = t.time()
        # Skip past times for today
        if chosen_date == date.today() and t <= now:
            t += timedelta(minutes=slot_minutes)
            continue
        # Check if slot is taken (pending or approved)
        taken = Appointment.objects.filter(
            date=chosen_date,
            time=slot_time
        ).filter(status__in=['pending', 'approved']).exists()
        if not taken:
            slots.append(slot_time.strftime('%H:%M'))
        t += timedelta(minutes=slot_minutes)
    return JsonResponse({'date': date_str, 'slots': slots})
