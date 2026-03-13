from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def login_admin(request):
    if request.user.is_authenticated and request.user.role == "admin":
        return redirect("core:api-docs")
    if request.user.is_authenticated and request.user.role != "admin":
        messages.error(request, "You do not have permission to access this page.")
        logout(request)
        return redirect("core:login-admin")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request, email=email, password=password)
        if user is not None and user.role == "admin":
            login(request, user)
            messages.success(request, "Login Successfull!!!")
            return redirect("core:api-docs")
        else:
            messages.error(request, "Invalid credentials or not an admin user.")
            return redirect("core:login-admin")
        
    return render(request, 'login.html')

@login_required(login_url='core:login-admin')
def api_docs(request):
    if request.user.role != "admin":
        messages.error(request, "You do not have permission to access this page.")
        return redirect("core:login-admin")
    
    return render(request, 'api_documentation.html')

def logout_admin(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("core:login-admin")


# ============================================================================================================

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny


from .models import (
    Subject,
    UserSubject,
    Streak,
    Topic,
    StudyMaterial,
    Roadmap,
    RoadmapDay,
    RoadmapTask,
    Assignment,     
    Question,
    Choice,
    AbilityScore,
)

from .serializers import (
    SubjectSerializer,
    UserSubjectSerializer,
    StreakSerializer,
    TopicSerializer,
    StudyMaterialSerializer,
    RoadmapSerializer,
    RoadmapDaySerializer,
    RoadmapTaskSerializer,
    AssignmentSerializer,
    QuestionSerializer,
    ChoiceSerializer,
    AbilityScoreSerializer,
)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_all_subjects(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user_subject(request):
    if not request.user.is_email_verified:
        return Response({
            'error': 'You must verify your email before adding subjects.'
        }, status=400)
    
    serializer = UserSubjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'User subject created successfully',
            'user_subject': serializer.data
        }, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_subjects(request):
    if not request.user.is_email_verified:
        return Response({
            'error': 'You must verify your email before adding subjects.'
        }, status=400)
    
    user = User.objects.get(id=request.user.id)
    user_subjects = UserSubject.objects.filter(user=user)
    
    serializer = UserSubjectSerializer(user_subjects, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_subject(request, user_subject_id):
    if not request.user.is_email_verified:
        return Response({
            'error': 'You must verify your email before adding subjects.'
        }, status=400)
    
    try:
        user_subject = UserSubject.objects.get(id=user_subject_id, user=request.user)
    except UserSubject.DoesNotExist:
        return Response({
            'error': 'User subject not found.'
        }, status=404)
    
    serializer = UserSubjectSerializer(user_subject, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'User subject updated successfully',
            'user_subject': serializer.data
        }, status=200)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_user_subject(request, user_subject_id):
    if not request.user.is_email_verified:
        return Response({
            'error': 'You must verify your email before adding subjects.'
        }, status=400)
    
    try:
        user_subject = UserSubject.objects.get(id=user_subject_id, user=request.user)
    except UserSubject.DoesNotExist:
        return Response({
            'error': 'User subject not found.'
        }, status=404)
    
    user_subject.delete()
    return Response({
        'message': 'User subject deleted successfully'
    }, status=200)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_all_streaks(request):
    streaks = Streak.objects.all()
    serializer = StreakSerializer(streaks, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_all_topics(request):
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_all_study_materials(request):
    study_materials = StudyMaterial.objects.all()
    serializer = StudyMaterialSerializer(study_materials, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_all_assignments(request):
    assignments = Assignment.objects.all()
    serializer = AssignmentSerializer(assignments, many=True)
    return Response(serializer.data, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_all_questions(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data, status=200)
