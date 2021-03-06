import numpy as np
from enum import Enum
import SimPy.MarkovClasses as Markov

# simulation settings
POP_SIZE = 4000         # cohort population size
SIMULATION_LENGTH = 1000    # length of simulation (years)
# annual probability of background mortality (number per year per 1,000 population)
ANNUAL_PROB_BACKGROUND_MORT = 8.15 / 1000

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

    # find the transition probability matrix
    trans_prob_matrix = get_trans_prob_matrix(trans_matrix=trans_matrix)

    # find the transition rate matrix
    trans_rate_matrix = Markov.discrete_to_continuous(
        trans_prob_matrix=trans_prob_matrix,
        delta_t=1)

    # calculate background mortality rate
    mortality_rate = -np.log(1 - ANNUAL_PROB_BACKGROUND_MORT)

    # add background mortality rate
    for row in trans_rate_matrix:
        row.append(mortality_rate)

    # add 2 rows for HIV death and natural death
    trans_rate_matrix.append([0] * len(HealthStates))
    trans_rate_matrix.append([0] * len(HealthStates))

    return trans_rate_matrix
