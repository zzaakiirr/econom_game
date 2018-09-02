from accounts.models import Financier


def is_user_financier(user):
    financiers = Financier.objects.all()
    return user in [financier.user for financier in financiers]
