from django.http import HttpResponse
import json
from django.http import JsonResponse

def json_pass(request):
    return JsonResponse({'message': 'Kuwa działa xDDD', 'nonie':'serio'})

