#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 11:03:29 2025

@author: olivialeake
"""

# Nigeria vaccination and screening

## Need to access the function made in Nigeria_screening
import sys
import os
import sciris as sc
sys.path.append("/Users/olivialeake/Library/CloudStorage/OneDrive-Nexus365/Part B/BSP project/HPV Project/hpvsim")


from Nigeria_screening.Nigeria_sim_fn import make_nigeria_sim
import hpvsim as hpv


# Create routine Nigeria vaccination:introduced in Oct 2023 to 90% of 9-14 year olds
vx = hpv.routine_vx(prob=0.9, start_year = 2024, age_range=[9,14], product='quadrivalent')


sim1 = make_nigeria_sim(label = 'no vax')
print(sim1.pars) # Check everything has been imported properly

sim2 = make_nigeria_sim(interventions = vx, label ='vx')

# %% Don't run this cell if you want to run the next cell - can't run the sims if they've already been ran


msim = hpv.MultiSim( [sim1, sim2] )
msim.run()
msim.plot()

# %%

# Add screening strategy

prob = 0.6 # Could consider starting at 60% then increasing to 90% as becomes more popular)

# the probability (60%) that eligible individuals between the ages of 25 64
# in the population will undergo routine screening.

# Triage will be performed if tested positive for HPV regardless
# of whether they are over the age of 64 


# First do hpv test
screen      = hpv.routine_screening(start_year=2026, age_range = [25,64], prob=prob, product='hpv', label='screen') # Routine screening
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
ablation    = hpv.treat_num(eligibility=to_ablate, prob=0.95, product='ablation') # Administer ablation

# The people to excise are the ones that got excision as the treatment assignment
to_excise   = lambda sim: sim.get_intervention('assign_tx').outcomes['excision'] # Define who's eligible for excision
excision    = hpv.treat_delay(eligibility=to_excise, prob=0.95, product='excision') # Administer excision



# Apply the strategy, to see if it helps me answer any of my questions

screen_sim = make_nigeria_sim(interventions = [vx, screen, triage, assign_tx, ablation, excision], label = 'Screening' )
screen_sim.run()
screen_sim.plot()


# %%




compare_sims = hpv.MultiSim(([sim1,sim2,screen_sim]))
# Note that this doesn't run when you have run each of the sims individually
# Initialize isn't really working so going to by-pass this by doing it from scratch each time
compare_sims.run()
compare_sims.plot()

## Questions

# Why is the probabiliity the same thorughout? Surely if a woman knows she has 
# cancer she is more likley to get treatment? 

# Q: Shouldn't you assign everyone to a treatment ,so assign_tx = 1, but whether they take it 
# or not is less?

# A: That's not what is happening. Normally the pobability for this function should be a 
# dictionary, specifyiing what portion of individuals get assigned each treatment
# if you only specify say a list with 0


#Q : Currently I haven't added in radition, however surely assign_tx will have assigned
# raditaoiton to some women. does this mean i am ignoring a bunch of women who have been diagnosed?
# Or does it mean that radiation isn't being considered to be an option if the first place?
# But this doesn't seem to be written into the model

# A :  No it means that everyone who has been assigned radiation isn\t recieving treatment

# Not sure how assign_tx is making assignments



# %%


## Note that I haven't put any data files in anywhere
# When I put Nigeria in, does it automaticlaly use the Nigeria datafiles?
# I'm assuming not, so where are they relevant? 


print(msim.t)

# %%
sim1.run()

print(sim1.t) # time step is 123
# Note that each timestep is 0.25, so this should be 30.75 years
print(sim1['start']) # 1980
print(sim1['end']) # 2030
# So yes looks correct-ish time step wise

# To check which years are being used in the sim
print(sim1.yearvec[sim.t])
