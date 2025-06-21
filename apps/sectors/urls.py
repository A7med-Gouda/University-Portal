from django.urls import path
from .views import SectorListView, SectorDetailView

urlpatterns = [
    path('sectors/', SectorListView.as_view(), name='sector-list'),
    path('sectors/<uuid:pk>/', SectorDetailView.as_view(), name='sector-detail'),
]