from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .confirm_transaction_helpers import is_user_operator
from .confirm_transaction_helpers import get_confirm_transaction_response
from transactions.money_transfer_helpers import get_money_transfer_response


@csrf_exempt
def confirm_transaction(request):
    user = request.user
    if not user.is_superuser and not is_user_operator(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = get_confirm_transaction_response(request)
    return JsonResponse(response)


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
