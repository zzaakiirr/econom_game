import stations.create_station_view_helpers as helpers
import cards.check_card_view_helpers as check_card


def get_money_transfer_response(give_money=True):
    card_error_response = check_card.get_card_error_response(data)
    if card_error_response:
        card_error_response['success'] = False
        return card_error_response

    money_amount = data.get('money_amount')
    if helpers.is_value_positive_integer(money_amount):
        return {
            'success': False,
            'error': 'Неверный формат денежной суммы'
        }

    team = check_card.get_team_by_card(data)
    card = check_card.get_team_card(team)
    if give_money:
        card.money_amount += data.get('money_amount')
    else:
        card.money_amount -= data.get('money_amount')

    return {'success': True}
