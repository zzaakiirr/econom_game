import json

from shares import models


def get_received_data(request):
    data = json.loads(request.body.decode("utf-8"))

    error_response = get_error_response(data)
    if error_response:
        error_response['success'] = False
        return error_response

    data['success'] = True
    return data


def get_error_response(data):
    expected_fields = ('card_type', 'card', 'share_type', 'count')
    not_received_fields = helpers.get_not_recieved_fields(
        data, expected_fields
    )
    if not_received_fields:
        return helpers.get_not_received_all_expected_fields_error_response(
            not_received_fields)

    response = check_card.get_card_error_response(data)
    if response.get('error'):
        return response

    sharetype_to_buy = received_data.get('share_type')
    amount_to_buy = received_data.get('amount')

    team = check_card.get_team_by_card(data)
    card = check_card.get_team_card(team)
    sharetype = models.ShareType.objects.filter(name=sharetype_to_buy)
    price = sharetype.stock_price.buy_price

    if not helpers.is_value_positive_integer(amount_to_buy):
        response['error'] = 'Неверный формат количества акций для покупки'

    elif not sharetype:
        response['error'] = 'Такого типа акций нет'

    if sharetype.amount < amount_to_buy:
        response['error'] = 'Такого количества акций нет в наличии'

    elif not sharetype.stock_price:
        response['error'] = 'У акций не заполнены расценки'

    if card.money_amount < price * amount_to_buy:
        response['error'] = 'Недостаточно средств на карте'

    return response


def create_new_deal(data):
    team = check_card.get_team_by_card(data)
    card = check_card.get_team_card(team)
    sharetype = models.ShareType.objects.filter(name=sharetype_to_buy)
    deal = models.ShareDeal.objects.filter(team=team, sharetype=sharetype)
    if not deal:
        deal = models.ShareDeal.create(
            team=team,
            sharetype=sharetype,
            amount=amount_to_buy
        )
    else:
        deal.amount += amount_to_buy
    deal.save()


def decrease_card_money_amount_to_buyed_shares(data):
    sharetype_to_buy = received_data.get('share_type')
    sharetype = models.ShareType.objects.filter(name=sharetype_to_buy)
    price = sharetype.stock_price.buy_price
    amount_to_buy = received_data.get('amount')
    card.money_amount -= price * amount_to_buy
    card.save()
