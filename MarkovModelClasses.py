import SimPy.RandomVariantGenerators as RVGs
import SimPy.MarkovClasses as Markov
import SimPy.SamplePathClasses as PathCls
from InputData import HealthState


class Patient:
    def __init__(self, id, trans_rate_matrix):
        """ initiates a patient
        :param id: ID of the patient
        :param trans_rate_matrix: transition rate matrix
        """
        self.id = id
        # gillespie algorithm
        self.gillespie = Markov.Gillespie(transition_rate_matrix=trans_rate_matrix)
        self.stateMonitor = PatientStateMonitor()  # patient state monitor

    def simulate(self, sim_length):
        """ simulate the patient over the specified simulation length """

        rng = RVGs.RNG(seed=self.id)  # random number generator for this patient
        t = 0  # simulation time
        if_stop = False

        while not if_stop:
            # find time until next event (dt), and next state
            # (note that the gillespie algorithm returns None for dt if the process
            # is in an absorbing state)
            dt, new_state_index = self.gillespie.get_next_state(
                current_state_index=self.stateMonitor.currentState.value,
                rng=rng)

            # stop if time to next event (dt) is None or the next event occurs beyond simulation length
            if dt is None or dt + t > sim_length:
                if_stop = True
            else:
                # advance time to the time of next event
                t += dt
                # update health state
                self.stateMonitor.update(time=t, new_state=HealthState(new_state_index))


class PatientStateMonitor:
    """ to update patient outcomes (years survived, cost, etc.) throughout the simulation """
    def __init__(self):

        self.currentState = HealthState.CD4_200to500    # current health state
        self.survivalTime = None      # survival time
        self.timeToAIDS = None        # time to develop AIDS
        self.ifDevelopedAIDS = False  # if the patient developed AIDS

    def update(self, time, new_state):
        """
        update the current health state to the new health state
        :param time: current time
        :param new_state: new state
        """

        # update survival time
        if new_state == HealthState.HIV_DEATH or HealthState.NATUAL_DEATH:
            self.survivalTime = time

        # update time until AIDS
        if self.currentState != HealthState.AIDS and new_state == HealthState.AIDS:
            self.ifDevelopedAIDS = True
            self.timeToAIDS = time

        # update current health state
        self.currentState = new_state


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
        """ simulate the cohort of patients over the specified number of time-steps
        :param sim_length: simulation length
        """

        # populate the cohort
        patients = []
        for i in range(self.popSize):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=self.id * self.popSize + i,
                              trans_rate_matrix=self.transRateMatrix)
            # add the patient to the cohort
            patients.append(patient)

        # simulate all patients
        for patient in patients:
            # simulate
            patient.simulate(sim_length)

        # store outputs of this simulation
        self.cohortOutcomes.extract_outcomes(simulated_patients=patients)


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []         # patients' survival times
        self.timesToAIDS = []           # patients' times to AIDS
        self.meanSurvivalTime = None    # mean survival times
        self.meanTimeToAIDS = None      # mean time to AIDS
        self.nLivingPatients = None     # survival curve (sample path of number of alive patients over time)

    def extract_outcomes(self, simulated_patients):
        """ extracts outcomes of a simulated cohort
        :param simulated_patients: a list of simulated patients"""

        # record survival time and time until AIDS
        for patient in simulated_patients:
            if not (patient.stateMonitor.survivalTime is None):
                self.survivalTimes.append(patient.stateMonitor.survivalTime)
            if patient.stateMonitor.ifDevelopedAIDS:
                self.timesToAIDS.append(patient.stateMonitor.timeToAIDS)

        # calculate mean survival time
        self.meanSurvivalTime = sum(self.survivalTimes) / len(self.survivalTimes)
        # calculate mean time to AIDS
        self.meanTimeToAIDS = sum(self.timesToAIDS)/len(self.timesToAIDS)

        # survival curve
        self.nLivingPatients = PathCls.PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size=len(simulated_patients),
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )
