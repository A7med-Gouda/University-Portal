from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .models import College, Department
from .serializers import CollegeSerializer, DepartmentSerializer
from Damnhour.shortcuts import IsAuth, has_permission, get_object_or_404
from rest_framework.request import HttpRequest

class CollegeView(APIView):
    def get(self, request: HttpRequest, pk=None):
        if pk:
            college = get_object_or_404(College, id=pk)
            serializer = CollegeSerializer(college)
            return Response(serializer.data, status=status.HTTP_200_OK)

        colleges = College.objects.all()
        serializer = CollegeSerializer(colleges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest):
        if not IsAuth(request):
            return Response({"error": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        if not has_permission('academics.add_college', request):
            raise PermissionDenied("You do not have permission to add colleges.")

        serializer = CollegeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: HttpRequest, pk=None):
        if not IsAuth(request):
            return Response({"error": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        if not has_permission('academics.change_college', request):
            raise PermissionDenied("You do not have permission to update colleges.")

        college = get_object_or_404(College, id=pk)
        serializer = CollegeSerializer(college, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentView(APIView):
    def get(self, request: HttpRequest, pk=None):
        if pk:
            department = get_object_or_404(Department, id=pk)
            serializer = DepartmentSerializer(department)
            return Response(serializer.data, status=status.HTTP_200_OK)

        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest):
        if not IsAuth(request):
            return Response({"error": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        if not has_permission('academics.add_department', request):
            raise PermissionDenied("You do not have permission to add departments.")

        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: HttpRequest, pk=None):
        if not IsAuth(request):
            return Response({"error": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        if not has_permission('academics.change_department', request):
            raise PermissionDenied("You do not have permission to update departments.")

        department = get_object_or_404(Department, id=pk)
        serializer = DepartmentSerializer(department, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)