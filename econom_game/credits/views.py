from django.http import JsonResponse

from transactions.confirm_transaction_view_helpers import is_user_operator
from . import take_credit_helpers


def take_credit(request):
    if not is_user_operator(request.user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    received_data = take_credit_helpers.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    take_credit_helpers.transfer_credit_amount_to_team_card(received_data)
    credit = take_credit_helpers.create_new_credit(received_data)
    if not credit._state.db:
        return JsonResponse({
            "success": False,
            "error": "Кредит не был добавлен в базу данных"
        })

    return JsonResponse({"success": True})