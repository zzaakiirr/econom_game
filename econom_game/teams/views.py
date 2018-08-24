from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse

from rest_framework import generics

from .models import Team, Card

from .serializers import TeamSerializer

from stations.views_helpers import get_received_data
from . import views_helpers


class ListTeamsView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


@csrf_exempt
def create_team(request):
    received_data = get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    new_team = views_helpers.create_new_team(received_data)
    if not new_team._state.db:
        return JsonResponse({
            "status": False, "error": "Команда не была добавлена в базу данных"
        })

    return JsonResponse({"status": True})


@user_passes_test(lambda u: u.is_superuser)
def create_card(request):
    id = request.GET['id']
    cvv = request.GET['cvv']
    money_amount = request.GET['money_amount']

    new_card = Card.objects.create(id=id, cvv=cvv, money_amount=money_amount)

    if new_card._state.db:
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})
