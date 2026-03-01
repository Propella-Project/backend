from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('login/', views.login_admin, name='login-admin'),
    path('', views.api_docs, name='api-docs'),
]
