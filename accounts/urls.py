from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('all-users/', views.all_users, name='all_users'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('create-exam-profile/', views.create_exam_profile, name='create_exam_profile'),
    path('edit-exam-profile/<int:profile_id>/', views.edit_exam_profile, name='edit_exam_profile'),

]
