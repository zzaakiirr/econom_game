from .models import ShareDeal

import cards.check_card_view_helpers as check_card


def get_share_info(data):
    team = check_card.get_team_by_card(data)
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
    team_shares = []
    for share_deal in ShareDeal.objects.all():
        if share_deal.team == team:
            share_type = share_deal.share_type
            share = {
                'share_name': sharetype.name,
                'share_count': share_deal.count
            }
            team_shares.append(share)
    return teams_shares