from django.shortcuts import render
from django.http import JsonResponse

from .views_helpers import get_transaction_result
from .models import Bank


def make_transaction(request):
    sender = request.GET['sender']
    recipient = request.GET['recipient']
    amount = int(request.GET['amount'])

    transaction_result = get_transaction_result(sender, recipient, amount)
    return JsonResponse(transaction_result)


def get_banks_list(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    banks = Bank.objects.values()
    banks_list = [bank for bank in banks]
    return JsonResponse(banks_list, safe=False)
