from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from transactions.confirm_transaction_view_helpers import is_user_operator
from cards import check_card_view_helpers as check_card
from . import get_deposit_info_helpers, exclude_money_helpers
from . import invest_money_helpers


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
    deposit = invest_money_helpers.create_new_deposit(received_data)
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

    received_data = check_card.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    deposit_info = get_deposit_info_helpers.get_deposit_info(received_data)
    return JsonResponse(deposit_info)


@csrf_exempt
def exclude_money(request):
    if not is_user_operator(request.user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    received_data = exclude_money_helpers.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    exclude_money_helpers.transfer_exclude_amount_to_team_card(received_data)
    return JsonResponse({"success": True})
