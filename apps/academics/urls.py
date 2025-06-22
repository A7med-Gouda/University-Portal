from django.urls import path
from .views import CollegeView, DepartmentView

urlpatterns = [
    path('colleges/', CollegeView.as_view(), name='college-list'),
    path('colleges/<uuid:pk>/', CollegeView.as_view(), name='college-detail'),
    path('departments/', DepartmentView.as_view(), name='department-list'),
    path('departments/<uuid:pk>/', DepartmentView.as_view(), name='department-detail'),
]