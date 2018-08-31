from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import cards.check_card_view_helpers as check_card

from cards.check_card_view_helpers import get_received_data
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
                'share_name': rate.sharetype.name,
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
    received_data = get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)
    team = check_card.get_team_by_card(received_data)
    card = check_card.get_team_card(team)
    deals = models.ShareDeal.objects.filter(team=team)
    response = {
        "name_team": team.name,
        "owner_team": team.owner,
        "money_team": card.money_amount,
        "shares": [
            {
                "share_name": deal.sharetype.name,
                "share_count": deal.amount,
            }
            for deal in deals
        ]
    }
    return JsonResponse(response)


@csrf_exempt
def sell_share(request):
    user = request.user
    if not user.is_superuser and not is_user_financier(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})
    received_data = get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)
    team = check_card.get_team_by_card(received_data)
    card = check_card.get_team_card(team)
    sharetype_to_sell = received_data["share_type"]
    amount_to_sell = received_data["count"]
    sharetype = models.ShareType.objects.filter(name=sharetype_to_sell)
    if not sharetype:
        return JsonResponse({'success': False, 'error': 'Такого типа нет'})
    deal = models.ShareDeal.objects.filter(team=team, sharetype=sharetype)
    if not deal:
        return JsonResponse({'success': False, 'error': 'Команда не покупала таких акций'})
    if deal.amount < amount_to_sell:
        return JsonResponse({'success': False, 'error': 'Недостаточно акций'})
    if not sharetype.stock_price:
        return JsonResponse({'success': False, 'error': 'У акций не заполнены расценки'})
    price = sharetype.stock_price.sell_price
    card.money_amount += price * amount_to_sell
    card.save()
    deal.amount -= amount_to_sell
    deal.save()


@csrf_exempt
def buy_share(request):
    user = request.user
    if not user.is_superuser and not is_user_financier(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})
    received_data = get_received_data(request)
    if not received_data['success']:
        return JsonResponse(received_data)
    team = check_card.get_team_by_card(received_data)
    card = check_card.get_team_card(team)
    sharetype_to_buy = received_data["share_type"]
    amount_to_buy = received_data["count"]
    sharetype = models.ShareType.objects.filter(name=sharetype_to_buy)
    if not sharetype:
        return JsonResponse({'success': False, 'error': 'Такого типа нет'})
    if sharetype.amount < amount_to_buy:
        return JsonResponse({'success': False, 'error': 'Такого количества акций нет в наличии'})
    if not sharetype.stock_price:
        return JsonResponse({'success': False, 'error': 'У акций не заполнены расценки'})
    price = sharetype.stock_price.buy_price
    if card.money_amount < price * amount_to_buy:
        return JsonResponse({'success': False, 'error': 'У команды недостаточно средств'})
    deal = models.ShareDeal.objects.filter(team=team, sharetype=sharetype)
    if not deal:
        deal = models.ShareDeal(
            team=team,
            sharetype=sharetype,
            amount=amount_to_buy
        )
    else:
        deal.amount += amount_to_buy
    deal.save()
    card.money_amount -= price * amount_to_buy
    card.save()
