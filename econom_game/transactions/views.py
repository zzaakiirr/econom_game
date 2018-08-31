from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .confirm_transaction_helpers import is_user_operator
from .confirm_transaction_helpers import get_confirm_transaction_response


@csrf_exempt
def confirm_transaction(request):
    user = request.user
    if not user.is_superuser and not is_user_operator(user):
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    response = get_confirm_transaction_response(request)
    return JsonResponse(response)
