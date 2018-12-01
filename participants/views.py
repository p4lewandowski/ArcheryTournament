from django.shortcuts import render
from .models import Participant
from django.http import JsonResponse, HttpResponse
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def create_mock_data(num):
    mock_data = []
    for i in range(num):
        mock_data.append({'name':'N{}'.format(i),
                          'surname':'S{}'.format(i),
                          'points':'{}'.format(i)})
    return mock_data




def send_participants(request):
    if request.method == "GET":
        dictionaries = [obj.as_json() for obj in Participant.objects.all()]
        if len(dictionaries)<17:
            dictionaries.extend(create_mock_data(abs(len(dictionaries)-16)))

        dd = {"participants": dictionaries}
        return JsonResponse(dd)

@csrf_exempt
def get_participants(request):
    if request.method == "POST":
        participants = json.loads(request.body.decode('utf-8'))['participants'].split(';')

        # Add participants in fancy way
        [Participant.objects.create(name=x.split(' ')[0],
                                                   surname=x.split(' ')[1],
                                                   points=x.split(' ')[2])
                        for x in participants]

        return HttpResponse('')

def delete_database(request):
    Participant.objects.all().delete()
    return HttpResponse('')