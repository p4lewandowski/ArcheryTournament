import math

def next_round(ladder):
    competitors0 = [competing_pair[0] for competing_pair in ladder.values()]
    competitors1 = [competing_pair[1] for competing_pair in ladder.values()]
    temp = competitors0[-1]
    competitors0 = [competitors0[0]] + [competitors1[0]] + competitors0[1:-1]
    competitors1 = competitors1[1:] + [temp]
    for position in ladder.keys():
        ladder[position] = (competitors0[position - 1], competitors1[position - 1])
    return ladder

nr_of_players = 16
nr_of_rounds = 1

player_numbers = range(1, nr_of_players + 1)

if nr_of_players % 2:
    player_numbers += ["free"]
    nr_of_rounds = nr_of_players
else:
    nr_of_rounds = nr_of_players - 1

nr_of_pairs = math.ceil(nr_of_players / 2)

ladder = {position : competing_pair for position, competing_pair in 
        enumerate([(player_numbers[index], player_numbers[-(index + 1)]) for index in range(0, nr_of_pairs)], 1)}

complete_ladder = []
complete_ladder.append(ladder.copy())

for round_nr in range(0, nr_of_rounds):
    print("Round nr {}".format(round_nr + 1))
    print(ladder)
    ladder = next_round(ladder)
    complete_ladder.append(ladder.copy())

print(complete_ladder)

