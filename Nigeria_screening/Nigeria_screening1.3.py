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

# All these sims include the vaccination introduced in Oct 2023

orig = make_nigeria_sim(rand_seed = 1)

strat1_1 = add_screening(rand_seed = 1, age_range = [18,64], 
                        years = np.arange(2026,2050,2), label = 'Age: 18-64, Interval=2')

strat1_2 = add_screening(rand_seed = 1, age_range = [18,64],
                        years = np.arange(2026,2050,5),label = 'Age: 18-64, Interval=5')

strat1_3 = add_screening(rand_seed = 1, age_range = [18,64],
                        years = np.arange(2026,2050,10),label = 'Age: 18-64, Interval=10')



# Compare screening intervals for age range 18-64
comp = hpv.MultiSim([orig, strat1_1,strat1_2,strat1_3])
comp.run()
comp.plot()
