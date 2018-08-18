from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

from .views_helpers import get_user_allowed_urls


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": True})

    return JsonResponse({"success": False})


def is_logged_in(request):
    username = request.user.username
    if not username:
        username = None
    return JsonResponse({'username': username})


@login_required
def get_menu(request):
    user_allowed_urls = get_user_allowed_urls(request)
    return JsonResponse(
        {"success": True, "user_allowed_urls": user_allowed_urls}
    )
