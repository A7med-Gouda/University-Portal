# urls.py
from django.urls import path
from .views import ServiceListView, ServiceDetailView

urlpatterns = [
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services/<uuid:pk>/', ServiceDetailView.as_view(), name='service-detail'),
]