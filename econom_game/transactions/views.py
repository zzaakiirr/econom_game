from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from . import confirm_transaction_view_helpers
from cards.check_card_view_helpers import get_received_data
from shares.get_exchange_rates_helpers import is_user_financier
from transactions.money_transfer_helpers import get_money_transfer_response


@csrf_exempt
def confirm_transaction(request):
    user = request.user
    if not user.is_superuser and not (
                confirm_transaction_view_helpers.is_user_operator(user)
            ):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    received_data = get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    won_money_amount = confirm_transaction_view_helpers.get_team_won_money(
        received_data
    )
    if not won_money_amount:
        return JsonResponse({
            "success": False,
            "won_money_amount": 0,
        })

    if confirm_transaction_view_helpers.transfer_won_money_to_card(
            request, received_data, won_money_amount):
        return JsonResponse({
            "success": True,
            "won_money_amount": won_money_amount,
        })

    return JsonResponse({
        "success": False,
        "error": "Деньги не были переведены на карту"
    })


@csrf_exempt
def give_money(request):
    user = request.user
    if not user.is_superuser and not is_user_financier(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = get_money_transfer_response()
    return JsonResponse(response)


@csrf_exempt
def exclude_money(request):
    user = request.user
    if not user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = get_money_transfer_response(give_money=False)
    return JsonResponse(response)
