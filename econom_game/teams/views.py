from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

from rest_framework import generics

from .models import Team, Card
from .serializers import TeamSerializer
import views_helpers


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

    Team.objects.create(
        id=id, name=name, login=login, card=team_card)
    new_team = Team.objects.get(id=id)

    if views_helpers.is_in_database(new_team, Team):
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})


@user_passes_test(lambda u: u.is_superuser)
def create_card(request):
    id = request.GET['id']
    cvv = request.GET['cvv']
    money_amount = request.GET['money_amount']

    Card.objects.create(id=id, cvv=cvv, money_amount=money_amount)
    new_card = Card.objects.get(id=id)

    if views_helpers.is_in_database(new_card, Card):
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})
