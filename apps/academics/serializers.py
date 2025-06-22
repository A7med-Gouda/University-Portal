from rest_framework import serializers
from .models import College, Department, Program
from apps.users.serializers import ShortCustomUserSerializer

class CollegeSerializer(serializers.ModelSerializer):
    chairman_details = ShortCustomUserSerializer(source='chairman', read_only=True)

    class Meta:
        model = College
        fields = ['id', 'name', 'chairman', 'address', 'chairman_details']

class DepartmentSerializer(serializers.ModelSerializer):
    head_details = ShortCustomUserSerializer(source='head', read_only=True)
    college_name = serializers.CharField(source='college.name', read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'head', 'college', 'head_details', 'college_name']

class ProgramSerializer(serializers.ModelSerializer):
    head_details = ShortCustomUserSerializer(source='head', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    college_name = serializers.CharField(source='department.college.name', read_only=True)

    class Meta:
        model = Program
        fields = ['id', 'name', 'head', 'department', 'head_details', 'department_name', 'college_name']