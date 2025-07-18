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
sys.path.append("/Users/olivialeake/Library/CloudStorage/OneDrive-Nexus365/Part B/BSP project/HPV Project/hpvsim")

import hpvsim as hpv

from Nigeria_screening.Nigeria_sim_fn import make_nigeria_sim



def add_screening(age_range, label, vax=True, years=np.arange(2026,2050), interventions=None, **kwargs): 
    #Start year is 2026 by default, and increases yearly
    
    '''
    Create a new sim with a routine screening strategy
    Vaccination added in Oct 2023 is handled by make_nigeria_sim via vax=True/False
    '''
    
    if interventions is None:
        interventions = []
        
    # Add vaccinatoin if requested:
    if vax==True:    
        vx = hpv.routine_vx(prob=0.9, start_year=2024, age_range=[9,14], product='quadrivalent')
        interventions = [vx] + interventions 
    # Vaccination is being applied every year by default
    
    
    
    # Removed this as have let the make_nigeria_sim function handle vaccinations instead
    
    # # First add in the vaccination introduced in Oct 2023 to 9-14 year olds
    # if vax == True:
    #     vx = hpv.routine_vx(prob=0.9, start_year = 2024, age_range=[9,14], product='quadrivalent')
    # else: vx = []
    
    
    # Defaults
    prob = 0.6 # Could consider starting at 60% then increasing to 90% as becomes more popular)
    prob_treat = 0.95 # Assume few woman would refuse treatment
    
    
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
    sim = make_nigeria_sim(interventions = interventions + [screen, triage, assign_tx, ablation, excision], label = label, **kwargs)
    # If vax = False, then vx =[], so not included in interventions
    # If vax=True, then vx = an intevention, is concatenated with the other interventions
    
    return sim

# %%

## Not sure if Oct 2023 vax being handled okay
## Not sure if you can iclude your own inventions on top of this screening strategy


## Think runs fine
test_fn= add_screening(age_range=[25,64], label ='23 vax')
test_fn.run()
test_fn.plot()

# Excluding the vax works fine|
test_fn2= add_screening(age_range=[25,64], label ='no 23 vax', vax=False)
test_fn2.run()
test_fn2.plot()


# Compare vacx vs no vax
comp_vx = hpv.MultiSim(([test_fn, test_fn2]))
comp_vx.plot()
# Yes looks like the vaccination is being removed properly
# Doesn't change much but this is probably because the screening strategy is doing a lot
# %% check Oct 2023 vaccination isn't being applied twice
print(test_fn['interventions'])
# [hpv.routine_vx(product=quadrivalent, prob=None, age_range=[9, 14], sex=0, eligibility=None, label=None), 
# hpv.routine_vx(product=quadrivalent, prob=None, age_range=[9, 14], sex=0, eligibility=None, label=None)

# To remove one of them should I just exlude vax altogether? Will commit to main, edit and can always return to this version 

# %%

# Lets check what happens if we only start the screening streategy in 2040
test_fn3= add_screening(age_range=[25,64], label ='23 vax', years = np.arange(2040,2050))
test_fn3.run()
test_fn4= add_screening(age_range=[25,64], label ='no 23 vax', years = np.arange(2040,2050), vax=False)
test_fn4.run()


# %%



# Lets check what happens if we only start the screening streategy in 2040
test_fn3= add_screening(age_range=[25,64], label ='23 vax', years = np.arange(2040,2050))
test_fn3.run()
test_fn4= add_screening(age_range=[25,64], label ='no 23 vax', years = np.arange(2040,2050), vax=False)
test_fn4.run()

comp_vx2 = hpv.MultiSim(([test_fn3, test_fn4]))
comp_vx2.plot()

## The screening strategy looks like it's doing a lot !!
