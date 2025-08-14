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
sys.path.append('/Users/olivialeake/Documents/BSP project/HPV Project/hpvsim')


from Nigeria_screening.Nigeria_sim_fn import make_nigeria_sim
from Nigeria_screening.Nig_screen_fn import add_screening

import hpvsim as hpv

# All these sims include the vaccination introduced in Oct 2|023

orig = make_nigeria_sim(rand_seed = 1)

strat1_1 = add_screening(rand_seed = 1, age_range = [18,64], 
                        years = np.arange(2026,2050,2), label = 'Age: 18-64, Interval=2')

strat1_2 = add_screening(rand_seed = 1, age_range = [18,64],
                        years = np.arange(2026,2050,5),label = 'Age: 18-64, Interval=5')

strat1_3 = add_screening(rand_seed = 1, age_range = [18,64],
                        years = np.arange(2026,2050,10),label = 'Age: 18-64, Interval=10')


# Compare screening intervals for age range 18-64
comp = hpv.MultiSim([orig, strat1_1,strat1_2,strat1_3])
comp.run(n_run=2, die=False)
comp_strat1 = comp.plot()


# Check the results of the plots
for sim in comp.sims:
    sim.brief()
    
# Sim("Sim 0"; 1990 to 2050; pop: 10000 default; epi: 1.21454e+09⚙, 1.03663e+06♋︎)
# Sim("Age: 18-64, Interval=2"; 1990 to 2050; pop: 10000 default; epi: 1.16455e+09⚙, 803820♋︎)
# Sim("Age: 18-64, Interval=5"; 1990 to 2050; pop: 10000 default; epi: 1.16341e+09⚙, 809569♋︎)
# Sim("Age: 18-64, Interval=10"; 1990 to 2050; pop: 10000 default; epi: 1.16341e+09⚙, 809569♋︎)
#
# There is a difference between strat1_1 and _2,_3 so know something has changed - tells me something probs wrong with 
# screening or vaccination itself



# save fig to mac. Don't forget .png !
hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/Nigeria/compare strat 1.png',
            fig = comp_strat1)

# Doesn't seem to be much difference betweem them
# Also changed the intervals in their T5 , and didn't see much difference there either
# Python crashed but you can see this in the image taken on my phone 18/07/25

# Why am I seeing triangluar shapes for cancer incidence per age


# %%

orig = make_nigeria_sim(rand_seed = 1)

strat2_1 = add_screening(rand_seed = 1, age_range = [25,64], 
                        years = np.arange(2026,2050,2), label = 'Age: 25-64, Interval=2')

strat2_2 = add_screening(rand_seed = 1, age_range = [25,64],
                        years = np.arange(2026,2050,5),label = 'Age: 25-64, Interval=5')

strat2_3 = add_screening(rand_seed = 1, age_range = [25,64],
                        years = np.arange(2026,2050,10),label = 'Age: 25-64, Interval=10')



# Compare screening intervals for age range 25-64
comp2 = hpv.MultiSim([orig, strat2_1,strat2_2,strat2_3])
comp2.run()
comp_strat2 = comp2.plot()
    
hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/Nigeria/compare strat 2.png',
            fig = comp_strat2)

# Overall seems slightly worse to start screening at 25 rather than 18
# but also should run multiple sims and take the mean 
# %%
    
orig = make_nigeria_sim(rand_seed = 1)

strat3_1 = add_screening(rand_seed = 1, age_range = [25,100], 
                        years = np.arange(2026,2050,2), label = 'Age: 25-100, Interval=2')

strat3_2 = add_screening(rand_seed = 1, age_range = [25,100],
                        years = np.arange(2026,2050,5),label = 'Age: 25-100, Interval=5')

strat3_3 = add_screening(rand_seed = 1, age_range = [25,100],
                        years = np.arange(2026,2050,10),label = 'Age: 25-100, Interval=10')



# Compare screening intervals for age range 25-64
comp3 = hpv.MultiSim([orig, strat3_1,strat3_2,strat3_3])
comp3.run()
comp_strat3 = comp3.plot()
# Weirdly does decrease quite a lot, eventhough life expectancy is Nigeria is 53
# Again should run multiple sims and average them

hpv.savefig('/Users/olivialeake/Documents/BSP project/HPV Project/Overleaf material/My plots/Nigeria/compare strat 3.png',
            fig = comp_strat3)


# %%

# Not getting a difference in the sims.. going to compare same interval different ages. Which need to do anyways actually 

# Compare ages for interval 2
comp4 = hpv.MultiSim([orig, strat1_1, strat2_1, strat3_1])
comp4.run(n_run=5)
comp_strat4 = comp4.plot()
comp4.brief()
    
# Compare ages for interval 5
comp5 = hpv.MultiSim([orig, strat1_2, strat2_2, strat3_2])
comp5.run()
comp_strat5 = comp5.plot()

# Compare ages for interval 10
comp6 = hpv.MultiSim([orig, strat1_3, strat2_3, strat3_3]) 
comp6.run()
comp_strat6 = comp6.plot()   
    
    