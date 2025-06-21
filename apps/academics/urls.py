from django.urls import path
from .views import CollegeView, DepartmentView


urlpatterns = [
    path('colleges/', CollegeView.as_view(), name='college-list'),
    path('colleges/<int:pk>/', CollegeView.as_view(), name='college-detail'),
    path('departments/', DepartmentView.as_view(), name='department-list'),
    path('departments/<int:pk>/', DepartmentView.as_view(), name='department-detail'),
]