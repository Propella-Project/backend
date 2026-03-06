from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('resend-code/', views.resend_verification_code, name='resend_code'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', views.change_password, name='change_password'),
    path('all-users/', views.all_users, name='all_users'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('create-exam-profile/', views.create_exam_profile, name='create_exam_profile'),
    path('edit-exam-profile/<int:profile_id>/', views.edit_exam_profile, name='edit_exam_profile'),
    
    # =================================================== Subscription =======================
    path('subscriptions/plans/', views.plan_list, name="plan_list"),
    path('subscriptions/subscribe/', views.subscribe_view, name="subscribe_view"),
    
    # ===================================  password reset ======================================
    path('forgot-password/', views.forgot_password, name="forgot-password"),
    path('reset-password/<uid>/<token>/', views.reset_password, name="reset-password")

]
