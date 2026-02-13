from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        role = request.POST.get('role', '').strip()
        
        # Validation
        if not username or not password or not role:
            messages.error(request, "All fields are required.")
            return render(request, 'accounts/register.html')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' is already taken. Please choose another.")
            return render(request, 'accounts/register.html')
        
        # Create user and profile
        try:
            user = User.objects.create_user(username=username, password=password)
            Profile.objects.create(user=user, role=role)
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('accounts:login')
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return render(request, 'accounts/register.html')
    
    return render(request, 'accounts/register.html')
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, 'accounts/login.html')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('core:dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:login') 