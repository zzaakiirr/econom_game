from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from . import views_helpers


@csrf_exempt
def create_card(request):
    received_data = views_helpers.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    new_card = views_helpers.create_new_card(received_data)
    if not new_card._state.db:
        return JsonResponse({
            "status": False, "error": "Карта не была добавлена в базу данных"
        })

    return JsonResponse({"status": True})
