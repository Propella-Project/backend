from rest_framework import serializers
from django.db import transaction
from .models import User, ExamProfile, Referral
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

class CreateUserSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField(required=False, allow_blank=True, max_length=12, write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'referral_code']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_referral_code(self, value):
        if value:
            value = value.strip().upper()
            
            if not User.objects.filter(referral_code=value).exists():
                raise serializers.ValidationError("Invalid referral code.")
        return value
    
    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)
        user = User.objects.create_user(**validated_data)
        if referral_code:
            referral_code = referral_code.strip().upper()
            referrer = User.objects.get(referral_code=referral_code)
            
            if referrer.id == user.id:
                raise serializers.ValidationError("You cannot use your own referral code.")
            
            user.referred_by = referrer
            user.save(update_fields=['referred_by'])
            
            ref = Referral.objects.create(referrer=referrer, referred=user, status='pending')
            ref.save()
        return user
    
class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_email_verified']
        

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    
class CreateExamProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamProfile
        fields = ['id', 'user', 'exam_date', 'daily_hours', 'personality',
                #   'learning_format',
                  'voice_pref']
        
class EditExamProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamProfile
        fields = ['id', 'user', 'exam_date', 'daily_hours', 'personality', 'learning_format', 'voice_pref']
        
class UserExamProfileSerializer(serializers.ModelSerializer):
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
        
# class CreateReferralSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Referral
#         fields = ['id', 'referrer', 'referred']