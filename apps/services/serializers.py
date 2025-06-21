# serializers.py
from rest_framework import serializers
from .models import Service
from apps.sectors.serializers import SectorSerializer
from ..sectors.models import Sector


class ServiceSerializer(serializers.ModelSerializer):
    sectors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Sector.objects.all(),
        required=False
    )

    class Meta:
        model = Service
        fields = '__all__'
        extra_kwargs = {
            'name_ar': {'required': True},
            'name_en': {'required': True},
            'description_ar': {'required': True},
            'description_en': {'required': True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['sectors'] = SectorSerializer(instance.sectors.all(), many=True).data
        return representation