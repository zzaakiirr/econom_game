import json

from .models import ShareDeal, ShareType

import cards.check_card_view_helpers as check_card


def fetch_share_info_response(request):
    check_card_response = check_card.fetch_check_card_response(request)
    if not check_card_response.get('success'):
        return check_card_response

    data = json.loads(request.body.decode("utf-8"))
    card_type = data.get('card_type')
    card = data.get('card')

    team = check_card.get_team_by_card(card_type, card)
    share_info = {
        'team_name': team.name,
        'team_owner': team.owner,
        'team_money_amount': team.card.money_amount,
        'team_bank': {
            'bank_id': team.bank.id,
            'bank_name': team.bank.name,
        },
        'team_shares': None
    }
    team_shares = get_team_shares(team)
    if team_shares:
        share_info['team_shares'] = team_shares
    return share_info


def get_team_shares(team):
    share_deals = ShareDeal.objects.filter(team=team)
    team_shares = [
        {
            'share_name': share_deal.share_type.name,
            'share_amount': share_deal.amount
        }
        for share_deal in share_deals
    ]
    return team_shares
