from rest_framework import serializers
from .models import College, Department
from apps.users.serializers import ShortCustomUserSerializer

class CollegeSerializer(serializers.ModelSerializer):

    cheirman_ = ShortCustomUserSerializer(read_only=True)

    class Meta:
        model = College
        fields = ['id', 'name', 'chairman', 'address', 'cheirman_']

    def get_cheirman_(self, obj):
        if obj.head:
            return ShortCustomUserSerializer(obj.head).data
        return None

class DepartmentSerializer(serializers.ModelSerializer):

    head_ = ShortCustomUserSerializer(read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'head', 'college', 'head_']

    def get_head_(self, obj):
        if obj.head:
            return ShortCustomUserSerializer(obj.head).data
        return None