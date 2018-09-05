import json

from shares.models import ShareType, ShareDeal
from timings.models import Timing

import stations.create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card


def fetch_buy_share_response(request):
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

    share_type_to_buy = data.get('share_type')
    amount_to_buy = data.get('amount')

    team = check_card.get_team_by_card(card_type, card)
    team_card = check_card.get_team_card(team)
    share_type = ShareType.objects.filter(name=share_type_to_buy)
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
    current_price = stock_price[0].buy_price

    error_response = get_error_response(
        share_type, amount_to_buy, current_price, team_card
    )
    if error_response:
        error_response['success'] = False
        return error_response

    decrease_card_money_amount_to_buyed_shares_price(
        team_card, current_price, amount_to_buy
    )

    deal = ShareDeal.objects.filter(team=team, share_type=share_type)
    if deal:
        deal[0].amount += amount_to_buy
        deal[0].save()
    else:
        deal = create_new_deal(team, share_type, amount_to_buy)

    return {'success': True}


def get_error_response(share_type, amount_to_buy, price, team_card):
    response = {}

    if not helpers.is_value_positive_integer(amount_to_buy):
        response['error'] = 'Неверный формат количества акций для покупки'

    elif share_type.amount < amount_to_buy:
        response['error'] = 'Такого количества акций нет в наличии'

    elif team_card.money_amount < price * amount_to_buy:
        response['error'] = 'Недостаточно средств на карте'

    return response


def create_new_deal(team, share_type, amount_to_buy):
    deal = ShareDeal.objects.create(
        team=team,
        share_type=share_type,
        amount=amount_to_buy
    )
    deal.save()


def decrease_card_money_amount_to_buyed_shares_price(
        team_card, price, amount_to_buy):
    team_card.money_amount -= price * amount_to_buy
    team_card.save()
