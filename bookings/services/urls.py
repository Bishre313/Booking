"""
URL configuration for the services app.
"""
from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.category_list_view, name='category_list'),
    path('<slug:category_slug>/<slug:service_slug>/', views.service_detail_view, name='service_detail'),
]
