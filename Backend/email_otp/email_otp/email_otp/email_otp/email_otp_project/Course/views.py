from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_content(request):
    data = {
        'title': 'Hello from Django!',
        'description': 'This content is served from Django REST API and shown in React frontend.'
    }
    return Response(data)
