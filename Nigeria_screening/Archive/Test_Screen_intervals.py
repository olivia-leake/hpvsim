#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 16:42:59 2025

@author: olivialeake
"""

# Testing changing intervals

# Sanity check for more simple sim

import hpvsim as hpv
import pandas as pd
import numpy as np

prob = 0.6

# %%
screen1      = hpv.routine_screening(age_range = [18,64], 
                        years = np.arange(2026,2100,2),
                        prob=prob, product='via', label='screen1') # Routine screening

to_triage1   = lambda sim: sim.get_intervention('screen1').outcomes['positive'] # Define who's eligible for triage

triage1      = hpv.routine_triage(eligibility=to_triage1, prob=prob, product='hpv', label='triage1') # Triage people
to_treat1    = lambda sim: sim.get_intervention('triage1').outcomes['positive'] # Define who's eligible to be assigned treatment
assign_tx1   = hpv.routine_triage(eligibility=to_treat1, prob=prob, product='tx_assigner', label='assign_tx1') # Assign treatment
to_ablate1   = lambda sim: sim.get_intervention('assign_tx1').outcomes['ablation'] # Define who's eligible for ablation treatment
ablation1    = hpv.treat_num(eligibility=to_ablate1, prob=prob, product='ablation') # Administer ablation
to_excise1   = lambda sim: sim.get_intervention('assign_tx1').outcomes['excision'] # Define who's eligible for excision
excision1    = hpv.treat_delay(eligibility=to_excise1, prob=prob, product='excision') # Administer excision

s1 = hpv.Sim(interventions = [screen1, triage1, assign_tx1, ablation1, excision1], label='s1', end=2100)

# %%
screen2      = hpv.routine_screening(age_range = [18,64], 
                        years = np.arange(2026,2100,5),
                        prob=prob, product='via', label='screen2') # Routine screening


to_triage2   = lambda sim: sim.get_intervention('screen2').outcomes['positive'] # Define who's eligible for triage
triage2      = hpv.routine_triage(eligibility=to_triage2, prob=prob, product='hpv', label='triage2') # Triage people
to_treat2    = lambda sim: sim.get_intervention('triage2').outcomes['positive'] # Define who's eligible to be assigned treatment
assign_tx2   = hpv.routine_triage(eligibility=to_treat2, prob=prob, product='tx_assigner', label='assign_tx2') # Assign treatment
to_ablate2   = lambda sim: sim.get_intervention('assign_tx2').outcomes['ablation'] # Define who's eligible for ablation treatment
ablation2    = hpv.treat_num(eligibility=to_ablate2, prob=prob, product='ablation') # Administer ablation
to_excise2   = lambda sim: sim.get_intervention('assign_tx2').outcomes['excision'] # Define who's eligible for excision
excision2    = hpv.treat_delay(eligibility=to_excise2, prob=prob, product='excision') # Administer excision

s2 = hpv.Sim(interventions = [screen2, triage2, assign_tx2, ablation2, excision2], label='s2', end=2100)


# %%

screen3      = hpv.routine_screening(age_range = [18,64], 
                        years = np.arange(2026,2100,10),
                        prob=prob, product='via', label='screen3') # Routine screening

to_triage3   = lambda sim: sim.get_intervention('screen3').outcomes['positive'] # Define who's eligible for triage
triage3      = hpv.routine_triage(eligibility=to_triage3, prob=prob, product='hpv', label='triage3') # Triage people
to_treat3    = lambda sim: sim.get_intervention('triage3').outcomes['positive'] # Define who's eligible to be assigned treatment
assign_tx3   = hpv.routine_triage(eligibility=to_treat3, prob=prob, product='tx_assigner', label='assign_tx3') # Assign treatment
to_ablate3   = lambda sim: sim.get_intervention('assign_tx3').outcomes['ablation'] # Define who's eligible for ablation treatment
ablation3    = hpv.treat_num(eligibility=to_ablate3, prob=prob, product='ablation') # Administer ablation
to_excise3   = lambda sim: sim.get_intervention('assign_tx3').outcomes['excision'] # Define who's eligible for excision
excision3    = hpv.treat_delay(eligibility=to_excise3, prob=prob, product='excision') # Administer excision

s3 = hpv.Sim(interventions = [screen3, triage3, assign_tx3, ablation3, excision3], label='s3', end=2100)

# %%
# s1.run()
# s2.run()
# s3.run()

multi = hpv.MultiSim([s1,s2,s3])

multi.run()
multi.plot()




