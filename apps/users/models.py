from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('student', 'Student'),
        ('employee', 'Employee'),
        ('staff', 'Staff'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, null=True, blank=True)

    email = models.EmailField(unique=True, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)

    # Additional fields
    name_ar = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    national_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    college = models.ForeignKey('academics.College', on_delete=models.SET_NULL, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Set email as the username field.
    USERNAME_FIELD = 'national_id'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        # If both name fields are empty, fallback to national_id.
        return f"{self.name_en or self.name_ar or self.national_id} - {self.get_user_type_display()}"
    
    class Meta:
        permissions = [
            ('admin_organization', 'user is admin organization'),
            ('is_staff', 'user is staff'),
            ('is_student', 'user is student'),
            ('is_employee', 'user is employee'),
        ]


class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff_profile', null=True, blank=True)
    disbursement_id = models.CharField(max_length=50)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    appointment_type = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    department = models.ForeignKey('academics.Department', on_delete=models.SET_NULL, null=True, blank=True)
    grade = models.CharField(max_length=50, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=50, blank=True, null=True)
    primary_appointment_group = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    x = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    tasks = models.TextField(blank=True, null=True)
    researches = models.TextField(blank=True, null=True)
    cv = models.FileField(upload_to='users/staff/cv/', blank=True, null=True)
    key_user = models.BooleanField(default=False)
    google_schoolar = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    related_sectors = models.ManyToManyField('sectors.Sector', blank=True, related_name='staff_related_sectors')

    def save(self, *args, **kwargs):

        self.user.user_type = 'staff'
        super().save(*args, **kwargs)
    


    def __str__(self):
        if self.user:
            return f"Staff: {self.user.name_en or self.user.name_ar or self.user.national_id}"
        return "Staff Profile"

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    student_number = models.CharField(max_length=20, unique=True)
    # for student profile
    job_title = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    x = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    tasks = models.TextField(blank=True, null=True)
    researches = models.TextField(blank=True, null=True)
    cv = models.FileField(upload_to='users/staff/cv/', blank=True, null=True)
    key_user = models.BooleanField(default=False)
    google_schoolar = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        if self.user:
            return f"Student: {self.user.national_id} - {self.student_number}"
        return f"Student: {self.student_number}"
    
    def save(self, *args, **kwargs):

        self.user.user_type = 'student'
        super().save(*args, **kwargs)

