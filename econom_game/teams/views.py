from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from teams import views_helpers


@csrf_exempt
def create_team(request):
    response = views_helpers.get_create_team_response(request)
    return JsonResponse(response)
