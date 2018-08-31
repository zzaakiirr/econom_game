from shares.models import ShareRate
from accounts.models import Financier


def is_user_financier(user):
    financiers = Financier.objects.all()
    return user in [financier.user for financier in financiers]


def get_exchange_rates():
    rates = ShareRate.objects.all()
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
    return serialized_rates
