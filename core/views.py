from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


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