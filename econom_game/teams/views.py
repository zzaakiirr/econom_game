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

    old_teams_count = Team.objects.count()
    new_team = Team.objects.create(
        id=id, name=name, login=login, card=team_card)
    new_team.save()
    new_teams_count = Team.objects.count()
    if new_teams_count == old_teams_count + 1:
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})


@user_passes_test(lambda u: u.is_superuser)
def create_card(request):
    id = request.GET['id']
    cvv = request.GET['cvv']
    money_amount = request.GET['money_amount']

    old_cards_count = Card.objects.count()
    new_card = Card.objects.create(id=id, cvv=cvv, money_amount=money_amount)
    new_card.save()
    new_cards_count = Card.objects.count()
    if new_cards_count == old_cards_count + 1:
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})
