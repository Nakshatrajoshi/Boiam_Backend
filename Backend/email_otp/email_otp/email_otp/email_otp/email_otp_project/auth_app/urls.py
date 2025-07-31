from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import GoogleLoginView



urlpatterns = [
    path('api/signup/', views.signup_view),
    path('api/login/', views.login_view),
    path('api/verify_signup/', views.verify_signup),
    path('api/verify_login/', views.verify_login),
    path('api/google-login/', GoogleLoginView.as_view(), name='google_login') 
  
]


