from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError
from .models import College, Department, Program
from .serializers import CollegeSerializer, DepartmentSerializer, ProgramSerializer
from Damnhour.shortcuts import IsAuth, has_permission, get_object_or_404
from rest_framework.request import HttpRequest

class CollegeView(APIView):
    def get(self, request: HttpRequest, pk=None):
        if pk:
            college = get_object_or_404(College, id=pk)
            serializer = CollegeSerializer(college)
            return Response(serializer.data, status=status.HTTP_200_OK)

        colleges = College.objects.select_related('chairman').all()
        serializer = CollegeSerializer(colleges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest):
        if not IsAuth(request):
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission('academics.add_college', request):
            raise PermissionDenied("You do not have permission to add colleges.")

        serializer = CollegeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return Response({"error": "Database integrity error."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: HttpRequest, pk=None):
        if not IsAuth(request):
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission('academics.change_college', request):
            raise PermissionDenied("You do not have permission to update colleges.")

        college = get_object_or_404(College, id=pk)
        serializer = CollegeSerializer(college, data=request.data, partial=True)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response({"error": "Database integrity error."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest, pk=None):
        if not IsAuth(request):
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission('academics.delete_college', request):
            raise PermissionDenied("You do not have permission to delete colleges.")

        college = get_object_or_404(College, id=pk)
        college.delete()
        return Response({"message": "College deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class DepartmentView(APIView):
    def get(self, request: HttpRequest, pk=None):
        if pk:
            department = get_object_or_404(Department, id=pk)
            serializer = DepartmentSerializer(department)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Filter by college if provided
        college_id = request.query_params.get('college')
        departments = Department.objects.select_related('head', 'college').all()
        
        if college_id:
            departments = departments.filter(college__id=college_id)

        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest):
        if not IsAuth(request):
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission('academics.add_department', request):
            raise PermissionDenied("You do not have permission to add departments.")

        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "Database integrity error."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: HttpRequest, pk=None):
        if not IsAuth(request):
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission('academics.change_department', request):
            raise PermissionDenied("You do not have permission to update departments.")

        department = get_object_or_404(Department, id=pk)
        serializer = DepartmentSerializer(department, data=request.data, partial=True)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response({"error": "Database integrity error."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest, pk=None):
        if not IsAuth(request):
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission('academics.delete_department', request):
            raise PermissionDenied("You do not have permission to delete departments.")

        department = get_object_or_404(Department, id=pk)
        department.delete()
        return Response({"message": "Department deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class ProgramView(APIView):
    def get(self, request: HttpRequest, pk=None):
        if pk:
            program = get_object_or_404(Program, id=pk)
            serializer = ProgramSerializer(program)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Filter by department or college if provided
        department_id = request.query_params.get('department')
        college_id = request.query_params.get('college')
        programs = Program.objects.select_related('head', 'department', 'department__college').all()
        
        if department_id:
            programs = programs.filter(department__id=department_id)
        elif college_id:
            programs = programs.filter(department__college__id=college_id)

        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest):
        if not IsAuth(request):
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission('academics.add_program', request):
            raise PermissionDenied("You do not have permission to add programs.")

        serializer = ProgramSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "Database integrity error."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: HttpRequest, pk=None):
        if not IsAuth(request):
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission('academics.change_program', request):
            raise PermissionDenied("You do not have permission to update programs.")

        program = get_object_or_404(Program, id=pk)
        serializer = ProgramSerializer(program, data=request.data, partial=True)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response({"error": "Database integrity error."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest, pk=None):
        if not IsAuth(request):
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission('academics.delete_program', request):
            raise PermissionDenied("You do not have permission to delete programs.")

        program = get_object_or_404(Program, id=pk)
        program.delete()
        return Response({"message": "Program deleted successfully."}, status=status.HTTP_204_NO_CONTENT)