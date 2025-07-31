from django.urls import path
from .views import get_content

urlpatterns = [
    path('api/content/', get_content),
]
