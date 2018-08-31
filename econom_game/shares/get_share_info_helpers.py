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
    share_deals = models.ShareDeal.objects.filter(team=team)
    team_shares = [
        {
            "share_name": share_deal.sharetype.name,
            "share_count": shae_deal.amount,
        }
        for share_deal in share_deals
    ]
    return teams_shares
