from shares.models import ShareRate, ShareType


def get_exchange_rates():
    rates = ShareRate.objects.all()
    half_years = set([rate.half_year for rate in rates])
    serialized_rates = {}
    for half_year in half_years:
        serialized_rates[half_year] = []
        current_half_year_rates = [
            rate for rate in rates if rate.half_year == half_year
        ]
        for current_half_year_rate in current_half_year_rates:
            share_types = ShareType.objects.filter(
                stock_price=current_half_year_rate
            )
            for share_type in share_types:
                serialized_rates[half_year].append({
                    'share_name': share_type.name,
                    'share_buy': current_half_year_rate.buy_price,
                    'share_sell': current_half_year_rate.sell_price
                })

    return serialized_rates
