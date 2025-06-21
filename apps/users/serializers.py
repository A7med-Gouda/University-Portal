from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.timezone import now
from .models import Staff, Student, CustomUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        super().get_validators(user)
        token = super().get_token(user)
        
        # Update the user's last login time
        user.last_login = now()
        user.save(update_fields=['last_login'])
        token['user_type'] = user.user_type

        if Staff.objects.filter(user=user).exists():
            token['user_type'] = 'Staff'
            staff_profile = Staff.objects.get(user=user)
            
            # Include related sectors in token
            sectors = staff_profile.related_sectors.all().values_list('name', flat=True)
            token['related_sectors'] = list(sectors)

        elif Student.objects.filter(user=user).exists():
            token['user_type'] = 'Student'
        else:
            token['user_type'] = 'CustomUser'

        # Add updatePassword flag to the token payload
        if (user.name_ar == user.password) or (user.name_en == user.password):
            token['updatePassword'] = 1
        else:
            token['updatePassword'] = 0

        # Add name flag to the token payload
        if user.name_ar and user.name_en:
            token['updateName'] = 0
        else:
            token['updateName'] = 1

        return token

class CustomeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ShortCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name_ar', 'name_en', 'email']

class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        exclude = ['basic_salary', 'disbursement_id', 'appointment_type', 'payment_status', 'primary_appointment_group']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'