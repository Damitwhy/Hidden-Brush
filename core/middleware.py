from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from .models import User

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')):
            if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
                return render(request, '403.html', status=403)
        response = self.get_response(request)
        return response

