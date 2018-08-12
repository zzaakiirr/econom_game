from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

import json


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
