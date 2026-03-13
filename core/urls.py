from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('login/', views.login_admin, name='login-admin'),
    path('', views.api_docs, name='api-docs'),
    path('logout/', views.logout_admin, name='logout-admin'),
    
    # =================================== Roadmap ======================================
    path('create-roadmap/', views.create_roadmap, name="create-roadmap"),
    path('roadmap/', views.get_roadmap, name="get-roadmap")
]
