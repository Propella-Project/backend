from rest_framework import serializers
from .models import User, ExamProfile

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    
class CreateExamProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamProfile
        fields = ['id', 'user', 'exam_date', 'daily_hours', 'personality', 'learning_format', 'voice_pref']
        
class EditExamProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamProfile
        fields = ['id', 'user', 'exam_date', 'daily_hours', 'personality', 'learning_format', 'voice_pref']
        
class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class AllExamProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamProfile
        fields = ['id', 'user', 'exam_date', 'daily_hours', 'personality', 'learning_format', 'voice_pref', 'total_points']