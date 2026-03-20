from django.shortcuts import render
from rest_framework import viewsets
from .models import User, ExamProfile, EmailVerification, Referral, Plan, Subscription
from core.models import Roadmap, RoadmapDay, RoadmapTask
from .serializers import CreateUserSerializer, EditUserSerializer, CreateExamProfileSerializer, EditExamProfileSerializer, AllUsersSerializer, AllExamProfilesSerializer, ChangePasswordSerializer, UserExamProfileSerializer, UserSerializer, PlanSerializer, SubscriptionSerializer, ReferralSerializer,LoginSerializer
from .utils import send_verification_code
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from config.settings.prod import FLUTTERWAVE_SECRET_KEY, DEFAULT_FROM_EMAIL
import requests
import uuid


from rest_framework.permissions import IsAuthenticated, AllowAny
from  rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
# =========================== check user's verification status============
def is_active_subscription(user):
    sub = Subscription.objects.filter(user=user, is_active=True).first()
    
    if not sub:
        return False
    
    if sub.end_date < timezone.now():
        sub.is_active = False
        sub.save()
        return False
    return True

# ========================================================
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):

    serializer = LoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = serializer.validated_data["user"]

    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "success": True,
            "message": "Login successful",
            "data": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username
                    "onboarded": user.onboarded,
                    "is_email_verified": user.is_email_verified,
                }
            }
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user and send verification email.
    
    The user will be created but marked as inactive until they verify their email.
    """
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Generate and send verification code
        verification = EmailVerification.generate_for_user(user)
        email_sent = send_verification_code(user, verification)
        
        
        if email_sent:
            return Response({
                'message': 'User registered successfully. Please check your email for verification code.',
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        else:
            # User created but email failed
            return Response({
                'message': 'User registered but verification email could not be sent. Please contact support.',
                'email': user.email
            }, status=status.HTTP_201_CREATED)
    
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

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if not user.check_password(old_password):
            return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get("email")
    
    try:
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)
        
        reset_link = f"https://propella.ng/reset-password/{uid}/{token}/"
        
        # send email logic
        subject = "Password Reset Request"

        message = f"""
                            Hello {user.username},

                            You requested to reset your password.

                            Click the link below to reset your password:

                            {reset_link}

                            If you did not request this, please ignore this email.

                            Thanks,
                            Your Team
                    """

        send_mail(
                subject,
                message,
                DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        
        return Response({
                "message": "Password reset link sent",
                "reset_link": reset_link
            })
        
    except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        
@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request, uid, token):
    
    password = request.data.get("password")

    try:
        user_id = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(id=user_id)

        if default_token_generator.check_token(user, token):
            user.password = make_password(password)
            user.save()

            return Response({"message": "Password reset successful"})

        return Response({"error": "Invalid token"}, status=400)

    except:
        return Response({"error": "Invalid request"}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_exam_profile(request):
    if not request.user.is_email_verified:
        return Response({
            'error': 'You must verify your email before creating an exam profile.'
        }, status=status.HTTP_400_BAD_REQUEST)
        
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

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    """
    Verify user email with the verification code sent to their email.
    
    Endpoint expects:
    - email: the user's email address
    - code: the 6-digit verification code
    """
    email = request.data.get('email')
    code = request.data.get('code')
    
    if not email or not code:
        return Response({
            'error': 'Both email and code are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    try:
        verification = EmailVerification.objects.get(user=user)
    except EmailVerification.DoesNotExist:
        return Response({
            'error': 'No verification code found for this email. Please register again.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Check if code is valid
    if not verification.is_valid():
        if verification.attempts >= verification.max_attempts:
            return Response({
                'error': 'Too many failed attempts. Please request a new verification code.'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        else:
            return Response({
                'error': 'Verification code has expired. Please request a new code.'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if code matches
    if verification.code != code:
        verification.increment_attempts()
        remaining = verification.max_attempts - verification.attempts
        return Response({
            'error': f'Invalid code. {remaining} attempts remaining.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Code is valid - mark user as verified
    
    user.is_email_verified = True
    user.is_active = True  # Activate the user
    user.save()
    
    try:
        referral = Referral.objects.get(referred=user, status='pending')
        if referral:
            referral.status = 'completed'
            referral.points = 10  # Award points for successful referral
            referral.save()
    except:
        pass
    
    verification.verified = True
    verification.save()
    
    return Response({
        'message': 'Email verified successfully. Your account is now active.'
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification_code(request):
    """
    Resend verification code to user's email.
    
    Endpoint expects:
    - email: the user's email address
    """
    email = request.data.get('email')
    
    if not email:
        return Response({
            'error': 'Email is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Don't reveal if user exists or not
        return Response({
            'message': 'If an account with this email exists, a verification code has been sent.'
        }, status=status.HTTP_200_OK)
    
    if user.is_email_verified:
        return Response({
            'message': 'This email is already verified.'
        }, status=status.HTTP_200_OK)
    
    # Generate new verification code
    verification = EmailVerification.generate_for_user(user)
    email_sent = send_verification_code(user, verification)
    
    if email_sent:
        return Response({
            'message': 'Verification code has been sent to your email.'
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': 'Failed to send verification code. Please try again later.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_exam_profile(request):
    try:
        exam_profile = ExamProfile.objects.get(user=request.user)
        serializer = UserExamProfileSerializer(exam_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ExamProfile.DoesNotExist:
        return Response({'error': 'Exam profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_referrals(request):
    referrals = Referral.objects.filter(referrer=request.user)
    serializer = ReferralSerializer(referrals, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def plan_list(request):
    plans = Plan.objects.all()
    serializer = PlanSerializer(plans, many=True)
    return Response(serializer.data, status=200)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_subscription(request):
    subscription = Subscription.objects.filter(
        user=request.user,
        is_active=True
    )
    if not subscription:
        return Response({"message":"No active subscription"}, status=400)
    
    serializer = SubscriptionSerializer(subscription)
    return Response(serializer.data, status=200)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def subscribe(request):
    
    existing = Subscription.objects.filter(
        user=request.user,
        is_active=True
    ).first()
    
    if existing:
        return Response({"error":"You already have an active subscription"})

    plan_id = request.data.get("plan_id")

    try:
        plan = Plan.objects.get(id=plan_id)

        tx_ref = str(uuid.uuid4())

        url = "https://api.flutterwave.com/v3/payments"

        headers = {
            "Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "tx_ref": tx_ref,
            "amount": str(plan.price),
            "currency": "NGN",
            "redirect_url": "https://dashboard.propella.ng/verify",
            "customer": {
                "email": request.user.email,
                "name": request.user.username
            },
            "customizations": {
                "title": f"{plan.name} Subscription"
            }
        }

        response = requests.post(url, headers=headers, json=payload)

        return Response(response.json())

    except Plan.DoesNotExist:
        return Response({"error": "Plan not found"}, status=404)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_subscription(request):

    transaction_id = request.data.get("transaction_id")
    plan_id = "3"

    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"

    headers = {
        "Authorization": f"Bearer {FLUTTERWAVE_SECRET_KEY}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if data["status"] == "success":

        plan = Plan.objects.get(id=plan_id)

        start = timezone.now()
        end = start + timedelta(days=plan.duration_days)

        subscription = Subscription.objects.create(
            user=request.user,
            plan=plan,
            start_date=start,
            end_date=end
        )
        
        user = request.user
        user.onboarded = True
        user.save()
        
        return Response({
            "message": "Subscription activated",
            "subscription_id": subscription.id
        })

    return Response({"error": "Payment verification failed"}, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def subscription_status(request):
    subscription = Subscription.objects.filter(
        user=request.user,
        is_active=True
    ).first()

    if not subscription:
        return Response({"active": False})

    if subscription.end_date < timezone.now():
        subscription.is_active = False
        subscription.save()
        return Response({"active": False})
    
    days_remaining = (subscription.end_date - timezone.now()).days

    return Response({
        "active": True,
        "plan": subscription.plan.name,
        "expires_at": subscription.end_date,
        "days_remaining": days_remaining,
        "subscription": SubscriptionSerializer(subscription).data
    })