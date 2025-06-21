from django.db import models
from uuid import uuid4


class College(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    chairman = models.OneToOneField('users.Staff', on_delete=models.SET_NULL, related_name='chaired_college',
                                    null=True, blank=True)
    address = models.TextField()

    def __str__(self):
        return f"College: {self.name}"


class Department(models.Model):  # Contains all departments in the colleges
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    head = models.OneToOneField('users.Staff', on_delete=models.SET_NULL, related_name='head_department',
                                null=True, blank=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return f"Department: {self.name} ({self.college.name})"


class Program(models.Model):  # Contains all Programmes in the colleges
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    head = models.OneToOneField('users.CustomUser', on_delete=models.SET_NULL, related_name='program_coordinator',
                                null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='program')

    def __str__(self):
        return f"Program: {self.name} ({self.department.name}) ({self.department.college.name})"
