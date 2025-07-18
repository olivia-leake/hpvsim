#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 16:51:21 2025

@author: olivialeake
"""

## Testing inteventions bug

import hpvsim as hpv
    
prob = 0.6 
# the probability (60%) that eligible individuals in the population will undergo routine screening.
screen      = hpv.routine_screening(years=[2015,2030], prob=prob, product='via', label='screen') # Routine screening
screen.years = None

# to_triage   = lambda sim: sim.get_intervention('screen').outcomes['positive'] # Define who's eligible for triage
# triage      = hpv.routine_triage(start_year=2015, eligibility=to_triage, prob=prob, product='hpv', label='triage') # Triage people

# to_treat    = lambda sim: sim.get_intervention('triage').outcomes['positive'] # Define who's eligible to be assigned treatment
# assign_tx   = hpv.routine_triage(start_year=2015, eligibility=to_treat, prob=prob, product='tx_assigner', label='assign_tx') # Assign treatment

# to_ablate   = lambda sim: sim.get_intervention('assign_tx').outcomes['ablation'] # Define who's eligible for ablation treatment
# ablation    = hpv.treat_num(start_year=2015,eligibility=to_ablate, prob=prob, product='ablation') # Administer ablation

# to_excise   = lambda sim: sim.get_intervention('assign_tx').outcomes['excision'] # Define who's eligible for excision
# excision    = hpv.treat_delay(start_year=2015,eligibility=to_excise, prob=prob, product='excision') # Administer excision



# # Define the parameters
# pars = dict(
#     n_agents      = 20e3,       # Population size
# #    n_years       = 35,         # Number of years to simulate
#     verbose       = 0,          # Don't print details of the run
#     rand_seed     = 2,          # Set a non-default seed
#     genotypes     = [16, 18],   # Include the two genotypes of greatest general interest
#     )

# Create the sim with and without interventions
# orig_sim = hpv.Sim(label='Baseline')
sim = hpv.Sim( interventions = [screen], label='With screen & treat')
# sim = hpv.Sim( interventions = [screen, triage, assign_tx, ablation, excision], label='With screen & treat')

# orig_sim.run()
sim.run()

# orig_sim.initialize(reset=True)
# orig_sim.run() # initializes fine, and runs again fine

sim.initialize(reset=True)
# ValueError: Provide either a list of years or a start year, not both.


# %% Debugging

for intv in [screen, triage, assign_tx, ablation, excision]:
    try:
        intv.initialize(screen_sim)
        print(f"{intv.label} initialized OK")
    except Exception as e:
        print(f"{intv.label} raised error: {e}")

# screen initialized OK
# triage initialized OK
# assign_tx initialized OK
# treat_num initialized OK
# treat_delay initialized OK

# All seem fine

# %% Try just do one intervention at a time to see if same issue arises

new_sim = hpv.Sim(pars, interventions =[screen], label='test')

print('years:', screen.years)
print('start_year:', screen.start_year)
print('end_year:', screen.end_year)



new_sim.run()



new_sim.initialize(reset=True)



# %%





for intv in [screen, triage, assign_tx, ablation, excision]:
    print(f"{intv.label}: years={getattr(intv, 'years', None)}, start_year={getattr(intv, 'start_year', None)}, end_year={getattr(intv, 'end_year', None)}")



for intv in [screen, triage, assign_tx, ablation, excision]:
    print(intv.__dict__)
    
print(screen.__dict__) # fine. still not sure why it sets prob to be None though
print(triage.__dict__) 






# sim.run()
# sim.initialize()


