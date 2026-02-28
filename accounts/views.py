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

