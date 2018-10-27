from django.http import HttpResponse
import json
from django.http import JsonResponse


def json_pass(request):

    # return HttpResponse(json.dumps({'message': 'Mam nadzieje, ze teraz zadziala', 'nonie':'serio'}), content_type='application/json')
    return JsonResponse({'message': 'Mam nadzieje, ze teraz zadziala', 'nonie':'serio'})
