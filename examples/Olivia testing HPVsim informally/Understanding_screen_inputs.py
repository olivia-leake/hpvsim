#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 11:10:29 2025

@author: olivialeake
"""

## Need to access the function made in Nigeria_screening
import sys
import os
import sciris as sc
import numpy as np
sys.path.append("/Users/olivialeake/Library/CloudStorage/OneDrive-Nexus365/Part B/BSP project/HPV Project/hpvsim")


from Nigeria_screening.Nigeria_sim_fn import make_nigeria_sim
from Nigeria_screening.Nig_screen_fn import add_screening

import hpvsim as hpv

 = make_nigeria_sim(rand_seed = 1)

strat1 = add_screening(rand_seed = 1, age_range = [25,64], label = '1st strategy')
strat2 = add_screening(rand_seed = 1, age_range = [25,64], label = '2nd strategy')


# How do I change the frequency of screening?
# Right now I think it's yearly

# check defaults

# From interventions.py can see the timepoints at which the intervention will be applied

# self.start_point    = sc.findinds(sim.yearvec, self.start_year)[0]
# self.end_point      = sc.findinds(sim.yearvec, self.end_year)[0] + adj_factor
# self.years          = sc.inclusiverange(self.start_year, self.end_year)
# self.timepoints     = sc.inclusiverange(self.start_point, self.end_point)
# self.yearvec        = np.arange(self.start_year, self.end_year+adj_factor, sim['dt'])

# Okay I think if you set years=yearvec you are saying every time you update the 
# simlation, you add the interventions. ie: 2026, 2026.25, 2026.5, ..
# But I want 2026, 2028, ....



# def __init__(self, years=None, start_year=None, end_year=None, prob=None, annual_prob=True):
#     self.years      = years
#     self.start_year = start_year
#     self.end_year   = end_year
#     self.prob       = sc.promotetoarray(prob)
#     self.annual_prob = annual_prob # Determines whether the probability is annual or per timestep
#     return    

# Rather than supplying start year it is porbably better to supply an array


# apply the screening strategy every 2 years
years= np.arange(start = 2026,stop =2050, step= 2)

# %%

a1 = np.arange(0,5,1)
print(a1) # [0 1 2 3 4]

a2 = np.arange(0,5)
print(a2) # [0 1 2 3 4]

# Okay so the default is time step = 1

