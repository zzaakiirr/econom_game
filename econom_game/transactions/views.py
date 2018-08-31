from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from transactions.confirm_transaction_view_helpers import is_user_operator
from cards.check_card_view_helpers import get_card_error_response


@csrf_exempt
def confirm_transaction(request):
    user = request.user
    if not user.is_superuser and not is_user_operator(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = get_confirm_transaction_response(request)
    return JsonResponse(response)
