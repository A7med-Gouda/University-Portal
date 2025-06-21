from django.urls import path
from . import views

urlpatterns = [
    path('vision-mission/', views.VisionMissionView.as_view(), name='vision-mission'),
    path('quick-access-services/', views.QuickAccessServiceView.as_view(), name='quick-access-services'),
    path('university-info/', views.UniversityInfoView.as_view(), name='university-info'),
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
    path('start-your-future/', views.StartYourFutureView.as_view(), name='start-your-future'),
    path('start-your-future/<int:pk>/', views.StartYourFutureView.as_view(), name='start-your-future-detail'),
    path('statistics/<int:pk>/', views.StatisticsView.as_view(), name='statistics-detail'),
    path('university-info/<int:pk>/', views.UniversityInfoView.as_view(), name='university-info-detail'),
    path('quick-access-services/<int:pk>/', views.QuickAccessServiceView.as_view(), name='quick-access-services-detail'),
    path('vision-mission/<int:pk>/', views.VisionMissionView.as_view(), name='vision-mission-detail'),
]