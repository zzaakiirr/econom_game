from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from transactions.confirm_transaction_helpers import is_user_operator
from cards import check_card_view_helpers as check_card
from . import invest_money_helpers

from .get_deposit_info_helpers import get_deposit_info_response
from .exclude_deposit_money_helpers import get_exclude_deposit_money_response


@csrf_exempt
def invest_money(request):
    if not is_user_operator(request.user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    received_data = invest_money_helpers.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    invest_money_helpers.decrease_team_card_money_amount_to_invest_amount(
        received_data
    )
    deposit = invest_money_helpers.get_increased_team_deposit_or_create_new(
        received_data
    )
    if not deposit._state.db:
        return JsonResponse({
            "success": False,
            "error": "Депозит не был добавлен в базу данных"
        })

    return JsonResponse({"success": True})


@csrf_exempt
def get_deposit_info(request):
    user = request.user
    if not user.is_superuser and not is_user_operator(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = get_deposit_info_response(request)
    return JsonResponse(response)


@csrf_exempt
def exclude_deposit_money(request):
    if not is_user_operator(request.user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = get_exclude_deposit_money_response(request)
    return JsonResponse(response)
