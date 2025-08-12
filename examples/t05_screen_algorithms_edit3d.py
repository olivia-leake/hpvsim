'''
Construct the 7 screen and treat algorithms recommended by the WHO
See documentation here: https://www.ncbi.nlm.nih.gov/books/NBK572308/
'''

import hpvsim as hpv
import numpy as np

debug = 1

def make_sim(seed=0):
    ''' Make a single sim '''

    # Parameters
    pars = dict(
        n_agents        = [50e3,5e3][debug],
        dt              = [0.5,1.0][debug],
        start           = [1975,2000][debug],
        end             = 2060,
        ms_agent_ratio  = 10,
        burnin          = [45,0][debug],
        rand_seed       = seed,
    )
    sim = hpv.Sim(pars=pars)
    return sim


def make_algorithms(sim=None, seed=0, debug=debug):

    if sim is None: sim = make_sim(seed=seed)

    # Shared parameters
    primary_screen_prob = 0
    triage_screen_prob = 0
    ablate_prob = 0
    start_year = 2025
    screen_eligible = lambda sim: np.isnan(sim.people.date_screened) | (sim.t > (sim.people.date_screened + 5 / sim['dt']))


  

    ####################################################################
    #### Algorithm 7 (https://www.ncbi.nlm.nih.gov/books/NBK572308/)
    # HPV DNA as the primary screening test, followed by cytology triage,
    # followed by colposcopy and treatment
    ####################################################################

    hpv_primary7 = hpv.routine_screening(
        product='hpv',
        prob=primary_screen_prob,
        eligibility=screen_eligible,
        start_year=start_year,
        label='hpv primary',
    )

    # Send HPV+ women for cytology
    to_cytology = lambda sim: sim.get_intervention('hpv primary').outcomes['positive']
    cytology7 = hpv.routine_triage(
        product='lbc',
        annual_prob=False,
        prob=triage_screen_prob,
        eligibility=to_cytology,
        label='cytology',
    )

    # Send ASCUS and abnormal cytology results for colpo
    to_colpo = lambda sim: list(set(sim.get_intervention('cytology').outcomes['abnormal'].tolist() + sim.get_intervention('cytology').outcomes['ascus'].tolist()))
    colpo7 = hpv.routine_triage(
        product='colposcopy',
        annual_prob=False,
        prob=triage_screen_prob,
        eligibility=to_colpo,
        label='colposcopy',
    )


    # After colpo, treat HSILs with ablation
    hsils = lambda sim: sim.get_intervention('colposcopy').outcomes['hsil']
    ablation7 = hpv.treat_num(
        prob = ablate_prob,
        product = 'ablation',
        eligibility = hsils,
        label = 'ablation'
    )

    algo7 = [hpv_primary7, cytology7, colpo7, ablation7]
    for intv in algo7: intv.do_plot=False                   # Don't plot the individual interventions


    ####################################################################
    #### Set up scenarios to compare algoriths
    ####################################################################

    # Create, run, and plot the simulations
    sim0 = hpv.Sim(label='No screening')
    sim7 = hpv.Sim(interventions=algo7, label='Algorithm 7')
    
    
    # sim0.run()
    # sim7.run()
    
    hpv.MultiSim([sim0, sim7]).run().plot()
    
    
    # msim = hpv.parallel([sim0,  sim7])                             

    # msim.compare()

    return msim




#%% Run as a script
if __name__ == '__main__':

    msim = make_algorithms()
    
    
# %%
    

# Testing 
make_sim()['dt']
# Loading location-specific demographic data for "nigeria"
# Out[109]: 1.0

