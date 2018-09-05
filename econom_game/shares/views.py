from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from shares.views_helpers import is_user_financier
from .exchange_rates_helpers import get_exchange_rates
from .sell_share_helpers import fetch_sell_share_response
from .buy_share_helpers import fetch_buy_share_response
from .share_info_helpers import fetch_share_info_response


@csrf_exempt
def exchange_rates(request):
    user = request.user
    if not user.is_superuser and not is_user_financier(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    serialized_rates = get_exchange_rates()
    return JsonResponse(serialized_rates, safe=False)


@csrf_exempt
def share_info(request):
    user = request.user
    if not user.is_superuser and not is_user_financier(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = fetch_share_info_response(request)
    return JsonResponse(response)


@csrf_exempt
def sell_share(request):
    user = request.user
    if not user.is_superuser and not is_user_financier(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = fetch_sell_share_response(request)
    return JsonResponse(response)


@csrf_exempt
def buy_share(request):
    user = request.user
    if not user.is_superuser and not is_user_financier(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = fetch_buy_share_response(request)
    return JsonResponse(response)
