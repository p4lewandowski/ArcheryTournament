import math
import random

nr_of_players = 104
free_to_16 = 8
stages = [48, 24, 16, 8, 4, 2, 1]
current_stage = stages[0]
max_nr_of_players = 2 * current_stage + free_to_16

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


ladder = {position : competing_pair for position, competing_pair in
        enumerate([(players[index][0], players[-index + free_to_16 - 1+ padding][0]) \
        if (players[index][1] == "unknown" and players[-index + free_to_16 - 1 + padding][1] == "unknown") \
        else (players[index][0], 0) if players[index][1] == "winner" \
        else (players[index][0], 0) if players[-index + free_to_16 - 1 + padding][1] == "loser" \
        else (0, 0) if players[index][0] == "N/A" and players[index - 1][1] == "winner"\
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

ladder = dict(sorted(temp_ladder.items(), key= lambda x: x[0]))

print(ladder)