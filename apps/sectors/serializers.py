# serializers.py
from rest_framework import serializers
from .models import Sector
from apps.users.serializers import StaffProfileSerializer

class SectorSerializer(serializers.ModelSerializer):
    head = StaffProfileSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    structure_url = serializers.SerializerMethodField()

    class Meta:
        model = Sector
        fields = [
            'id',
            'name_ar',
            'name_en',
            'description_ar',
            'description_en',
            'message_ar',
            'message_en',
            'speech_ar',
            'speech_en',
            'sector_type',
            'image_url',
            'structure_url',
            'head',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at')

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

    def get_structure_url(self, obj):
        return obj.organizational_structure.url if obj.organizational_structure else None

    def validate(self, data):
        # Add custom validation logic here
        if data.get('name_ar') and len(data['name_ar']) < 3:
            raise serializers.ValidationError("Arabic name must be at least 3 characters long")
        if data.get('name_en') and len(data['name_en']) < 3:
            raise serializers.ValidationError("English name must be at least 3 characters long")
        return data