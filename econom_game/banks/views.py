from django.http import JsonResponse

from .models import Bank
from transactions.confirm_transaction_view_helpers import is_user_operator


def get_banks_list(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    banks = Bank.objects.values()
    banks_list = [bank for bank in banks]
    return JsonResponse(banks_list, safe=False)


def take_credit(request):
    if not confirm_transaction.is_user_operator(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})
        