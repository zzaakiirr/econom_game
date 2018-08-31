# def buy_share(request):
#     user = request.user
#     if not user.is_superuser and not is_user_financier(user):
#         return JsonResponse({'success': False, 'error': 'Недостаточно прав'})
#     received_data = get_received_data(request)
#     if not received_data['success']:
#         return JsonResponse(received_data)
#     team = check_card.get_team_by_card(received_data)
#     card = check_card.get_team_card(team)
#     sharetype_to_buy = received_data["share_type"]
#     amount_to_buy = received_data["count"]
#     sharetype = models.ShareType.objects.filter(name=sharetype_to_buy)
#     if not sharetype:
#         return JsonResponse({'success': False, 'error': 'Такого типа нет'})
#     if sharetype.amount < amount_to_buy:
#         return JsonResponse({'success': False, 'error': 'Такого количества акций нет в наличии'})
#     if not sharetype.stock_price:
#         return JsonResponse({'success': False, 'error': 'У акций не заполнены расценки'})
#     price = sharetype.stock_price.buy_price
#     if card.money_amount < price * amount_to_buy:
#         return JsonResponse({'success': False, 'error': 'У команды недостаточно средств'})
#     deal = models.ShareDeal.objects.filter(team=team, sharetype=sharetype)
#     if not deal:
#         deal = models.ShareDeal(
#             team=team,
#             sharetype=sharetype,
#             amount=amount_to_buy
#         )
#     else:
#         deal.amount += amount_to_buy
#     deal.save()
#     card.money_amount -= price * amount_to_buy
#     card.save()


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

    share_type_to_sell = data.get("share_type")
    amount_to_sell = data.get('amount')

    team = check_card.get_team_by_card(data)
    card = check_card.get_team_card(team)
    sharetype = models.ShareType.objects.filter(name=sharetype_to_sell)
    deal = models.ShareDeal.objects.filter(team=team, sharetype=sharetype)

    if not helpers.is_value_positive_integer(amount_to_sell):
        response['error'] = 'Неверный формат количества акций для продажи'

    elif not sharetype:
        response['error'] = 'Такого типа акций нет'

    elif not deal:
        response['error'] = 'Команда не покупала таких акций'

    elif deal.amount < amount_to_sell:
        response['error'] = 'Недостаточно акций'

    elif not sharetype.stock_price:
        response['error'] = 'У акций не заполнены расценки'


def transfer_money_from_sold_shares_to_card(data):
    share_type_to_sell = data.get("share_type")
    sharetype = models.ShareType.objects.filter(name=sharetype_to_sell)
    price = sharetype.stock_price.sell_price
    card.money_amount += price * amount_to_sell
    card.save()


def decrease_deal_sharetype_amount(data):
    team = check_card.get_team_by_card(data)
    deal = models.ShareDeal.objects.filter(team=team, sharetype=sharetype)
    amount_to_sell = data.get('amount')

    deal.amount -= amount_to_sell
    deal.save()
