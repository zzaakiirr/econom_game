from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shares import models

from shares.views_helpers import is_user_financier
import cards.check_card_view_helpers as check_card


@csrf_exempt
def exchange_rates(request):
    user = request.user
    if not user.is_superuser and not is_user_financier(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    serialized_rates = get_exchange_rates()
    return JsonResponse(serialized_rates)


@csrf_exempt
def share_info(request):
    user = request.user
    if not user.is_superuser and not is_user_financier(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    received_data = check_card.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    response = get_share_info(received_data)
    return JsonResponse(response)


@csrf_exempt
def sell_share(request):
    user = request.user
    if not user.is_superuser and not is_user_financier(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    received_data = sell_share_helpers.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    sell_share_helpers.transfer_money_from_sold_shares_to_card(received_data)
    sell_share_helpers.decrease_deal_sharetype_amount(received_data)
    return JsonResponse({'success': True})


@csrf_exempt
def buy_share(request):
    user = request.user
    if not user.is_superuser and not is_user_financier(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    received_data = check_card.get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)

    buy_share_helpers.decrease_card_money_amount_to_buyed_shares(received_data)
    buy_share_helpers.create_new_deal(received_data)

    return JsonResponse({'success': True})
