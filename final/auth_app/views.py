from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

from django.http import JsonResponse
from django.utils.http import unquote

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'auth_app/login.html', {"error": "Invalid username or password."})

    return render(request, 'auth_app/login.html')

# def signup_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']

#         if password != confirm_password:
#             return render(request, 'auth_app/signup.html', {"error": "Passwords do not match."})
        
#         if User.objects.filter(username=username).exists():
#             return render(request, 'auth_app/signup.html', {"error": "Username already exists."})
        
#         user = User.objects.create_user(username=username, email=email, password=password)
#         user.save()
#         login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#         return redirect('/')
    
#     return render(request, 'auth_app/signup.html')

@ensure_csrf_cookie
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'auth_app/signup.html', {"error": "Passwords do not match."})

        if User.objects.filter(username=username).exists():
            return render(request, 'auth_app/signup.html', {"error": "Username already exists."})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False  # Аккаунт не активен до подтверждения
        user.save()

        # Сохраняем email в сессии
        request.session["pending_email"] = email

        # Генерируем токен
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(request)

        mail_subject = "Activate your TechForge account"
        html_message = render_to_string(
            "auth_app/email_confirmation.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": uid,
                "token": token,
            },
        )

        text_message = strip_tags(html_message)

        email_message = EmailMultiAlternatives(mail_subject, text_message, "your_email@gmail.com", [email])
        email_message.attach_alternative(html_message, "text/html")
        email_message.send()

        return render(request, "auth_app/email_sent.html", {"email": email})  # Новый шаблон
    return render(request, 'auth_app/signup.html')

def logout_view(request):
    logout(request)
    return redirect('/')


def activate(request, uidb64, token):
    try:
        uid = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("✅ Ваш аккаунт активирован! Теперь можете <a href='/auth/login'>войти</a>.")
    else:
        return HttpResponse("❌ Ссылка активации недействительна или устарела.")
    

def check_activation_status(request, email):
    try:
        email = unquote(email)  # Декодируем URL-encoded email
        user = User.objects.get(email=email)
        return JsonResponse({"activated": user.is_active})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)