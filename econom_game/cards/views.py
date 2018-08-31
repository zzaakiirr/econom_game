from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from cards import create_card_view_helpers
from cards.check_card_view_helpers import get_check_card_response


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
    response = get_check_card_response(request)
    return JsonResponse(response)
