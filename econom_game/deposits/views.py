from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from transactions.confirm_transaction_helpers import is_user_operator
from cards import check_card_view_helpers as check_card
from . import invest_money_helpers

from .get_deposit_info_helpers import fetch_deposit_info_response
from .exclude_deposit_money_helpers import fetch_exclude_deposit_money_response
from .invest_money_helpers import fetch_invest_money_response


@csrf_exempt
def invest_money(request):
    if not is_user_operator(request.user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = fetch_invest_money_response(request)
    return JsonResponse(response)


@csrf_exempt
def get_deposit_info(request):
    user = request.user
    if not user.is_superuser and not is_user_operator(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = fetch_deposit_info_response(request)
    return JsonResponse(response)


@csrf_exempt
def exclude_deposit_money(request):
    if not is_user_operator(request.user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = fetch_exclude_deposit_money_response(request)
    return JsonResponse(response)
