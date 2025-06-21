# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Service
from .serializers import ServiceSerializer
from Damnhour.shortcuts import get_object_or_404, IsAuth, has_permission
from Damnhour.pagination import StandardResultsSetPagination



class ServiceListView(APIView):
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sectors']

    def get_queryset(self):
        queryset = Service.objects.all()
        search_query = self.request.query_params.get('search', None)

        if search_query:
            queryset = queryset.filter(
                Q(name_ar__icontains=search_query) |
                Q(name_en__icontains=search_query) |
                Q(description_ar__icontains=search_query) |
                Q(description_en__icontains=search_query)
            )
        return queryset.order_by('name_ar')

    def get(self, request):
        queryset = self.get_queryset()

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ServiceSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission('services.add_service', request):
            raise PermissionDenied("You don't have permission to create services")

        serializer = ServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ServiceDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Service, pk=pk)

    def get(self, request, pk):
        service = self.get_object(pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def patch(self, request, pk):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission('services.change_service', request):
            raise PermissionDenied("You don't have permission to edit services")

        service = self.get_object(pk)
        serializer = ServiceSerializer(service, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission('services.delete_service', request):
            raise PermissionDenied("You don't have permission to delete services")

        service = self.get_object(pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)