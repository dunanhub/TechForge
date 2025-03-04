from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('/')

            return redirect('/')
        else:
            return render(request, 'auth_app/login.html', {"error": "Invalid username or password."})
    return render(request, 'auth_app/login.html')

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            return render(request, 'auth_app/signup.html', {"error": "Passwords do not match."})

        if User.objects.filter(username=username).exists():
            return render(request, 'auth_app/signup.html', {"error": "Username already taken."})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('/login/')
    return render(request, 'auth_app/signup.html')

def logout_view(request):
    logout(request)
    return redirect('/')