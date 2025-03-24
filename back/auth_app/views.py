from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests


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


def google_auth_callback(request):
    return JsonResponse({"status": "OK"})


@csrf_exempt
def sign_in(request):
    return render(request, 'sign_in.html')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def auth_receiver(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            token = data.get('credential')

            user_data = id_token.verify_oauth2_token(
                token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
            )

            if not user_data:
                return JsonResponse({'success': False, 'error': 'Invalid token'}, status=400)

            email = user_data.get("email")
            name = user_data.get("name")

            user, created = User.objects.get_or_create(username=email, defaults={'email': email, 'first_name': name})

            login(request, user)

            return JsonResponse({'success': True, 'redirect_url': '/'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def sign_out(request):
    del request.session['user_data']
    return redirect('sign_in')