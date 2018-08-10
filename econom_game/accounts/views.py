import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, login


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        received_json_data = json.loads(data)
        username = received_json_data[username]
        password = received_json_data[password]
        user = authenticate(username=username, password=password)
        if user is not None:
            if login(request, user):
                return JsonResponse({"status": "success"})

    return JsonResponse({"status": "failure"})
