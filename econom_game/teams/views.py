from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from teams.views_helpers import fetch_create_team_response


@csrf_exempt
def create_team(request):
    response = fetch_create_team_response(request)
    return JsonResponse(response)
