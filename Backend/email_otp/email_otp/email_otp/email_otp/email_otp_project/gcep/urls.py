from django.urls import path

from . import views

app_name = 'gcep'

urlpatterns = [
    path('contact/', views.contact_form, name='contact_form'),
    path('contact/submit/', views.submit_contact_form, name='submit_contact_form'),
] 