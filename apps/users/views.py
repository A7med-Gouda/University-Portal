from rest_framework_simplejwt.views import TokenObtainPairView
from . import serializers
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from . import models as users_models
from Damnhour.shortcuts import IsAuth, has_permission, get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import HttpRequest


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer

class CustomeUserView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, user_pk=None):
        pass

    def post(self, request):
        pass

    def patch(self, request):
        pass

class StaffProfileView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request: HttpRequest, pk=None, user_pk=None):
        if pk:
            staff = users_models.Staff.objects.filter(id=pk).first()
            if staff:
                serializer = serializers.StaffProfileSerializer(staff)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Staff not found"}, status=status.HTTP_404_NOT_FOUND)

        if user_pk:
            staff = users_models.Staff.objects.filter(user__id=user_pk).first()
            if staff:
                serializer = serializers.StaffProfileSerializer(staff)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "Staff not found"}, status=status.HTTP_404_NOT_FOUND)

        staff = users_models.Staff.objects.all()
        serializer = serializers.StaffProfileSerializer(staff, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest):
        
        if not IsAuth(request):
            return Response({"error": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        if not has_permission('users.add_staff', request):
            raise PermissionDenied("You do not have permission to add staff.")
        
        serializer = serializers.StaffProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: HttpRequest):
        
        if not IsAuth(request):
            return Response({"error": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        if not has_permission('users.is_staff', request):
            raise PermissionDenied("You do not have permission to update staff.")
        
        staff = get_object_or_404(users_models.Staff,user__id=request.user.pk)
        serializer = serializers.StaffProfileSerializer(staff, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest, pk=None, user_pk=None):
        if pk:
            student = get_object_or_404(users_models.Student, id=pk)
            serializer = serializers.StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if user_pk:
            student = get_object_or_404(users_models.Student, user__id=user_pk)
            serializer = serializers.StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)

        students = users_models.Student.objects.all()
        serializer = serializers.StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest):
        
        if not IsAuth(request):
            return Response({"error": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        if not has_permission('users.add_student', request):
            raise PermissionDenied("You do not have permission to add students.")

        serializer = serializers.StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request: HttpRequest):

        if not IsAuth(request):
            return Response({"error": "You are not authorized to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        if not has_permission('users.change_student', request):
            raise PermissionDenied('You do not have permission to perform this action')

        student = get_object_or_404(users_models.Student, user__id=request.user.pk)
        serializer = serializers.StudentSerializer(student, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
