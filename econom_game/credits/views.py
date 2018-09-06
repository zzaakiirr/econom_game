from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import cards.check_card_view_helpers as check_card
from transactions.confirm_transaction_helpers import is_user_operator
from .take_credit_helpers import fetch_take_credit_response
from .get_credit_info_helpers import fetch_credit_info_response
from .repay_credit_helpers import fetch_repay_credit_response


@csrf_exempt
def take_credit(request):
    if not is_user_operator(request.user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = fetch_take_credit_response(request)
    return JsonResponse(response)


@csrf_exempt
def get_credit_info(request):
    user = request.user
    if not user.is_superuser and not is_user_operator(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = fetch_credit_info_response(request)
    return JsonResponse(response)


@csrf_exempt
def repay_credit(request):
    if not is_user_operator(request.user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = fetch_repay_credit_response(request)
    return JsonResponse(response)
