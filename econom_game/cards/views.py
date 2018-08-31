from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from cards.create_card_view_helpers import get_create_card_response
from cards.check_card_view_helpers import get_check_card_response


@csrf_exempt
def create_card(request):
    response = get_create_card_response(request)
    return JsonResponse(response)


@csrf_exempt
def check_card(request):
    response = get_check_card_response(request)
    return JsonResponse(response)
