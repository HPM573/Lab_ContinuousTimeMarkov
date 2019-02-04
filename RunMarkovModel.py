import MarkovModelClasses as Cls
import SimPy.SamplePathClasses as PathCls
import SimPy.FigureSupport as Fig
import InputData as D

# create a cohort
myCohort = Cls.Cohort(id=1,
                      pop_size=D.POP_SIZE,
                      transition_matrix=D.get_trans_rate_matrix(D.TRANS_MATRIX))

# simulate the cohort over the specified time steps
myCohort.simulate(sim_length=D.SIMULATION_LENGTH)

# plot the sample path (survival curve)
PathCls.graph_sample_path(
    sample_path=myCohort.cohortOutcomes.nLivingPatients,
    title='Survival Curve',
    x_label='Time-Step (Year)',
    y_label='Number Survived')

# plot the histogram of survival times
Fig.graph_histogram(
    data=myCohort.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=1)

# print the patient survival time
print('Mean survival time (years):',
      myCohort.cohortOutcomes.meanSurvivalTime)
# print mean time to AIDS
print('Mean time until AIDS (years)',
      myCohort.cohortOutcomes.meanTimeToAIDS)
