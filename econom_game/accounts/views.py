from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

from .views_helpers import get_user_allowed_urls


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": True})

    return JsonResponse({"success": False})


def logout_user(request):
    logout(request)
    return JsonResponse({'success': True})


def is_logged_in(request):
    if request.user.is_authenticated():
        return JsonResponse({'is_logged_in': True})
    return JsonResponse({'is_logged_in': False})


def get_menu(request):
    user_allowed_urls = get_user_allowed_urls(request)
    return JsonResponse({"user_allowed_urls": user_allowed_urls})
