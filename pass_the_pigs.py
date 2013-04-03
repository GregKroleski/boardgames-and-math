from collections import defaultdict
from matplotlib import pyplot as plt
from random import random

PIG_PROBABILITIES = [
    ('dot', .3020),
    ('no_dot', .3490),
    ('trot', .880),
    ('razorback', .2240),
    ('snouter', .03),
    ('jowler', .0061)]

PIG_POINTS = {
    'dot': 0,
    'no_dot': 0,
    'trot': 5,
    'razorback': 5,
    'snouter': 10,
    'jowler': 15}

DOUBLE_PIG_POINTS = {
    'dot': 1,
    'no_dot': 1,
    'trot': 20,
    'razorback': 20,
    'snouter': 40,
    'jowler': 60}


def roll_pig():
    '''Returns an outcome based on the probability of the pig
    Uses a random number and running total sum of the probabilities
    to create ranges for each outcome. In the case that the probabilities
    don't add to 1 - the function repeats.'''
    r, s = random(), 0
    while True:
        for pig_prob in PIG_PROBABILITIES:
            s += pig_prob[1]
            if s >= r:
                return pig_prob[0]


def roll_the_pigs(current_round_score):
    '''Takes in a current round score, then rolls the pigs and returns
    and updated score or None if the die pig out'''
    results = [roll_pig() for pig in range(0,2)]
    # First check if both pigs are the same, there are special points if so
    if results[0] == results[1]:
        return current_round_score + DOUBLE_PIG_POINTS[results[0]]
    elif results[0] == 'dot' and results[1] == 'no_dot' or results[0] == 'no_dot' and results[1] == 'dot':
        return None
    else:
        return current_round_score + PIG_POINTS[results[0]] + PIG_POINTS[results[1]]


def play_a_round(limit):
    '''Optionall takes in a limit and then plays the round, returning
    an integer or None'''
    current_round_score = 0
    while current_round_score <= limit:
        current_round_score = roll_the_pigs(current_round_score)
        if not current_round_score:
            return None
    return current_round_score


def play_pass_the_pigs(limit=17):
    '''Plays a game of pass the pigs using the limit as a risk threshold'''
    num_rounds = 0
    total_score = 0
    while total_score < 100:
        # print total_score
        if 100 - total_score < limit:
            limit = 100 - total_score
        round_score = play_a_round(limit)
        if not round_score:
            pass
        else:
            total_score += round_score
        num_rounds += 1
    return total_score, num_rounds


def run_threshold_simulation():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    result_dict = defaultdict(list)
    for threshold in range(0, 101):
        # Run each simulation 1000 times
        for i in range(1, 1000):
            total_score, num_rounds = play_pass_the_pigs(limit=threshold)
            result_dict[threshold].append(num_rounds)
    ax.boxplot(result_dict)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    run_threshold_simulation()
