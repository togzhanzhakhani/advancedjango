from rest_framework import serializers
from .models import Resume, Specialization
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ResumeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  
    specialization = serializers.StringRelatedField()  
    class Meta:
        model = Resume
        fields = ['user', 'specialization', 'file']

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name']
