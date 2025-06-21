from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('staff/', views.StaffProfileView.as_view(), name='staff_profile'),
    path('staff/<int:pk>/', views.StaffProfileView.as_view(), name='staff_profile_detail'),
    path('staff/user/<int:user_pk>/', views.StaffProfileView.as_view(), name='staff_profile_by_user'),

    # Student Endpoints
    path('students/', views.StudentView.as_view(), name='student_list'),
    path('students/<int:pk>/', views.StudentView.as_view(), name='student_detail'),
    path('students/user/<int:user_pk>/', views.StudentView.as_view(), name='student_by_user'),
]