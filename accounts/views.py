from django.shortcuts import render
from rest_framework import viewsets
from .models import User, ExamProfile
from .serializers import CreateUserSerializer, EditUserSerializer, CreateExamProfileSerializer, EditExamProfileSerializer, AllUsersSerializer, AllExamProfilesSerializer

from rest_framework.permissions import IsAuthenticated, AllowAny
from  rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def edit_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = EditUserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_exam_profile(request):
    serializer = CreateExamProfileSerializer(data=request.data)
    if serializer.is_valid():
        exam_profile = serializer.save()
        return Response({'message': 'Exam profile created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def edit_exam_profile(request, profile_id):
    try:
        exam_profile = ExamProfile.objects.get(id=profile_id, user=request.user)
    except ExamProfile.DoesNotExist:
        return Response({'error': 'Exam profile not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = EditExamProfileSerializer(exam_profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Exam profile updated successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_users(request):
    if request.user.role != 'admin':
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    users = User.objects.all()
    return Response(AllUsersSerializer(users, many=True).data, status=status.HTTP_200_OK)