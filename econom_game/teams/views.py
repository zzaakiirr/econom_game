from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from rest_framework import generics

from .models import Team

from .serializers import TeamSerializer

from . import views_helpers


class ListTeamsView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


@csrf_exempt
def create_team(request):
    received_data = views_helpers.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    new_team = views_helpers.create_new_team(received_data)
    if not new_team._state.db:
        return JsonResponse({
            "success": False, "error": "Команда не была добавлена в базу данных"
        })

    return JsonResponse({"success": True})
