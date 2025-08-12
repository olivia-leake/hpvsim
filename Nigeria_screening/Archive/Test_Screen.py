#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 16:42:59 2025

@author: olivialeake
"""


# Testing 1) putting prob - 0
#         2) adding in radiation 

# Sanity check for more simple sim

import hpvsim as hpv
import pandas as pd

prob = 0

screen      = hpv.routine_screening(start_year=2015, prob=prob, product='via', label='screen') # Routine screening
to_triage   = lambda sim: sim.get_intervention('screen').outcomes['positive'] # Define who's eligible for triage
triage      = hpv.routine_triage(eligibility=to_triage, prob=prob, product='hpv', label='triage') # Triage people
to_treat    = lambda sim: sim.get_intervention('triage').outcomes['positive'] # Define who's eligible to be assigned treatment

assign_tx   = hpv.routine_triage(eligibility=to_treat, prob=prob, product='tx_assigner', label='assign_tx') # Assign treatment

to_ablate   = lambda sim: sim.get_intervention('assign_tx').outcomes['ablation'] # Define who's eligible for ablation treatment
ablation    = hpv.treat_num(eligibility=to_ablate, prob=prob, product='ablation') # Administer ablation
# notice treat_num

to_excise   = lambda sim: sim.get_intervention('assign_tx').outcomes['excision'] # Define who's eligible for excision
excision    = hpv.treat_delay(eligibility=to_excise, prob=prob, product='excision') # Administer excision
#notice treat_delay

# Create the sim with and without interventions
orig_sim = hpv.Sim( label='Baseline')
orig_multi = hpv.MultiSim(orig_sim)
orig_multi.run(n_runs = 30)
orig_multi.plot()
orig_multi.mean()
orig_multi.plot()
orig_multi.summarize()


sim = hpv.Sim(interventions = [screen, triage, assign_tx, ablation, excision], label='With screen & treat')
sim_multi = hpv.MultiSim(sim)
sim_multi.run(n_runs=30)
a2 = sim_multi.mean()
sim_multi.plot()

orig_multi.brief()
sim_multi.brief()

merged = hpv.MultiSim.merge(orig_multi, sim_multi)
merged.plot()

# %%



# # What happens if you put treat_num instead, does this still work?

# to_excise   = lambda sim: sim.get_intervention('assign_tx').outcomes['excision'] # Define who's eligible for excision
# excision    = hpv.treat_num(eligibility=to_excise, prob=prob, product='excision') # Administer excision

# # Yes still works !





to_radiate   = lambda sim: sim.get_intervention('assign_tx').outcomes['radiation'] # Define who's eligible for excision
radiation    = hpv.treat_delay(eligibility=to_radiate, prob=prob, product='radiation') # Administer excision


to_radiate   = lambda sim: sim.get_intervention('assign_tx').outcomes['radiation'] # Define who's eligible for excision
radiation    = hpv.treat_num(eligibility=to_radiate, prob=prob, radiation) # Administer excision




# Create the sim with and without interventions
orig_sim = hpv.Sim( label='Baseline')

sim = hpv.Sim(interventions = [screen, triage, assign_tx, ablation, excision], label='With screen & treat').run()

sim.get_intervention('assign_tx').outcomes['ablation']

# Out[181]: 
# array([  527,  4232, 18406, 19322, 21368, 22862, 24779, 27014, 30414,
#        37895, 39206, 46191, 47582, 51780, 54676, 54683, 66830])


sim.get_intervention('assign_tx').outcomes['radiation']

# The number of people assigned ablation at each time-step
# array([57525])

sim.get_intervention('assign_tx').outcomes['excision']
 # array([3105, 4878])

sim.get_intervention('assign_tx').outcomes['none']

# array([ 7591,  9250, 12077, 25244, 26067, 48972, 63601])



# %%




screen      = hpv.routine_screening(start_year=2015, prob=prob, product='via', label='screen')
sim.get_intervention('assign_tx').outcomes['excision']


# Expect these to be the same

hpv.MultiSim(([sim, orig_sim])).run().plot()


print(orig_sim['interventions'])
print(sim['interventions'])
