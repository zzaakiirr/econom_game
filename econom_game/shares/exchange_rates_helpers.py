from shares.models import ShareRate


def get_exchange_rates():
    rates = ShareRate.all()
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
