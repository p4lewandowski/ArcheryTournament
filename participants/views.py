from django.shortcuts import render
from .models import Participant
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import math, random, json
import random
# Create your views here.

participants = []
def create_mock_data(num):
    """
    Create number of temporary Participants objects.
    :param num: Number of objects to create.
    :return: List of Participants objects.
    """
    mock_data = []
    for i in range(num):
        mock_data.append(Participant(name='N{}'.format(i),
                          surname='S{}'.format(i),
                          points=random.randint(0,31)))
    return mock_data

def send_participants(request):
    """
    Returns all saved Participants objects in the database.
    :param request:
    :return:
    """
    if request.method == "GET":
        dictionaries = [obj.as_json() for obj in Participant.objects.all()]
        if len(dictionaries)<17:
            dictionaries.extend(create_mock_data(abs(len(dictionaries)-16)))

        dd = {"participants": dictionaries}
        return JsonResponse(dd)

@csrf_exempt
def get_participants(request):
    """
    Endpoint to receive participants in json format.
    :param request:
    :return:
    """
    if request.method == "POST":
        participants = json.loads(request.body.decode('utf-8'))['participants'].split(';')

        # Add participants in fancy way
        [Participant.objects.get_or_create(name=x.split(' ')[0],
                                                   surname=x.split(' ')[1],
                                                   points=x.split(' ')[2])
                        for x in participants]

        return HttpResponse('')

def getsort_participants(number):
    """
    Returns sorted list of participants. If required more than there are objects
    in the database - create mock objects.
    :param number: Number of best participants to pick.
    :return: list of participants
    """
    participants = list(Participant.objects.order_by('points'))[::-1]
    if len(participants) < number:
        participants.extend(create_mock_data(number-len(participants)))
        participants.sort(key=lambda x: x.points)
    participants = [str(x) for x in participants]
    return participants[:number]

def delete_database(request):
    """
    Deletes objects currently saved to the database.
    :param request:
    :return:
    """
    Participant.objects.all().delete()
    return HttpResponse('')

def next_round(ladder):
    competitors0 = [competing_pair[0] for competing_pair in ladder.values()]
    competitors1 = [competing_pair[1] for competing_pair in ladder.values()]
    temp = competitors0[-1]
    competitors0 = [competitors0[0]] + [competitors1[0]] + competitors0[1:-1]
    competitors1 = competitors1[1:] + [temp]
    for position in ladder.keys():
        ladder[position] = (competitors0[position - 1], competitors1[position - 1])
    return ladder

def ladder_tournament(request):
    nr_of_players = 104
    free_to_16 = 8
    stages = [48, 24, 16, 8, 4, 2, 1]
    current_stage = stages[0]
    max_nr_of_players = 2 * current_stage + free_to_16
    participants = getsort_participants(nr_of_players)

    players = []

    for stage in stages:
        if nr_of_players > stage + free_to_16:
            max_nr_of_players = 2 * stage + free_to_16
            current_stage = stage
            break

    if current_stage < 24:
        max_nr_of_players = max_nr_of_players - free_to_16

    for player_nr in range(1, nr_of_players + 1):
        if player_nr <= 8:
            if current_stage >= 24:
                players.append((player_nr, "winner"))
            else:
                players.append((player_nr, "unknown"))
            if current_stage == 48:
                players.append(("N/A", "loser"))
        else:
            players.append((player_nr, "unknown"))

    for player_nr in range(nr_of_players + 1, max_nr_of_players + 1):
        players.append((player_nr, "loser"))

    if current_stage < 24:
        free_to_16 = 0

    nr_of_pairs = math.ceil((max_nr_of_players - free_to_16) / 2)

    padding = 0
    if current_stage == 48:
        padding = 8

    ladder = {position: competing_pair for position, competing_pair in
              enumerate([(players[index][0], players[-index + free_to_16 - 1 + padding][0]) \
                             if (
                          players[index][1] == "unknown" and players[-index + free_to_16 - 1 + padding][1] == "unknown") \
                             else (players[index][0], 0) if players[index][1] == "winner" \
                  else (players[index][0], 0) if players[-index + free_to_16 - 1 + padding][1] == "loser" \
                  else (0, 0) if players[index][0] == "N/A" and players[index - 1][1] == "winner" \
                  else (players[index][0], "Cos jest nie tak") \
                         for index in range(0, nr_of_pairs + free_to_16 + padding)], 1)}

    temp_ladder = {}

    steps = 1
    if current_stage == 48:
        steps = 5
    elif current_stage == 24:
        steps = 4
    elif current_stage == 16:
        steps = 3
    elif current_stage == 8:
        steps = 2
    else:
        steps = 1

    temp_ladder[1] = ladder[1]
    total_number_of_places = list(ladder.keys())[-1]

    for index in range(1, 17):
        if index % 2 == 1:
            starting_position = 0
            for element in temp_ladder.items():
                if element[1][0] == index or element[1][1] == index:
                    starting_position = element[0]
            competitor_number = int(total_number_of_places / 2) - (index - 1)
            step = 2
            new_position = starting_position + 1 + step
            if steps == 0:
                steps = 1
            for _ in range(0, steps):
                for element in ladder.items():
                    if element[1][0] == competitor_number or element[1][1] == competitor_number:
                        temp_ladder[new_position] = element[1]
                step = step * 2
                new_position = new_position + step
                competitor_number = competitor_number / 2 - int(index / 2)
        else:
            starting_position = 0
            for element in temp_ladder.items():
                if element[1][0] == index or element[1][1] == index:
                    starting_position = element[0]
            competitor_number = int(total_number_of_places / 2) - (index - 1)
            step = 2
            new_position = starting_position - 1 - step
            if steps == 0:
                steps = 1
            for _ in range(0, steps):
                for element in ladder.items():
                    if element[1][0] == competitor_number or element[1][1] == competitor_number:
                        temp_ladder[new_position] = element[1]
                step = step * 2
                new_position = new_position - step
                competitor_number = int(competitor_number / 2) - int(index / 2 - 1)
            steps = steps - 1

    if current_stage == 48:
        empty_places = dict({})
        for element in temp_ladder.items():
            if element[1][0] in [1, 3, 5, 7]:
                empty_places[element[0] + 1] = (0, 0)
            if element[1][0] in [2, 4, 6, 8]:
                empty_places[element[0] - 1] = (0, 0)

        temp_ladder.update(empty_places)

    available_places = []

    for i in range(1, list(ladder.keys())[-1] + 1):
        if i not in list(temp_ladder.keys()):
            available_places.append(i)

    for element in ladder.values():
        if element not in list(temp_ladder.values()):
            random_index = random.randint(0, len(available_places) - 1)
            temp_ladder[available_places[random_index]] = element
            available_places.remove(available_places[random_index])



    ladder = dict(sorted(temp_ladder.items(), key=lambda x: x[0]))
    #Placing name and surname in place of id
    for duel in ladder.keys():
        ladder[duel] = (participants[ladder[duel][0]-1],
                        participants[ladder[duel][1]-1])

    return JsonResponse(ladder)

def ladder_all(request, nr_of_players, participants):

    nr_of_rounds = 1
    complete_ladder = []

    player_numbers = range(1, nr_of_players + 1)

    if nr_of_players % 2:
        player_numbers += ["free"]
        nr_of_rounds = nr_of_players
    else:
        nr_of_rounds = nr_of_players - 1

    nr_of_pairs = math.ceil(nr_of_players / 2)

    ladder = {position: competing_pair for position, competing_pair in
              enumerate([(player_numbers[index], player_numbers[-(index + 1)]) for index in range(0, nr_of_pairs)], 1)}
    complete_ladder.append(ladder.copy())

    for round_nr in range(0, nr_of_rounds):
        print("Round nr {}".format(round_nr + 1))
        print(ladder)
        ladder = next_round(ladder)
        complete_ladder.append(ladder.copy())

    #Placing name and surname in place of id
    for round in complete_ladder:
        for duel in round.keys():
            round[duel] = (participants[round[duel][0]-1],
                           participants[round[duel][1]-1])

    dict_ladder = dict(zip(list(range(1, nr_of_rounds+1)), complete_ladder))

    return JsonResponse(dict_ladder)

@csrf_exempt
def buildladder_all(request):
    if request.method == "POST":
        participants_id = json.loads(request.body.decode('utf-8'))['participantIds']
        participants = Participant.objects.filter(id__in=participants_id).order_by('points')[::-1]
        participants = [str(x) for x in participants]

        participantsCount = json.loads(request.body.decode('utf-8'))['participantsCount']

        return ladder_all(request, participantsCount, participants)

def teamladder_tournament():
    #Use whole team as a member for tournament method
    pass

def teamladder_freepass():
    druzyny = [24]
    posortowane_druzyny = [24]
    drabinka_pucharowa = [32]

    if len(posortowane_druzyny) > 16:
        drabinka_pucharowa[0] = posortowane_druzyny[0]
        drabinka_pucharowa[1] = ""
        drabinka_pucharowa[2] = posortowane_druzyny[15]
        drabinka_pucharowa[3] = posortowane_druzyny[16]
        drabinka_pucharowa[4] = posortowane_druzyny[23]
        drabinka_pucharowa[5] = posortowane_druzyny[8]
        drabinka_pucharowa[6] = ""
        drabinka_pucharowa[7] = posortowane_druzyny[7]
        drabinka_pucharowa[8] = posortowane_druzyny[4]
        drabinka_pucharowa[9] = ""
        drabinka_pucharowa[10] = posortowane_druzyny[11]
        drabinka_pucharowa[11] = posortowane_druzyny[20]
        drabinka_pucharowa[12] = posortowane_druzyny[12]
        drabinka_pucharowa[13] = posortowane_druzyny[19]
        drabinka_pucharowa[14] = posortowane_druzyny[3]
        drabinka_pucharowa[15] = ""
        drabinka_pucharowa[16] = posortowane_druzyny[2]
        drabinka_pucharowa[17] = ""
        drabinka_pucharowa[18] = posortowane_druzyny[13]
        drabinka_pucharowa[19] = posortowane_druzyny[18]
        drabinka_pucharowa[20] = posortowane_druzyny[10]
        drabinka_pucharowa[21] = posortowane_druzyny[21]
        drabinka_pucharowa[22] = posortowane_druzyny[5]
        drabinka_pucharowa[23] = ""
        drabinka_pucharowa[24] = posortowane_druzyny[6]
        drabinka_pucharowa[25] = ""
        drabinka_pucharowa[26] = posortowane_druzyny[9]
        drabinka_pucharowa[27] = posortowane_druzyny[22]
        drabinka_pucharowa[28] = posortowane_druzyny[14]
        drabinka_pucharowa[29] = posortowane_druzyny[17]
        drabinka_pucharowa[30] = ""
        drabinka_pucharowa[31] = posortowane_druzyny[1]
    elif len(posortowane_druzyny) > 8:
        drabinka_pucharowa[0] = posortowane_druzyny[0]
        drabinka_pucharowa[1] = posortowane_druzyny[15]
        drabinka_pucharowa[2] = posortowane_druzyny[8]
        drabinka_pucharowa[3] = posortowane_druzyny[7]
        drabinka_pucharowa[4] = posortowane_druzyny[4]
        drabinka_pucharowa[5] = posortowane_druzyny[11]
        drabinka_pucharowa[6] = posortowane_druzyny[12]
        drabinka_pucharowa[7] = posortowane_druzyny[3]
        drabinka_pucharowa[8] = posortowane_druzyny[2]
        drabinka_pucharowa[9] = posortowane_druzyny[13]
        drabinka_pucharowa[10] = posortowane_druzyny[10]
        drabinka_pucharowa[11] = posortowane_druzyny[5]
        drabinka_pucharowa[12] = posortowane_druzyny[6]
        drabinka_pucharowa[13] = posortowane_druzyny[9]
        drabinka_pucharowa[14] = posortowane_druzyny[14]
        drabinka_pucharowa[15] = posortowane_druzyny[1]
    elif len(posortowane_druzyny) > 4:
        drabinka_pucharowa[0] = posortowane_druzyny[0]
        drabinka_pucharowa[1] = posortowane_druzyny[7]
        drabinka_pucharowa[2] = posortowane_druzyny[4]
        drabinka_pucharowa[3] = posortowane_druzyny[3]
        drabinka_pucharowa[4] = posortowane_druzyny[2]
        drabinka_pucharowa[5] = posortowane_druzyny[5]
        drabinka_pucharowa[6] = posortowane_druzyny[6]
        drabinka_pucharowa[7] = posortowane_druzyny[1]
    elif len(posortowane_druzyny) > 2:
        drabinka_pucharowa[0] = posortowane_druzyny[0]
        drabinka_pucharowa[1] = posortowane_druzyny[3]
        drabinka_pucharowa[2] = posortowane_druzyny[2]
        drabinka_pucharowa[3] = posortowane_druzyny[1]
    elif len(posortowane_druzyny) > 1:
        drabinka_pucharowa[0] = posortowane_druzyny[0]
        drabinka_pucharowa[1] = posortowane_druzyny[1]

def teamladder_nofreepass():
    druzyny = [16]
    posortowane_druzyny = [16]
    drabinka_pucharowa = [16]

    if len(posortowane_druzyny) > 8:
        drabinka_pucharowa[0] = posortowane_druzyny[0]
        drabinka_pucharowa[1] = posortowane_druzyny[15]
        drabinka_pucharowa[2] = posortowane_druzyny[8]
        drabinka_pucharowa[3] = posortowane_druzyny[7]
        drabinka_pucharowa[4] = posortowane_druzyny[4]
        drabinka_pucharowa[5] = posortowane_druzyny[11]
        drabinka_pucharowa[6] = posortowane_druzyny[12]
        drabinka_pucharowa[7] = posortowane_druzyny[3]
        drabinka_pucharowa[8] = posortowane_druzyny[2]
        drabinka_pucharowa[9] = posortowane_druzyny[13]
        drabinka_pucharowa[10] = posortowane_druzyny[10]
        drabinka_pucharowa[11] = posortowane_druzyny[5]
        drabinka_pucharowa[12] = posortowane_druzyny[6]
        drabinka_pucharowa[13] = posortowane_druzyny[9]
        drabinka_pucharowa[14] = posortowane_druzyny[14]
        drabinka_pucharowa[15] = posortowane_druzyny[1]
    elif len(posortowane_druzyny) > 4:
        drabinka_pucharowa[0] = posortowane_druzyny[0]
        drabinka_pucharowa[1] = posortowane_druzyny[7]
        drabinka_pucharowa[2] = posortowane_druzyny[4]
        drabinka_pucharowa[3] = posortowane_druzyny[3]
        drabinka_pucharowa[4] = posortowane_druzyny[2]
        drabinka_pucharowa[5] = posortowane_druzyny[5]
        drabinka_pucharowa[6] = posortowane_druzyny[6]
        drabinka_pucharowa[7] = posortowane_druzyny[1]
    elif len(posortowane_druzyny) > 2:
        drabinka_pucharowa[0] = posortowane_druzyny[0]
        drabinka_pucharowa[1] = posortowane_druzyny[3]
        drabinka_pucharowa[2] = posortowane_druzyny[2]
        drabinka_pucharowa[3] = posortowane_druzyny[1]
    elif len(posortowane_druzyny) > 1:
        drabinka_pucharowa[0] = posortowane_druzyny[0]
        drabinka_pucharowa[1] = posortowane_druzyny[1]