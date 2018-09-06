import json

from timings.models import Timing
from shares.models import ShareType, ShareDeal

import stations.create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card


def fetch_sell_share_response(request):
    current_half_year = Timing.objects.all()[0].current_half_year
    data = json.loads(request.body.decode("utf-8"))

    expected_fields = ('card_type', 'card', 'share_type', 'amount')
    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    card_type = data.get('card_type')
    card = data.get('card')

    card_error_response = check_card.get_card_error_response(card_type, card)
    if card_error_response:
        card_error_response['success'] = False
        return card_error_response

    share_type_to_sell = data.get("share_type")
    amount_to_sell = data.get('amount')

    team = check_card.get_team_by_card(card_type, card)
    team_card = check_card.get_team_card(team)

    share_type = ShareType.objects.filter(name=share_type_to_sell)
    if not share_type:
        return {
            'success': False,
            'error': 'Такого типа акций нет'
        }
    share_type = share_type[0]

    stock_price = share_type.stock_price.filter(half_year=current_half_year)
    if not stock_price:
        return {
            'success': False,
            'error': 'У акций не заполнены расценки'
        }
    current_price = stock_price[0].sell_price

    deal = ShareDeal.objects.filter(team=team, share_type=share_type)
    if not deal:
        return {
            'success': False,
            'error': 'Команда не покупала таких акций'
        }
    deal = deal[0]

    error_response = get_error_response(amount_to_sell, deal)
    if error_response:
        error_response['success'] = False
        return error_response

    increase_card_money_amount_to_sold_shares_price(
        team_card, current_price, amount_to_sell
    )
    decrease_deal_share_type_amount(deal, amount_to_sell)

    return {'success': True}


def get_error_response(amount_to_sell, deal):
    response = {}

    if not helpers.is_value_positive_integer(amount_to_sell):
        response['error'] = 'Неверный формат количества акций для продажи'

    elif deal.amount < amount_to_sell:
        response['error'] = 'У команды нет такого количества акций'

    return response


def increase_card_money_amount_to_sold_shares_price(
        team_card, price, amount_to_sell):
    team_card.money_amount += price * amount_to_sell
    team_card.save()


def decrease_deal_share_type_amount(deal, amount_to_sell):
    deal.amount -= amount_to_sell
    deal.save()
