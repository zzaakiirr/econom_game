from django.http import JsonResponse

from .models import Bank


def get_banks_list(request):
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Недостаточно прав'})

    banks = Bank.objects.values()
    banks_list = [bank for bank in banks]
    return JsonResponse(banks_list, safe=False)
