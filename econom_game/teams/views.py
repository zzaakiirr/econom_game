from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

from rest_framework import generics

from .models import Team, Card
from .serializers import TeamSerializer


class ListTeamsView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


@user_passes_test(lambda u: u.is_superuser)
def create_team(request):
    id = request.GET['id']
    name = request.GET['name']
    login = request.GET['login']
    card_id = request.GET['card_id']
    team_card = Card.objects.get(id=card_id)

    new_team = Team.objects.create(
        id=id, name=name, login=login, card=team_card)

    if new_team._state.db:
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})


@user_passes_test(lambda u: u.is_superuser)
def create_card(request):
    id = request.GET['id']
    cvv = request.GET['cvv']
    money_amount = request.GET['money_amount']

    new_card = Card.objects.create(id=id, cvv=cvv, money_amount=money_amount)

    if new_card._state.db:
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})
