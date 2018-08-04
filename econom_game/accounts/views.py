from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

from .forms import LoginForm


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse(
                {"status": "failure"})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
