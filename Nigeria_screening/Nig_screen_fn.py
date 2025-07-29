#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 10:14:25 2025

@author: olivialeake
"""

## Create a screening function to be used to make scripts easier to read

import sys
import os
import numpy as np
import sciris as sc
sys.path.append('/Users/olivialeake/Documents/BSP project/HPV Project/hpvsim')

import hpvsim as hpv

from Nigeria_screening.Nigeria_sim_fn import make_nigeria_sim

# %%



def add_screening(age_range, label, vax=True, years=np.arange(2026,2050), interventions=None, **kwargs): 
    #Start year is 2026 by default, and increases yearly
    
    '''
    Create a new sim with a routine screening strategy
    Vaccination added in Oct 2023 is handled by make_nigeria_sim via vax=True/False
    '''
    
    if interventions is None:
        interventions = []
        
    
    # Defaults
    prob = 0.3 # Could consider starting at 60% then increasing to 90% as becomes more popular) #0.6
    prob_treat = 0.3 # Assume few woman would refuse treatment #0.95
    
    
    # the probability (60%) that eligible individuals between the ages of 25 64
    # in the population will undergo routine screening.

    # Triage will be performed if tested positive for HPV regardless
    # of whether they are over the age of 64 


    # First do hpv test
    screen      = hpv.routine_screening(years=years, age_range = age_range, prob=prob, product='hpv', label='screen') # Routine screening
    to_triage   = lambda sim: sim.get_intervention('screen').outcomes['positive'] # Define who's eligible for triage

    # Relfex cytology (perform lbc on the same sample that test positive for HPV)
    # This is done automatically so prob = 1 here
    triage      = hpv.routine_triage(eligibility=to_triage, prob=1, product='hpv', label='triage') # Triage people
    to_treat    = lambda sim: sim.get_intervention('triage').outcomes['positive'] # Define who's eligible to be assigned treatment


    # This function decides who gets what treatment - not sure what this is based off?
    # Is there a prob distn that shows what the percentage of woman who get what is?
    assign_tx   = hpv.routine_triage(eligibility=to_treat, prob=1, product='tx_assigner', label='assign_tx') # Assign treatment

    # The people to ablate are the ones that got ablation as the treatment assignment
    to_ablate   = lambda sim: sim.get_intervention('assign_tx').outcomes['ablation'] # Define who's eligible for ablation treatment
    ablation    = hpv.treat_num(eligibility=to_ablate, prob=prob_treat, product='ablation') # Administer ablation

    # The people to excise are the ones that got excision as the treatment assignment
    to_excise   = lambda sim: sim.get_intervention('assign_tx').outcomes['excision'] # Define who's eligible for excision
    excision    = hpv.treat_delay(eligibility=to_excise, prob=prob_treat, product='excision') # Administer excision
    
    
    ## Apply it to the sim
    sim = make_nigeria_sim(interventions = interventions + [screen, triage, assign_tx, ablation, excision], vax=vax, label = label, **kwargs)
    # If vax = False, then vx =[], so not included in interventions
    # If vax=True, then vx = an intevention, is concatenated with the other interventions
    
    return sim


# %%

# # Not sure if Oct 2023 vax being handled okay
# # Not sure if you can iclude your own inventions on top of this screening strategy


# ## Think runs fine
# test_fn= add_screening(age_range=[25,64], label ='23 vax')
# test_fn.run()
# test_fn.plot()

# # Excluding the vax works fine|
# test_fn2= add_screening(age_range=[25,64], label ='no 23 vax', vax=False)
# test_fn2.run()
# test_fn2.plot()


# # Compare vacx vs no vax
# comp_vx = hpv.MultiSim(([test_fn, test_fn2]))
# comp_vx.plot()
# # Yes looks like the vaccination is being removed properly
# # Now I've made sure vaccination isn't being applied twice it looks like it's working much better
# %% check Oct 2023 vaccination isn't being applied twice

# print(test_fn['interventions'])
# # [hpv.routine_vx(product=quadrivalent, prob=None, age_range=[9, 14], sex=0, eligibility=None, label=None), 
# # Now only showing this vaccination once so that's good


# # Check the vaccination isn't being included in test_fn2
# print(test_fn2['interventions'])
# # Great is not being included

# %%


# # Lets check what happens if we only start the screening streategy in 2040
# test_fn3= add_screening(age_range=[25,64], label ='23 vax', years = np.arange(2040,2050))
# test_fn3.run()
# test_fn4= add_screening(age_range=[25,64], label ='no 23 vax', years = np.arange(2040,2050), vax=False)
# test_fn4.run()
# # These took ages to run but that is expected since we are applying screening every year

# comp_vx2 = hpv.MultiSim(([test_fn3, test_fn4]))
# comp_vx2.plot()
# # Producing a lot of code. I think this whole script, Maybe because it used the function that
# # is defined in this script, so it imports the whole script? But then why wouldn't it do that for 
# # the other functions?

# # Regardless, looks like it's working fine so happpy with this. 

# ## The screening strategy looks like it's doing a lot !!

# %% Final test is to compare what happens when you remove the vaccination for 2 sims

# # One of them has screeing starting in 2024, the other has no screening
# # Hope to see they look the same until 2024

# novx_nosc = make_nigeria_sim(vax=False)
# novx_sc= add_screening(vax=False, age_range=[25,64], label ='23 vax', years = np.arange(2040,2050))

# mult = hpv.MultiSim([novx_nosc,novx_sc])
# mult.run()
# mult.plot()

# # Okay yes passed the test!
# # Is running the whole script for some reason. Wonder| what would happen if I commented other secions out. 
# # would it just run this section twice?

# # Weirdly just runs it once. Anywho, it's running fine. 


# %% Check that kwargs are passed to make_nigeria_sim

# orig = add_screening(age_range=[25,64], label ='Check kwargs',years = np.arange(2040,2050))
# orig.run()
# orig.plot()

# rand = add_screening(rand_seed=2, age_range=[25,64], label ='Check kwargs',years = np.arange(2040,2050))
# rand.run()
# rand.plot()

# # # Very weirdly shaped cancers by age...
# # Think fine actualy. Think it's just picking pup on screening stopping at 64

# base=hpv.Sim()
# base.run()
# base.plot() # Just seeing what it normally looks like

# %% Haven't tried changing intervals

# base_sim = make_nigeria_sim()
# sim_int1 = sim_int2 = add_screening(age_range=[9,14], years=np.arange(2026,2050) , label ='Screen every year')
# sim_int2 = add_screening(age_range=[9,14], years=np.arange(2026,2050,2), label ='Screen every 2 years')
# sim_int5 = add_screening(age_range=[9,14], years=np.arange(2026,2050,5), label ='Screen every 5 years')

# base_sim.run()
# sim_int1.run() 
# sim_int2.run()
# sim_int5.run()
# # Okay this works



