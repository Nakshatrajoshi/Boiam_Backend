# import random

# from django.contrib.auth.models import \
#     User  # ya apna custom User model import karo
# from django.core.mail import send_mail
# from django.shortcuts import redirect, render

# from .models import UserOTP


# def signup_view(request):
#     if request.method == 'POST':
#         email = request.POST['email']

#         # Check karo email already registered na ho
#         if User.objects.filter(email=email).exists():
#             return render(request, 'auth_app/signup.html', {'error': 'Email already registered. Please login instead.'})

#         otp = str(random.randint(100000, 999999))
#         UserOTP.objects.update_or_create(email=email, defaults={'otp': otp})

#         send_mail(
#             'Your Sign Up OTP',
#             f'Your OTP is: {otp}',
#             'user@gmail.com',
#             [email],
#             fail_silently=False,
#         )
#         request.session['email'] = email
#         return redirect('verify_signup')

#     return render(request, 'auth_app/signup.html')


# def login_view(request):
#     if request.method == 'POST':
#         email = request.POST['email']

#         # Check karo user registered hai ya nahi
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return render(request, 'auth_app/login.html', {'error': 'Email not registered. Please sign up first.'})

#         otp = str(random.randint(100000, 999999))
#         UserOTP.objects.update_or_create(email=email, defaults={'otp': otp})

#         send_mail(
#             'Your Login OTP',
#             f'Your OTP is: {otp}',
#             'techbaoiam@gmail.com',
#             [email],
#             fail_silently=False,
#         )
#         request.session['email'] = email
#         return redirect('verify_login')

#     return render(request, 'auth_app/login.html')


# def verify_signup(request):
#     email = request.session.get('email')
#     if request.method == 'POST':
#         entered_otp = request.POST['otp']
#         try:
#             user_otp = UserOTP.objects.get(email=email)
#             if user_otp.otp == entered_otp:
#                 # Yahan pe naya user create karo (simple example: username=email)
#                 User.objects.create_user(username=email, email=email, password=None)
#                 return redirect('success')
#             else:
#                 return render(request, 'auth_app/verify_signup.html', {'error': 'Invalid OTP'})
#         except UserOTP.DoesNotExist:
#             return redirect('signup')
#     return render(request, 'auth_app/verify_signup.html')


# def verify_login(request):
#     email = request.session.get('email')
#     if request.method == 'POST':
#         entered_otp = request.POST['otp']
#         try:
#             user_otp = UserOTP.objects.get(email=email)
#             if user_otp.otp == entered_otp:
#                 # Login successful: tum yahan session set kar sakte ho, ya redirect
#                 return redirect('success')
#             else:
#                 return render(request, 'auth_app/verify_login.html', {'error': 'Invalid OTP'})
#         except UserOTP.DoesNotExist:
#             return redirect('login')
#     return render(request, 'auth_app/verify_login.html')




import json
import random
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from .models import UserOTP

from .models import UserProfile

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get("id_token")
        if not token:
            return Response({"error": "Missing id_token"}, status=400)

        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request())

            email = idinfo["email"]
            name = idinfo.get("name", "")
            picture = idinfo.get("picture", "")

            # ✅ Use get_or_create to prevent duplicate user error
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email,
                    'first_name': name
                }
            )

            # ✅ Create profile if new user
            if created:
                UserProfile.objects.create(user=user, auth_provider='google')

            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "email": user.email,
                    "name": user.first_name,
                    "picture": picture,
                },
                "created": created
            })

        except ValueError:
            return Response({"error": "Invalid ID token"}, status=400)

        
#  OTP Email Sender 
def send_otp_email(email, otp):
    html_content = render_to_string('auth_app/otp_email.html', {'otp': otp})
    email_msg = EmailMessage(
        subject='Your OTP Code',
        body=html_content,
        from_email='techbaoiam@gmail.com',
        to=[email],
    )
    email_msg.content_subtype = "html"
    email_msg.send()

# ✅ Signup Endpoint
@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        print(f"[SIGNUP] Email received: {email}")

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already registered. Please log in.'}, status=400)

        otp = str(random.randint(100000, 999999))
        UserOTP.objects.update_or_create(email=email, defaults={'otp': otp})

        send_otp_email(email, otp)
        return JsonResponse({'message': 'OTP sent successfully to email.'})

    return JsonResponse({'error': 'Invalid method'}, status=405)

# ✅ Login Endpoint
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        print(f"[LOGIN] Email received: {email}")

        if not User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email not registered. Please sign up.'}, status=400)

        otp = str(random.randint(100000, 999999))
        UserOTP.objects.update_or_create(email=email, defaults={'otp': otp})

        send_otp_email(email, otp)
        return JsonResponse({'message': 'OTP sent successfully to email.'})

    return JsonResponse({'error': 'Invalid method'}, status=405)

#  Verify Signup Endpoint
@csrf_exempt
def verify_signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        otp = data.get('otp')
        print(f"[VERIFY SIGNUP] Email: {email} | OTP: {otp}")

        try:
            user_otp = UserOTP.objects.get(email=email)
            
            
            if user_otp.otp == otp:

                   if User.objects.filter(email=email).exists():
                    user = User.objects.get(email=email)
                    try:
                        profile = UserProfile.objects.get(user=user)
                        if profile.auth_provider == 'google':
                            return JsonResponse({'error': 'Email already registered via Google. Please log in with Google.'}, status=400)
                        else:
                            return JsonResponse({'error': 'Email already registered.'}, status=400)
                    except UserProfile.DoesNotExist:
                        return JsonResponse({'error': 'Email already registered.'}, status=400)


                
                   user = User.objects.create_user(username=email, email=email)
                   UserProfile.objects.create(user=user, auth_provider='email')

                   return JsonResponse({'message': 'Signup successful'})

            return JsonResponse({'error': 'Invalid OTP'}, status=400)

        except UserOTP.DoesNotExist:
            return JsonResponse({'error': 'No OTP found for this email'}, status=404)

    return JsonResponse({'error': 'Invalid method'}, status=405)


# ✅ Verify Login Endpoint
@csrf_exempt
def verify_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        otp = data.get('otp')
        print(f"[VERIFY LOGIN] Email: {email} | OTP: {otp}")

        try:
            user_otp = UserOTP.objects.get(email=email)
            if user_otp.otp == otp:
                return JsonResponse({'message': 'Login successful'})
            return JsonResponse({'error': 'Invalid OTP'}, status=400)
        except UserOTP.DoesNotExist:
            return JsonResponse({'error': 'No OTP found for this email'}, status=404)

    return JsonResponse({'error': 'Invalid method'}, status=405)
