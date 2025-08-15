#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 10:14:25 2025

@author: olivialeake
"""

# NOTE : HAVE USED SAME NAMES FOR SAVING THE PLOTS FOR UK AS NIGERIA - THIS IS FINE AS LONG AS RUN EACH CELL INDIVIDUALY

# Create a screening function to be used to make scripts easier to read

import sys
import os
import numpy as np
import sciris as sc
sys.path.append('/Users/olivialeake/Documents/BSP project/HPV Project/hpvsim')

import hpvsim as hpv

from Nigeria_screening.Nigeria_sim_fn import make_nigeria_sim
from UK_screening.UK_sim_fn import make_uk_sim



def add_screening(location, age_range, label, vax=True, years=np.arange(2026,2050), interventions=None, prob_screen=None, prob_triage=None, prob_assign=None, prob_ablate=None, prob_excise=None, **kwargs): 

    # Start year is 2026 by default, and increases yearly

    # DEFAULTS #TODO: look at this
    # prob = 0.6 # Could consider starting at 60% then increasing to 90% as becomes more popular) #0.6
    # prob_treat = 0.95 # Assume few woman would refuse treatment #0.95
    
    '''
    Create a new sim with a routine screening strategy
    Vaccination added in Oct 2023 is handled by make_nigeria_sim via vax=True/False
    Similarly for UK
    '''
    
    # Allow for probabilities to be over-written
    # Probabilities will be location specific
    if location == 'nigeria':
        prob_screen = prob_screen if prob_screen is not None else 0.3
        prob_triage = prob_triage if prob_triage is not None else 1
        prob_assign = prob_assign if prob_assign is not None else 1
        prob_ablate = prob_ablate if prob_ablate is not None else 0.9
        prob_excise = prob_excise if prob_excise is not None else 0.6

    elif location == 'uk':
        prob_screen = prob_screen if prob_screen is not None else 0.7
        prob_triage = prob_triage if prob_triage is not None else 1
        prob_assign = prob_assign if prob_assign is not None else 1
        prob_ablate = prob_ablate if prob_ablate is not None else 0.9
        prob_excise = prob_excise if prob_excise is not None else 0.9  # More likely to screen in UK
    
    
    if interventions is None:
        interventions = []
    
    
    # the probability (60%) that eligible individuals between the ages of 25 64
    # in the population will undergo routine screening.

    # Triage will be performed if tested positive for HPV regardless
    # of whether they are over the age of 64 


    # First do hpv test
    screen      = hpv.routine_screening(years=years, age_range = age_range, prob=prob_screen, product='hpv', label='screen') # Routine screening #0.95
    to_triage   = lambda sim: sim.get_intervention('screen').outcomes['positive'] # Define who's eligible for triage

    # Relfex cytology (perform lbc on the same sample that test positive for HPV)
    # This is done automatically so prob = 1 here
    triage      = hpv.routine_triage(eligibility=to_triage, prob=prob_triage, product='hpv', label='triage') # Triage people
    to_treat    = lambda sim: sim.get_intervention('triage').outcomes['positive'] # Define who's eligible to be assigned treatment


    # This function decides who gets what treatment - not sure what this is based off?
    # Is there a prob distn that shows what the percentage of woman who get what is?
    assign_tx   = hpv.routine_triage(eligibility=to_treat, prob=prob_assign, product='tx_assigner', label='assign_tx') # Assign treatment

    # The people to ablate are the ones that got ablation as the treatment assignment
    to_ablate   = lambda sim: sim.get_intervention('assign_tx').outcomes['ablation'] # Define who's eligible for ablation treatment
    ablation    = hpv.treat_num(eligibility=to_ablate, prob=prob_ablate, product='ablation') # Administer ablation

    # The people to excise are the ones that got excision as the treatment assignment
    to_excise   = lambda sim: sim.get_intervention('assign_tx').outcomes['excision'] # Define who's eligible for excision
    excision    = hpv.treat_delay(eligibility=to_excise, prob=prob_excise, product='excision') # Administer excision
    
    if location == 'nigeria':
    
        ## Apply it to the sim
        sim = make_nigeria_sim(interventions = interventions + [screen, triage, assign_tx, ablation, excision], vax=vax, label = label, **kwargs)
        # If vax = False, then vx =[], so not included in interventions
        # If vax=True, then vx = an intevention, is concatenated with the other interventions
    
    elif location == 'uk':
        
        sim = make_uk_sim(interventions = interventions + [screen, triage, assign_tx, ablation, excision], vax=vax, label = label, **kwargs)
        
    else:
        raise ValueError("Location must be 'uk' or 'nigeria'")
    
    
    return sim


# %%







# %% NIGERIA SCREENING

# All these sims include the vaccination introduced in Oct 2023

orig = make_nigeria_sim(rand_seed = 1, label = 'no screening')

strat1_1 = add_screening(location = 'nigeria', rand_seed = 1, age_range = [18,64], 
                        years = np.arange(2026,2050,2), label = 'Age: 18-64, Interval=2')

strat1_2 = add_screening(location = 'nigeria', rand_seed = 1, age_range = [18,64], 
                        years = np.arange(2026,2050,5),label = 'Age: 18-64, Interval=5')

strat1_3 = add_screening(location = 'nigeria', rand_seed = 1, age_range = [18,64],
                        years = np.arange(2026,2050,10),label = 'Age: 18-64, Interval=10')

# orig.run()
# strat1_1.run()
# strat1_2.run()
# strat1_3.run()

# Compare screening intervals for age range 18-64
comp1 = hpv.MultiSim([orig, strat1_1,strat1_2,strat1_3])
comp1.run()
comp_strat1 = comp1.plot()


# Check the results of the plots
for sim in comp1.sims:
    sim.brief()
    
# Sim("Sim 0"; 1990 to 2050; pop: 10000 default; epi: 1.21454e+09⚙, 1.03663e+06♋︎)
# Sim("Age: 18-64, Interval=2"; 1990 to 2050; pop: 10000 default; epi: 1.16455e+09⚙, 803820♋︎)
# Sim("Age: 18-64, Interval=5"; 1990 to 2050; pop: 10000 default; epi: 1.16341e+09⚙, 809569♋︎)
# Sim("Age: 18-64, Interval=10"; 1990 to 2050; pop: 10000 default; epi: 1.16341e+09⚙, 809569♋︎)
#
# There is a difference between strat1_1 and _2,_3 so know something has changed - tells me something probs wrong with 
# screening or vaccination itself



# save fig to mac. Don't forget .png !
hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/Nigeria/compare n strat 1.png',
            fig = comp_strat1)

# Doesn't seem to be much difference betweem them
# Also changed the intervals in their T5 , and didn't see much difference there either
# Python crashed but you can see this in the image taken on my phone 18/07/25

# Why am I seeing triangluar shapes for cancer incidence per age


# %%

orig = make_nigeria_sim(rand_seed = 1, label = 'no screening')

strat2_1 = add_screening(location = 'nigeria', rand_seed = 1, age_range = [25,64], 
                        years = np.arange(2026,2050,2), label = 'Age: 25-64, Interval=2')

strat2_2 = add_screening(location = 'nigeria', rand_seed = 1, age_range = [25,64],
                        years = np.arange(2026,2050,5),label = 'Age: 25-64, Interval=5')

strat2_3 = add_screening(location = 'nigeria', rand_seed = 1, age_range = [25,64],
                        years = np.arange(2026,2050,10),label = 'Age: 25-64, Interval=10')



# Compare screening intervals for age range 25-64
comp2 = hpv.MultiSim([orig, strat2_1,strat2_2,strat2_3])
comp2.run()
comp_strat2 = comp2.plot()
    
hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/Nigeria/compare n strat 2.png',
            fig = comp_strat2)

# Overall seems slightly worse to start screening at 25 rather than 18
# but also should run multiple sims and take the mean 
# %%
    
orig = make_nigeria_sim(rand_seed = 1, label = 'no screening')

strat3_1 = add_screening(location = 'nigeria', rand_seed = 1, age_range = [25,100], 
                        years = np.arange(2026,2050,2), label = 'Age: 25-100, Interval=2')

strat3_2 = add_screening(location = 'nigeria', rand_seed = 1, age_range = [25,100],
                        years = np.arange(2026,2050,5),label = 'Age: 25-100, Interval=5')

strat3_3 = add_screening(location = 'nigeria', rand_seed = 1, age_range = [25,100],
                        years = np.arange(2026,2050,10),label = 'Age: 25-100, Interval=10')



# Compare screening intervals for age range 25-64
comp3 = hpv.MultiSim([orig, strat3_1,strat3_2,strat3_3])
comp3.run()
comp_strat3 = comp3.plot()
# Weirdly does decrease quite a lot, eventhough life expectancy is Nigeria is 53
# Again should run multiple sims and average them

hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/Nigeria/compare n strat 3.png',
            fig = comp_strat3)


    
# %%
# %%

# Now going to do the same thing but with the vaccination in 2024 removed. 

orig_nv = make_nigeria_sim(rand_seed = 1, vax=False, label = 'no screening, no vax')

strat1_1_nv = add_screening(location = 'nigeria', rand_seed = 1, age_range = [18,64], vax=False,
                        years = np.arange(2026,2050,2), label = 'Age: 18-64, Interval=2, no vax')

strat1_2_nv = add_screening(location = 'nigeria', rand_seed = 1, age_range = [18,64], vax=False,
                        years = np.arange(2026,2050,5),label = 'Age: 18-64, Interval=5, no vax')

strat1_3_nv = add_screening(location = 'nigeria', rand_seed = 1, age_range = [18,64], vax=False,
                        years = np.arange(2026,2050,10),label = 'Age: 18-64, Interval=10, no vax')

# orig.run()
# strat1_1_nv.run()
# strat1_2_nv.run()
# strat1_3_nv.run()

# Compare screening intervals for age range 18-64
comp7 = hpv.MultiSim([orig_nv, strat1_1_nv, strat1_2_nv, strat1_3_nv])
comp7.run()
comp_strat7 = comp7.plot()



# save fig to mac. Don't forget .png !
hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/Nigeria/compare n strat 1 with no vax.png',
            fig = comp_strat7)

# Doesn't seem to be much difference betweem them
# Also changed the intervals in their T5 , and didn't see much difference there either
# Python crashed but you can see this in the image taken on my phone 18/07/25

# Why am I seeing triangluar shapes for cancer incidence per age


# %%

orig_nv = make_nigeria_sim(rand_seed = 1, vax=False, label = 'no screening, no vax')

strat2_1_nv = add_screening(location = 'nigeria', rand_seed = 1, age_range = [25,64], vax=False,
                        years = np.arange(2026,2050,2), label = 'Age: 25-64, Interval=2, no vax')

strat2_2_nv = add_screening(location = 'nigeria', rand_seed = 1, age_range = [25,64],vax=False,
                        years = np.arange(2026,2050,5),label = 'Age: 25-64, Interval=5, no vax')

strat2_3_nv = add_screening(location = 'nigeria', rand_seed = 1, age_range = [25,64],vax=False,
                        years = np.arange(2026,2050,10),label = 'Age: 25-64, Interval=10, no vax')



# Compare screening intervals for age range 25-64
comp8 = hpv.MultiSim([orig_nv, strat2_1_nv, strat2_2_nv, strat2_3_nv])
comp8.run()
comp_strat8 = comp8.plot()
    
hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/Nigeria/compare n strat 2 with no vax.png',
            fig = comp_strat8)

# Overall seems slightly worse to start screening at 25 rather than 18
# but also should run multiple sims and take the mean 
# %%
    
orig_nv = make_nigeria_sim(rand_seed = 1, vax=False, label = 'no screening, no vax')

strat3_1_nv = add_screening(location = 'nigeria', rand_seed = 1, age_range = [25,100], vax=False,
                        years = np.arange(2026,2050,2), label = 'Age: 25-100, Interval=2, no vax')

strat3_2_nv = add_screening(location = 'nigeria', rand_seed = 1, age_range = [25,100],vax=False,
                        years = np.arange(2026,2050,5),label = 'Age: 25-100, Interval=5, no vax')

strat3_3_nv = add_screening(location = 'nigeria', rand_seed = 1, age_range = [25,100],vax=False,
                        years = np.arange(2026,2050,10),label = 'Age: 25-100, Interval=10, no vax')



# Compare screening intervals for age range 25-64
comp9 = hpv.MultiSim([orig_nv, strat3_1_nv,strat3_2_nv,strat3_3_nv])
comp9.run()
comp_strat9 = comp9.plot()
# Weirdly does decrease quite a lot, eventhough life expectancy is Nigeria is 53
# Again should run multiple sims and average them

hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/Nigeria/compare n strat 3 with no vax.png',
            fig = comp_strat9)


# %%
# %%

# Not getting a difference in the sims.. going to compare same interval different ages.

# Compare ages for interval 2
comp4 = hpv.MultiSim([orig, strat1_1, strat2_1, strat3_1])
comp4.run()
comp_strat4 = comp4.plot()
comp4.brief()

hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/Nigeria/compare ages for n interval 2.png',
            fig = comp_strat4)
    
# Compare ages for interval 5
comp5 = hpv.MultiSim([orig, strat1_2, strat2_2, strat3_2])
comp5.run()
comp_strat5 = comp5.plot()

hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/Nigeria/compare ages for n interval 5.png',
            fig = comp_strat5)

# Compare ages for interval 10
comp6 = hpv.MultiSim([orig, strat1_3, strat2_3, strat3_3]) 
comp6.run()
comp_strat6 = comp6.plot()   

hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/Nigeria/compare ages for n interval 10.png',
            fig = comp_strat6)

# %%
# %%

# Now compare the same interval different ages, where the 2023 vaxination is removed

# Compare ages for interval 2, no vax
comp10 = hpv.MultiSim([orig_nv, strat1_1_nv, strat2_1_nv, strat3_1_nv])
comp10.run()
comp_strat10 = comp10.plot()
comp4.brief()
    
hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/Nigeria/compare ages for n interval 2 with no vax.png',
            fig = comp_strat10)

# Compare ages for interval 5, no vax
comp11 = hpv.MultiSim([orig_nv, strat1_2_nv, strat2_2_nv, strat3_2_nv])
comp11.run()
comp_strat11 = comp11.plot()

hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/Nigeria/compare ages for n interval 5 with no vax.png',
            fig = comp_strat11)

# Compare ages for interval 10, no vax
comp12 = hpv.MultiSim([orig_nv, strat1_3_nv, strat2_3_nv, strat3_3_nv]) 
comp12.run()
comp_strat12 = comp12.plot()   

hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/Nigeria/compare ages for n interval 10 with no vax.png',
            fig = comp_strat12)

# %%
# %%

# Compare vax vs no vax with no screening

comp13 = hpv.MultiSim([orig, orig_nv])
comp13.run()
comp_strat13 = comp13.plot()

hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/Nigeria/compare vax vs no vax for n : no screening.png',
            fig = comp_strat13)
# %%
# %%

# Put no vax and vax side by side

# No screening no vax, no screening vax, screening vax, screening no vax 

comp14 = hpv.MultiSim([strat1_1, strat1_1_nv])
comp14.run()
comp_strat14 = comp14.plot()

hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/Nigeria/compare vax vs no vax for n : strat 1_1 : ages 18-64, interval 2.png',
            fig = comp_strat14)

## REALLY IMPORTANT PLOT

# Can see that with screening implemented but no vaccination, you have a higher HPV prevalence, but this doesn't imply increased cancer prevalance
# So in the prescence of screening, whilst the vaccination signigicantly decreases HPV incidence, actually screening with no vaccination is just as good
# as protecting from cancer as screening with vaccination

# This might suggest that it is sufficient to screen for cancer without vaccination in order to reduce cancer incidence
# However this is only if we have correct treatments in place - and this would probably be more costly and time consuming than just 
# vaccination in the first instance

# %%










# %%

# %% UK SCREENING

# All these sims include the vaccination introduced in Oct 2023

orig = make_uk_sim(rand_seed = 1, label = 'no screening')

strat1_1 = add_screening(location = 'uk', rand_seed = 1, age_range = [18,64], 
                        years = np.arange(2026,2050,2), label = 'Age: 18-64, Interval=2')

strat1_2 = add_screening(location = 'uk', rand_seed = 1, age_range = [18,64], 
                        years = np.arange(2026,2050,5),label = 'Age: 18-64, Interval=5')

strat1_3 = add_screening(location = 'uk', rand_seed = 1, age_range = [18,64],
                        years = np.arange(2026,2050,10),label = 'Age: 18-64, Interval=10')

# orig.run()
# strat1_1.run()
# strat1_2.run()
# strat1_3.run()

# Compare screening intervals for age range 18-64
comp1 = hpv.MultiSim([orig, strat1_1,strat1_2,strat1_3])
comp1.run()
comp_strat1 = comp1.plot()


# Check the results of the plots
for sim in comp1.sims:
    sim.brief()
    
# Sim("Sim 0"; 1990 to 2050; pop: 10000 default; epi: 1.21454e+09⚙, 1.03663e+06♋︎)
# Sim("Age: 18-64, Interval=2"; 1990 to 2050; pop: 10000 default; epi: 1.16455e+09⚙, 803820♋︎)
# Sim("Age: 18-64, Interval=5"; 1990 to 2050; pop: 10000 default; epi: 1.16341e+09⚙, 809569♋︎)
# Sim("Age: 18-64, Interval=10"; 1990 to 2050; pop: 10000 default; epi: 1.16341e+09⚙, 809569♋︎)
#
# There is a difference between strat1_1 and _2,_3 so know something has changed - tells me something probs wrong with 
# screening or vaccination itself



# save fig to mac. Don't forget .png !
hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/uk/compare uk strat 1.png',
            fig = comp_strat1)

# Doesn't seem to be much difference betweem them
# Also changed the intervals in their T5 , and didn't see much difference there either
# Python crashed but you can see this in the image taken on my phone 18/07/25

# Why am I seeing triangluar shapes for cancer incidence per age


# %%

orig = make_uk_sim(rand_seed = 1, label = 'no screening')

strat2_1 = add_screening(location = 'uk', rand_seed = 1, age_range = [25,64], 
                        years = np.arange(2026,2050,2), label = 'Age: 25-64, Interval=2')

strat2_2 = add_screening(location = 'uk', rand_seed = 1, age_range = [25,64],
                        years = np.arange(2026,2050,5),label = 'Age: 25-64, Interval=5')

strat2_3 = add_screening(location = 'uk', rand_seed = 1, age_range = [25,64],
                        years = np.arange(2026,2050,10),label = 'Age: 25-64, Interval=10')



# Compare screening intervals for age range 25-64
comp2 = hpv.MultiSim([orig, strat2_1,strat2_2,strat2_3])
comp2.run()
comp_strat2 = comp2.plot()
    
hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/uk/compare uk strat 2.png',
            fig = comp_strat2)

# Overall seems slightly worse to start screening at 25 rather than 18
# but also should run multiple sims and take the mean 
# %%
    
orig = make_uk_sim(rand_seed = 1, label = 'no screening')

strat3_1 = add_screening(location = 'uk', rand_seed = 1, age_range = [25,100], 
                        years = np.arange(2026,2050,2), label = 'Age: 25-100, Interval=2')

strat3_2 = add_screening(location = 'uk', rand_seed = 1, age_range = [25,100],
                        years = np.arange(2026,2050,5),label = 'Age: 25-100, Interval=5')

strat3_3 = add_screening(location = 'uk', rand_seed = 1, age_range = [25,100],
                        years = np.arange(2026,2050,10),label = 'Age: 25-100, Interval=10')



# Compare screening intervals for age range 25-64
comp3 = hpv.MultiSim([orig, strat3_1,strat3_2,strat3_3])
comp3.run()
comp_strat3 = comp3.plot()
# Again should run multiple sims and average them

hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/uk/compare uk strat 3.png',
            fig = comp_strat3)


    
# %%
# %%

# Now going to do the same thing but with all vaccination removed. 

orig_nv = make_uk_sim(rand_seed = 1, vax=False, label = 'no screening, no vax')

strat1_1_nv = add_screening(location = 'uk', rand_seed = 1, age_range = [18,64], vax=False,
                        years = np.arange(2026,2050,2), label = 'Age: 18-64, Interval=2, no vax')

strat1_2_nv = add_screening(location = 'uk', rand_seed = 1, age_range = [18,64], vax=False,
                        years = np.arange(2026,2050,5),label = 'Age: 18-64, Interval=5, no vax')

strat1_3_nv = add_screening(location = 'uk', rand_seed = 1, age_range = [18,64], vax=False,
                        years = np.arange(2026,2050,10),label = 'Age: 18-64, Interval=10, no vax')

# orig.run()
# strat1_1_nv.run()
# strat1_2_nv.run()
# strat1_3_nv.run()

# Compare screening intervals for age range 18-64
comp7 = hpv.MultiSim([orig_nv, strat1_1_nv, strat1_2_nv, strat1_3_nv])
comp7.run()
comp_strat7 = comp7.plot()



# save fig to mac. Don't forget .png !
hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/uk/compare uk strat 1 with no vax.png',
            fig = comp_strat7)

# Doesn't seem to be much difference betweem them
# Also changed the intervals in their T5 , and didn't see much difference there either
# Python crashed but you can see this in the image taken on my phone 18/07/25

# Why am I seeing triangluar shapes for cancer incidence per age


# %%

orig_nv = make_uk_sim(rand_seed = 1, vax=False, label = 'no screening, no vax')

strat2_1_nv = add_screening(location = 'uk', rand_seed = 1, age_range = [25,64], vax=False,
                        years = np.arange(2026,2050,2), label = 'Age: 25-64, Interval=2, no vax')

strat2_2_nv = add_screening(location = 'uk', rand_seed = 1, age_range = [25,64],vax=False,
                        years = np.arange(2026,2050,5),label = 'Age: 25-64, Interval=5, no vax')

strat2_3_nv = add_screening(location = 'uk', rand_seed = 1, age_range = [25,64],vax=False,
                        years = np.arange(2026,2050,10),label = 'Age: 25-64, Interval=10, no vax')



# Compare screening intervals for age range 25-64
comp8 = hpv.MultiSim([orig_nv, strat2_1_nv, strat2_2_nv, strat2_3_nv])
comp8.run()
comp_strat8 = comp8.plot()
    
hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/uk/compare uk strat 2 with no vax.png',
            fig = comp_strat8)

# Overall seems slightly worse to start screening at 25 rather than 18
# but also should run multiple sims and take the mean 
# %%
    
orig_nv = make_uk_sim(rand_seed = 1, vax=False, label = 'no screening, no vax')

strat3_1_nv = add_screening(location = 'uk', rand_seed = 1, age_range = [25,100], vax=False,
                        years = np.arange(2026,2050,2), label = 'Age: 25-100, Interval=2, no vax')

strat3_2_nv = add_screening(location = 'uk', rand_seed = 1, age_range = [25,100],vax=False,
                        years = np.arange(2026,2050,5),label = 'Age: 25-100, Interval=5, no vax')

strat3_3_nv = add_screening(location = 'uk', rand_seed = 1, age_range = [25,100],vax=False,
                        years = np.arange(2026,2050,10),label = 'Age: 25-100, Interval=10, no vax')



# Compare screening intervals for age range 25-64
comp9 = hpv.MultiSim([orig_nv, strat3_1_nv,strat3_2_nv,strat3_3_nv])
comp9.run()
comp_strat9 = comp9.plot()
# Again should run multiple sims and average them

hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/uk/compare uk strat 3 with no vax.png',
            fig = comp_strat9)


# %%
# %%

# Not getting a difference in the sims.. going to compare same interval different ages.

# Compare ages for interval 2
comp4 = hpv.MultiSim([orig, strat1_1, strat2_1, strat3_1])
comp4.run()
comp_strat4 = comp4.plot()
comp4.brief()

hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/uk/compare ages for uk interval 2.png',
            fig = comp_strat4)
    
# Compare ages for interval 5
comp5 = hpv.MultiSim([orig, strat1_2, strat2_2, strat3_2])
comp5.run()
comp_strat5 = comp5.plot()

hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/uk/compare ages for uk interval 5.png',
            fig = comp_strat5)

# Compare ages for interval 10
comp6 = hpv.MultiSim([orig, strat1_3, strat2_3, strat3_3]) 
comp6.run()
comp_strat6 = comp6.plot()   

hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/uk/compare ages for uk interval 10.png',
            fig = comp_strat6)

# %%
# %%

# Now compare the same interval different ages, where the 2023 vaxination is removed

# Compare ages for interval 2, no vax
comp10 = hpv.MultiSim([orig_nv, strat1_1_nv, strat2_1_nv, strat3_1_nv])
comp10.run()
comp_strat10 = comp10.plot()
comp4.brief()
    
hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/uk/compare ages for uk interval 2 with no vax.png',
            fig = comp_strat10)

# Compare ages for interval 5, no vax
comp11 = hpv.MultiSim([orig_nv, strat1_2_nv, strat2_2_nv, strat3_2_nv])
comp11.run()
comp_strat11 = comp11.plot()

hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/uk/compare ages for uk interval 5 with no vax.png',
            fig = comp_strat11)

# Compare ages for interval 10, no vax
comp12 = hpv.MultiSim([orig_nv, strat1_3_nv, strat2_3_nv, strat3_3_nv]) 
comp12.run()
comp_strat12 = comp12.plot()   

hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/uk/compare ages for uk interval 10 with no vax.png',
            fig = comp_strat12)





# %%








# %%  Fabian session - include sanity checks

# orig = make_nigeria_sim(rand_seed = 1)

strat1_1 = add_screening(location = 'nigeria', rand_seed = 1, age_range = [18,64], 
                        years = list(np.arange(2026,2050,2)), label = 'Age: 18-64, Interval=2')

# strat1_2 = add_screening(location = 'nigeria', rand_seed = 1, age_range = [18,64],
#                         years = 
#                         list(np.arange(2026,2050,5)),
#                         label = 'Age: 18-64, Interval=5')

strat1_3 = add_screening(location = 'nigeria', rand_seed = 1, age_range = [18,64],
                        years = list(np.arange(2036,2050,10)),label = 'Age: 18-64, Interval=10')

# strat1_3 = add_screening(location = 'nigeria', rand_seed = 1, age_range = [18,64],
#                         years=[2026,2027,2028], label = 'Age: 18-64, Interval=10')

strat1_3['interventions']

# orig.run()
# strat1_1.run()
# strat1_2.run()
# strat1_3.run()

# Run fine individually but not together?

# Compare screening intervals for age range 18-64
comp = hpv.MultiSim([#orig, 
                     strat1_1,
                     #strat1_2,
                     strat1_3])
comp.run()
comp_strat1 = comp.plot()


# %%






    
# %% SANITY CHECKS
    
#     # # Test if location update works
    
#     # uk = add_screening('uk', [9,14], 'uk')
#     # uk['interventions']
    
#     # czechia = add_screening('czechia', [9,10], 'czechia')
#     # # ValueError: Location must be 'uk' or 'nigeria' 
    
#     # %%
    
#     # Sanity check - for this i put all the probabilites to 1
#     standard_sim = make_nigeria_sim()
#     prob_zero = add_screening(location='nigeria', age_range=[25,64], label = 'prob screen to 0', prob_screen = 0)
#     # Expect these to be the same , but they're not ...
    
#     # At least they're not according to multisim
#     another_sim = make_nigeria_sim()
#     hpv.MultiSim([standard_sim,another_sim]).run().plot()
#     # Okay multisim doesn't assign different seeds to the same sim so that can't be the issue
    
    
    
#     prob_6 = add_screening(location='nigeria', age_range=[25,64], label = 'prob screen to 0.6', prob_screen = 0.6)
#     prob_9 = add_screening(location='nigeria', age_range=[25,64], label = 'prob screen to 0.9', prob_screen = 0.9)
    
#     prob_one =  add_screening(location='nigeria', age_range=[25,64], label = 'prob screen to 1', prob_screen = 1)
    
    
    
    
#     hpv.MultiSim([standard_sim, prob_zero, prob_one, prob_6, prob_9]).run().plot()
#     # Not the same so something wrong here
    
#     print(standard_sim['interventions'])
#     print(prob_zero['interventions'])
    
    
    
#     # %%
    
#     # # Not sure if Oct 2023 vax being handled okay
#     # # Not sure if you can iclude your own inventions on top of this screening strategy
    
    
#     ## Think runs fine
#     test_fn= add_screening(location='nigeria', age_range=[25,64], label ='23 vax')
#     test_fn.run()
#     test_fn.plot()
    
#     # # Excluding the vax works fine|
#     # test_fn2= add_screening(age_range=[25,64], label ='no 23 vax', vax=False)
#     # test_fn2.run()
#     # test_fn2.plot()
    
    
#     # # Compare vacx vs no vax
#     # comp_vx = hpv.MultiSim(([test_fn, test_fn2]))
#     # comp_vx.plot()
#     # # Yes looks like the vaccination is being removed properly
#     # # Now I've made sure vaccination isn't being applied twice it looks like it's working much better
#     # %% check Oct 2023 vaccination isn't being applied twice
    
#     print(test_fn['interventions'])
#     # # [hpv.routine_vx(product=quadrivalent, prob=None, age_range=[9, 14], sex=0, eligibility=None, label=None), 
#     # # Now only showing this vaccination once so that's good
    
    
#     # # Check the vaccination isn't being included in test_fn2
#     # print(test_fn2['interventions'])
#     # # Great is not being included
    
#     # %%
    
    
#     # # Lets check what happens if we only start the screening streategy in 2040
#     # test_fn3= add_screening(age_range=[25,64], label ='23 vax', years = np.arange(2040,2050))
#     # test_fn3.run()
#     # test_fn4= add_screening(age_range=[25,64], label ='no 23 vax', years = np.arange(2040,2050), vax=False)
#     # test_fn4.run()
#     # # These took ages to run but that is expected since we are applying screening every year
    
#     # comp_vx2 = hpv.MultiSim(([test_fn3, test_fn4]))
#     # comp_vx2.plot()
#     # # Producing a lot of code. I think this whole script, Maybe because it used the function that
#     # # is defined in this script, so it imports the whole script? But then why wouldn't it do that for 
#     # # the other functions?
    
#     # # Regardless, looks like it's working fine so happpy with this. 
    
#     # ## The screening strategy looks like it's doing a lot !!
    
#     # %% Final test is to compare what happens when you remove the vaccination for 2 sims
    
#     # # One of them has screeing starting in 2024, the other has no screening
#     # # Hope to see they look the same until 2024
    
#     # novx_nosc = make_nigeria_sim(vax=False)
#     # novx_sc= add_screening(vax=False, age_range=[25,64], label ='23 vax', years = np.arange(2040,2050))
    
#     # mult = hpv.MultiSim([novx_nosc,novx_sc])
#     # mult.run()
#     # mult.plot()
    
#     # # Okay yes passed the test!
#     # # Is running the whole script for some reason. Wonder| what would happen if I commented other secions out. 
#     # # would it just run this section twice?
    
#     # # Weirdly just runs it once. Anywho, it's running fine. 
    
    
#     # %% Check that kwargs are passed to make_nigeria_sim
    
#     # orig = add_screening(age_range=[25,64], label ='Check kwargs',years = np.arange(2040,2050))
#     # orig.run()
#     # orig.plot()
    
#     # rand = add_screening(rand_seed=2, age_range=[25,64], label ='Check kwargs',years = np.arange(2040,2050))
#     # rand.run()
#     # rand.plot()
    
#     # # # Very weirdly shaped cancers by age...
#     # # Think fine actualy. Think it's just picking pup on screening stopping at 64
    
#     # base=hpv.Sim()
#     # base.run()
#     # base.plot() # Just seeing what it normally looks like
    
#     # %% Haven't tried changing intervals
    
#     # base_sim = make_nigeria_sim()
#     # sim_int1 = sim_int2 = add_screening(age_range=[9,14], years=np.arange(2026,2050) , label ='Screen every year')
#     # sim_int2 = add_screening(age_range=[9,14], years=np.arange(2026,2050,2), label ='Screen every 2 years')
#     # sim_int5 = add_screening(age_range=[9,14], years=np.arange(2026,2050,5), label ='Screen every 5 years')
    
#     # base_sim.run()
#     # sim_int1.run() 
#     # sim_int2.run()
#     # sim_int5.run()
#     # # Okay this works
    
# %%


# # Test location prob update works

# uk = add_screening(location = 'uk', rand_seed = 1, age_range = [18,64], 
#                         years = np.arange(2026,2050,2), label = 'Age: 18-64, Interval=2')

# uk['interventions'] # excise prob = 0.14

# nigeria = add_screening(location = 'nigeria', rand_seed = 1, age_range = [18,64], 
#                         years = np.arange(2026,2050,2), label = 'Age: 18-64, Interval=2')

# nigeria['interventions'] # excise prob = 0.87

# # Check can override

# uk_ep = add_screening(location = 'uk', rand_seed = 1, age_range = [18,64], 
#                         years = np.arange(2026,2050,2), label = 'Age: 18-64, Interval=2',
#                         prob_excise=0.5)

# uk_ep['interventions'] # excise prob = 0.5

# # Great this works


