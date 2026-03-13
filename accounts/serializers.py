from rest_framework import serializers
from django.db import transaction
from .models import User, ExamProfile, Referral, Subscription, Plan
from core.models import Roadmap, RoadmapDay, RoadmapTask
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        if not user.is_active:
            raise serializers.ValidationError("Account disabled")

        data["user"] = user
        return data
    
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

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8)
    token = serializers.CharField()
    uid = serializers.CharField()

    
    
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
        
class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
        
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['user', 'start_date']

        