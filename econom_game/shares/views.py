from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shares import models
from shares.views_helpers import is_user_financier


def exchange_rates(request):
    user = request.user
    if not user.is_superuser and not is_user_financier(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})
    rates = models.ShareRate.all()
    terms = set([rate.term for rate in rates])
    serialized_rates = []
    for term in terms:
        serialized_rates.append({
            rate.id: {
                'share_name': rate.share_type.name,
                'share_buy': rate.buy_price,
                'share_sell': rate.sell_price
            }
            for rate in [rate for rate in rates if rate.term == term]
        })
    return JsonResponse(serialized_rates)


def share_info(request):
    user = request.user
    if not user.is_superuser and not is_user_financier(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})
    pass


@csrf_exempt
def sell_share(request):
    user = request.user
    if not user.is_superuser and not is_user_financier(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})
    pass


@csrf_exempt
def buy_share(request):
    user = request.user
    if not user.is_superuser and not is_user_financier(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})
    pass
