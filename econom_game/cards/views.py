from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from . import create_card_view_helpers
from . import check_card_view_helpers


@csrf_exempt
def create_card(request):
    received_data = create_card_view_helpers.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    new_card = create_card_view_helpers.create_new_card(received_data)
    if not new_card._state.db:
        return JsonResponse({
            "success": False, "error": "Карта не была добавлена в базу данных"
        })

    return JsonResponse({"success": True})


@csrf_exempt
def check_card(request):
    received_data = check_card_view_helpers.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    team = check_card_view_helpers.get_team_by_card(received_data)
    return JsonResponse({
        'success': True,
        'team_name': team.name
    })
