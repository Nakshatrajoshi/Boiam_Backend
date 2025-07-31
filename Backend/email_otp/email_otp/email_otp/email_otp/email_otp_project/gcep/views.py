import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import ContactForm

# Create your views here.

def contact_form(request):
    """Display the contact form"""
    return render(request, 'gcep/contact_form.html')

@csrf_exempt
@require_http_methods(["POST"])
def submit_contact_form(request):
    """Handle contact form submission"""
    try:
        data = json.loads(request.body)
        
        # Extract form data
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        institute = data.get('institute', '').strip()
        designation = data.get('designation', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        job_title = data.get('job_title', '').strip()
        message = data.get('message', '').strip()
        
        # Validate required fields
        if not first_name or not last_name or not institute or not email or not message:
            return JsonResponse({
                'success': False,
                'message': 'Please fill in all required fields.'
            }, status=400)
        
        # Create and save the contact form submission
        contact_submission = ContactForm.objects.create(
            first_name=first_name,
            last_name=last_name,
            institute=institute,
            designation=designation if designation else None,
            email=email,
            phone=phone if phone else None,
            job_title=job_title if job_title else None,
            message=message
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Thank you! Your message has been submitted successfully.',
            'submission_id': contact_submission.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while processing your request.'
        }, status=500)
