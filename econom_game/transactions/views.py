from django.shortcuts import render
from django.http import JsonResponse

from transactions import transactions_helpers


def make_transaction(request):
    sender = request.GET['sender']
    recipient = request.GET['recipient']
    amount = int(request.GET['amount'])

    transaction_result = transactions_helpers.get_transaction_result(
        sender, recipient, amount
    )
    return JsonResponse(transaction_result)
