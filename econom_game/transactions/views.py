from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from shares.views_helpers import is_user_financier
from .confirm_transaction_helpers import is_user_operator
from .confirm_transaction_helpers import fetch_confirm_transaction_response
from .transfer_money_helpers import fetch_transfer_money_response


@csrf_exempt
def confirm_transaction(request):
    user = request.user
    if not user.is_superuser and not is_user_operator(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = fetch_confirm_transaction_response(request)
    return JsonResponse(response)


@csrf_exempt
def give_money(request):
    user = request.user
    if not user.is_superuser and not is_user_financier(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = fetch_transfer_money_response(request, give_money=True)
    return JsonResponse(response)


@csrf_exempt
def exclude_money(request):
    user = request.user
    if not user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = fetch_transfer_money_response(request, give_money=False)
    return JsonResponse(response)
