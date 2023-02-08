import numpy as np
from deampy.plots.sample_paths import PrevalencePathBatchUpdate

from CTMarkovInputData import HealthStates


class Patient:
    def __init__(self, id, trans_rate_matrix):
        """ initiates a patient
        :param id: ID of the patient
        :param trans_rate_matrix: transition rate matrix
        """
        self.id = id
        self.transRateMatrix = trans_rate_matrix
        self.stateMonitor = PatientStateMonitor()  # patient state monitor

    def simulate(self, sim_length):
        """ simulate the patient over the specified simulation length """

        # random number generator for this patient
        rng = np.random.RandomState(seed=self.id)



class PatientStateMonitor:
    """ to update patient outcomes (years survived, cost, etc.) throughout the simulation """
    def __init__(self):

        self.currentState = HealthStates.CD4_200to500    # current health state
        self.survivalTime = None      # survival time
        self.ifDevelopedAIDS = False  # if the patient developed AIDS

    def update(self, time, new_state):
        """
        update the current health state to the new health state
        :param time: current time
        :param new_state: new state
        """




class Cohort:
    def __init__(self, id, pop_size, trans_rate_matrix):
        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        :param trans_rate_matrix: transition rate matrix
        """
        self.id = id
        self.popSize = pop_size
        self.transRateMatrix = trans_rate_matrix
        self.cohortOutcomes = CohortOutcomes()  # outcomes of the this simulated cohort

    def simulate(self, sim_length):
        """ simulate the cohort of patients over the specified duration
        :param sim_length: simulation length
        """

        # populate and simulate the cohort
        for i in range(self.popSize):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=self.id * self.popSize + i,
                              trans_rate_matrix=self.transRateMatrix)
            # simulate
            patient.simulate(sim_length)

            # store outputs of this simulation
            self.cohortOutcomes.extract_outcome(simulated_patient=patient)

        # calculate cohort outcomes
        self.cohortOutcomes.calculate_cohort_outcomes(initial_pop_size=self.popSize)


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []         # patients' survival times
        self.timesToAIDS = []           # patients' times to AIDS
        self.meanSurvivalTime = None    # mean survival times
        self.meanTimeToAIDS = None      # mean time to AIDS
        self.nLivingPatients = None     # survival curve (sample path of number of alive patients over time)

    def extract_outcome(self, simulated_patient):
        """ extracts outcomes of a simulated patient
        :param simulated_patient: a simulated patient"""

        # record survival time and time until AIDS
        if simulated_patient.stateMonitor.survivalTime is not None:
            self.survivalTimes.append(simulated_patient.stateMonitor.survivalTime)
        if simulated_patient.stateMonitor.timeToAIDS is not None:
            self.timesToAIDS.append(simulated_patient.stateMonitor.timeToAIDS)

    def calculate_cohort_outcomes(self, initial_pop_size):
        """ calculates the cohort outcomes
        :param initial_pop_size: initial population size
        """

        # calculate mean survival time
        self.meanSurvivalTime = sum(self.survivalTimes) / len(self.survivalTimes)
        # calculate mean time to AIDS
        self.meanTimeToAIDS = sum(self.timesToAIDS)/len(self.timesToAIDS)

        # survival curve
        self.nLivingPatients = PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size=initial_pop_size,
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )
