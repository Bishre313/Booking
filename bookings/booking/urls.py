"""
URL configuration for the booking app.
"""
from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.BookingView.as_view(), name='book'),
    path('confirmation/', views.confirmation_view, name='confirmation'),
    path('api/available-slots/', views.available_slots, name='available_slots'),
]
