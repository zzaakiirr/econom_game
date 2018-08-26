from django.http import JsonResponse

from .views_helpers import get_transaction_result


def make_transaction(request):
    sender = request.GET['sender']
    recipient = request.GET['recipient']
    amount = int(request.GET['amount'])

    transaction_result = get_transaction_result(sender, recipient, amount)
    return JsonResponse(transaction_result)
