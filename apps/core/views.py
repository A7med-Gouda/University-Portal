from rest_framework.views import APIView
from . import models as core_models
from rest_framework import status
from rest_framework.response import Response
from Damnhour.shortcuts import IsAuth
from . import serializers as core_serializer
from . import models as core_models
from Damnhour.shortcuts import has_permission, get_object_or_404

class VisionMissionView(APIView):
    def get(self, request):
        queryset = core_models.VisionMission.objects.all()
        serializer = core_serializer.VisionMissionSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not IsAuth(request):
            return Response({"detail": "User Not authenticated"}, status=403)
        
        if not has_permission('core.add_visionmission', request):
            return Response({"detail": "User Not authorized"}, status=403)
        
        all_messions = core_models.VisionMission.objects.all()

        if len(all_messions) >= 2:
            return Response({"detail": "You can only add 2 Vision and Mission"}, status=403)

        serializer = core_serializer.VisionMissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        if not IsAuth(request):
            return Response({"detail": "User Not authenticated"}, status=403)

        if not has_permission('core.change_visionmission', request):
            return Response({"detail": "User Not authorized"}, status=403)
        
        instance = get_object_or_404(core_models.VisionMission, pk=pk)

        serializer = core_serializer.VisionMissionSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     if not IsAuth(request):
    #         return Response({"detail": "User Not authenticated"}, status=403)

    #     if not has_permission('core.delete_visionmission', request):
    #         return Response({"detail": "User Not authorized"}, status=403)

    #     try:
    #         instance = core_models.VisionMission.objects.get(pk=pk)
    #         instance.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     except core_models.VisionMission.DoesNotExist:
    #         return Response({"detail": "Not found"}, status=404)

class QuickAccessServiceView(APIView):
    def get(self, request):
        queryset = core_models.QuickAccessService.objects.all()
        serializer = core_serializer.QuickAccessServiceSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not IsAuth(request):
            return Response({"detail": "User Not authenticated"}, status=403)
        
        if not has_permission('core.add_quickaccessservice', request):
            return Response({"detail": "User Not authorized"}, status=403)

        serializer = core_serializer.QuickAccessServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        if not IsAuth(request):
            return Response({"detail": "User Not authenticated"}, status=403)
        
        if not has_permission('core.change_quickaccessservice', request):
            return Response({"detail": "User Not authorized"}, status=403)
        
        instance = get_object_or_404(core_models.QuickAccessService, pk=pk)

        serializer = core_serializer.QuickAccessServiceSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not IsAuth(request):
            return Response({"detail": "User Not authenticated"}, status=403)
        
        if not has_permission('core.delete_quickaccessservice', request):
            return Response({"detail": "User Not authorized"}, status=403)

        instance = get_object_or_404(core_models.QuickAccessService, pk=pk)

        instance.delete()

        return Response({"detail" : "Quick access deleted succesffully."}, status=status.HTTP_204_NO_CONTENT)

class UniversityInfoView(APIView):
    def get(self, request):
        queryset = core_models.UniversityInfo.objects.all()
        serializer = core_serializer.UniversityInfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not IsAuth(request):
            return Response({"detail": "User Not authenticated"}, status=403)
        
        if not has_permission('core.add_universityinfo', request):
            return Response({"detail": "User Not authorized"}, status=403)

        all_university_info = core_models.UniversityInfo.objects.all()

        if len(all_university_info) >= 1:
            return Response({"detail": "You can only add 1 University Info"}, status=403)

        serializer = core_serializer.UniversityInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        if not IsAuth(request):
            return Response({"detail": "User Not authenticated"}, status=403)
        
        if not has_permission('core.change_universityinfo', request):
            return Response({"detail": "User Not authorized"}, status=403)
        
        instance = get_object_or_404(core_models.UniversityInfo, pk=pk)

        serializer = core_serializer.UniversityInfoSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     if not IsAuth(request):
    #         return Response({"detail": "User Not authenticated"}, status=403)
        
    #     if not has_permission('core.delete_universityinfo', request):
    #         return Response({"detail": "User Not authorized"}, status=403)

    #     try:
    #         instance = core_models.UniversityInfo.objects.get(pk=pk)
    #         instance.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     except core_models.UniversityInfo.DoesNotExist:
    #         return Response({"detail": "Not found"}, status=404)

class StatisticsView(APIView):
    def get(self, request):
        queryset = core_models.Statistics.objects.all()
        serializer = core_serializer.StatisticsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not IsAuth(request):
            return Response({"detail": "User Not authenticated"}, status=403)
        
        if not has_permission('core.add_statistics', request):
            return Response({"detail": "User Not authorized"}, status=403)

        all_statistics = core_models.Statistics.objects.all()

        if len(all_statistics) >= 1:
            return Response({"detail": "You can only add 1 Statistics"}, status=403)

        serializer = core_serializer.StatisticsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        if not IsAuth(request):
            return Response({"detail": "User Not authenticated"}, status=403)
        
        if not has_permission('core.change_statistics', request):
            return Response({"detail": "User Not authorized"}, status=403)
        
        instance = get_object_or_404(core_models.Statistics, pk=pk)

        serializer = core_serializer.StatisticsSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     if not IsAuth(request):
    #         return Response({"detail": "User Not authenticated"}, status=403)
        
    #     if not has_permission('core.delete_statistics', request):
    #         return Response({"detail": "User Not authorized"}, status=403)

    #     try:
    #         instance = core_models.Statistics.objects.get(pk=pk)
    #         instance.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     except core_models.Statistics.DoesNotExist:
    #         return Response({"detail": "Not found"}, status=404)

class StartYourFutureView(APIView):
    def get(self, request):
        queryset = core_models.StartYourFuture.objects.all()
        serializer = core_serializer.StartYourFutureSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not IsAuth(request):
            return Response({"detail": "User Not authenticated"}, status=403)
        
        if not has_permission('core.add_startyourfuture', request):
            return Response({"detail": "User Not authorized"}, status=403)

        all_start_your_future = core_models.StartYourFuture.objects.all()

        if len(all_start_your_future) >= 1:
            return Response({"detail": "You can only add 1 Start Your Future"}, status=403)

        serializer = core_serializer.StartYourFutureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        if not IsAuth(request):
            return Response({"detail": "User Not authenticated"}, status=403)
        
        if not has_permission('core.change_startyourfuture', request):
            return Response({"detail": "User Not authorized"}, status=403)
        
        instance = get_object_or_404(core_models.StartYourFuture, pk=pk)

        serializer = core_serializer.StartYourFutureSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)