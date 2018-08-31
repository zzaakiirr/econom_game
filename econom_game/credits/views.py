from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from transactions.confirm_transaction_helpers import is_user_operator
from cards import check_card_view_helpers as check_card
from . import take_credit_helpers, get_credit_info_helpers
from . import repay_credit_helpers


@csrf_exempt
def take_credit(request):
    if not is_user_operator(request.user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = take_credit_helpers.get_take_credit_response(request)
    return JsonResponse(response)


@csrf_exempt
def get_credit_info(request):
    user = request.user
    if not user.is_superuser and not is_user_operator(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    received_data = check_card.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    credit_info = get_credit_info_helpers.get_credit_info(received_data)
    return JsonResponse(credit_info)


@csrf_exempt
def repay_credit(request):
    if not is_user_operator(request.user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    received_data = repay_credit_helpers.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    repay_credit_helpers.transfer_repay_amount_to_team_credit(received_data)
    return JsonResponse({"success": True})
