from enum import Enum

import numpy as np

# simulation settings
POP_SIZE = 5000         # cohort population size
SIMULATION_LENGTH = 100    # length of simulation (years)
# annual probability of background mortality among adults
# (number per year per 1,000 population)
ANNUAL_PROB_BACKGROUND_MORT = 11.7 / 1000

# transition matrix
TRANS_MATRIX = [
    [1251,  350,    116,    17],   # CD4_200to500
    [0,     731,    512,    15],   # CD4_200
    [0,     0,      1312,   437]   # AIDS
    ]


class HealthStates(Enum):
    """ health states of patients with HIV """
    CD4_200to500 = 0
    CD4_200 = 1
    AIDS = 2
    HIV_DEATH = 3
    NATUAL_DEATH = 4


def get_trans_prob_matrix(trans_matrix):
    """
    :param trans_matrix: transition matrix containing counts of transitions between states
    :return: transition probability matrix
    """

    # initialize transition probability matrix
    trans_prob_matrix = []

    # for each row in the transition matrix
    for row in trans_matrix:
        # calculate the transition probabilities
        prob_row = np.array(row)/sum(row)
        # add this row of transition probabilities to the transition probability matrix
        trans_prob_matrix.append(prob_row)

    return trans_prob_matrix


def get_trans_rate_matrix(trans_matrix):
    """
    :param trans_matrix: transition matrix containing counts of transitions between states
    :return: transition rate matrix
    """


