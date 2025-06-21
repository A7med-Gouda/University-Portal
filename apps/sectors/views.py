from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from Damnhour.shortcuts import IsAuth, has_permission, get_object_or_404
from . import models as sectors_models
from . import serializers as sectors_serializers
from Damnhour.pagination import StandardResultsSetPagination


class SectorListView(APIView):
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['sector_type', 'head']
    search_fields = ['name_ar', 'name_en', 'description_ar', 'description_en']

    def get_queryset(self):
        return sectors_models.Sector.objects.all().select_related('head__user').order_by('-created_at')

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = sectors_serializers.SectorSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = sectors_serializers.SectorSerializer(queryset, many=True)
        return Response(serializer.data)

    def paginate_queryset(self, queryset):
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, self.request, view=self)
        return page

    def get_paginated_response(self, data):
        paginator = self.pagination_class()
        return paginator.get_paginated_response(data)
    def post(self, request):
        if not IsAuth(request):
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_403_FORBIDDEN)

        if not has_permission('sectors.add_sector', request):
            return Response({"detail": "You do not have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        # Prevent duplicate sector names
        existing = sectors_models.Sector.objects.filter(
            name_ar=request.data.get('name_ar'),
            name_en=request.data.get('name_en')
        ).exists()

        if existing:
            return Response({"detail": "Sector with these names already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = sectors_serializers.SectorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({
            "detail": "Validation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SectorDetailView(APIView):

    def get_object(self, pk):
        return get_object_or_404(sectors_models.Sector, pk=pk)

    def get(self, request, pk):
        sector = self.get_object(pk)
        serializer = sectors_serializers.SectorSerializer(sector)
        return Response(serializer.data)

    def patch(self, request, pk):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"},
                            status=status.HTTP_403_FORBIDDEN)

        if not has_permission('sectors.change_sector', request):
            return Response({"detail": "Permission denied"},
                            status=status.HTTP_403_FORBIDDEN)

        sector = self.get_object(pk)
        serializer = sectors_serializers.SectorSerializer(
            sector, data=request.data, partial=True
        )

        if serializer.is_valid():
            # # Validate sector head relationship
            # head = serializer.validated_data.get('head')
            # if head and head.sector != sector:
            #     return Response({
            #         "detail": "Head must belong to this sector"
            #     }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data)

        return Response({
            "detail": "Validation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     if not IsAuth(request):
    #         return Response({"detail": "Authentication required"},
    #                         status=status.HTTP_403_FORBIDDEN)
    #
    #     if not has_permission('sectors.delete_sector', request):
    #         return Response({"detail": "Permission denied"},
    #                         status=status.HTTP_403_FORBIDDEN)
    #
    #     sector = self.get_object(pk)
    #     sector.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)