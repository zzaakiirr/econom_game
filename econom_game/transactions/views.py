from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .make_transaction_view_helpers import get_transaction_result
from . import confirm_transaction_view_helpers
from cards.check_card_view_helpers import get_received_data


def make_transaction(request):
    sender = request.GET['sender']
    recipient = request.GET['recipient']
    amount = int(request.GET['amount'])

    transaction_result = get_transaction_result(sender, recipient, amount)
    return JsonResponse(transaction_result)


@csrf_exempt
def confirm_transaction(request):
    user = request.user
    if not user.is_superuser or not confirm_transaction.is_user_operator(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    received_data = get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    won_money_amount = confirm_transaction_view_helpers.get_team_won_money(
        received_data
    )
    if confirm_transaction_view_helpers.transfer_won_money_to_card(
            request, received_data, won_money_amount):
        return JsonResponse({"won_money_amount": won_money_amount})

    return JsonResponse({
        "success": False,
        "error": "Деньги не были переведены на карту"
    })
