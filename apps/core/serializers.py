from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from . import models as core_models
from Damnhour.shortcuts import IsAuth

# Serializers

class VisionMissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.VisionMission
        fields = '__all__'

class QuickAccessServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.QuickAccessService
        fields = '__all__'

class UniversityInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.UniversityInfo
        fields = '__all__'

class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Statistics
        fields = '__all__'

class StartYourFutureSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.StartYourFuture
        fields = '__all__'