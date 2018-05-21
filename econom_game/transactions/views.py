from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

from transactions import transactions_helpers


@user_passes_test(lambda u: u.is_superuser)
def make_transaction(request):
    sender = request.GET['sender']
    recipient = request.GET['recipient']
    amount = int(request.GET['amount'])

    transaction_result = transactions_helpers.get_transaction_result(
        sender, recipient, amount
    )
    return JsonResponse(transaction_result)
