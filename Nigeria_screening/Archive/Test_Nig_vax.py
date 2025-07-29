#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 10:53:49 2025

@author: olivialeake
"""


## Testing Nigeria vaccination using the Nigeria sim function

# Need access to the function created

## Need to access the simulation made in Nigeria_screening
import sys
import os
import sciris as sc

sys.path.append('/Users/olivialeake/Documents/BSP project/HPV Project/hpvsim')


from Nigeria_screening.Nigeria_sim_fn import make_nigeria_sim

import hpvsim as hpv

# Works alone
sim1 = make_nigeria_sim(label = 'no vax 9 to 10, vax 9 to 14')
sim1.run()
sim1.plot()

# Works changing random seed
sim2 = make_nigeria_sim(rand_seed = 2)
sim2.run()
sim2.plot()

# Accepts keyword args
sim3 = make_nigeria_sim(location = 'india')
sim3.run()
sim3.plot()
sim3['location'] # india


# Accepts interventions
vx1 = hpv.routine_vx(prob=0.6, start_year=2015, age_range=[9,10], product='bivalent')
sim4 = make_nigeria_sim(interventions = [vx1], label = 'vax 9 to 10 and vax 9 to 14')
sim4.run()
sim4.plot()
sim4['interventions'] 
# Out[134]: 
# [hpv.routine_vx(product=quadrivalent, prob=None, age_range=[9, 14], sex=0, eligibility=None, label=None),
#  hpv.routine_vx(product=bivalent, prob=None, age_range=[9, 10], sex=0, eligibility=None, label=None)]
# Not sure why prob = None
# That said, if you compare it to Sim1, cancer incidence per age is the same up to 2015,
# and declines after that, therefore am sure that it is being applied
print(type(sim4['interventions'])) # list, not a dictionary, so can't call elements by name
sim4['interventions'][0]

# Lets you remove the vax
sim5 = make_nigeria_sim(vax=False)
sim5.run()
sim5.plot()



# Plot comparison 
# msim.plot(sim1, sim4) # note this doesn't work because it only works if you used
# multisim to create the plots in the first place

# You don't need to run them again, but you do have to create a multisim in order
# to compare them

msim = hpv.MultiSim([sim1,sim4])

msim.plot()

# Now let's compare both sim1 and sim4 to themselves but with the vax in 2024 removed
# sim1 no vax
sim1_nv =make_nigeria_sim(vax=False, label = 'no vax at all')
sim1_nv.run()
sim4_nv = make_nigeria_sim(vax=False, interventions = [vx1], label = 'vax 9 to 10 and no vax 9 to 14')
sim4_nv.run()

msim_comp = hpv.MultiSim([sim1, sim1_nv, sim4, sim4_nv]) # I forgot to put the sims as a list and it didn't work !
msim_comp.plot()

# I think the issue is when I put vax = False, I can't then override it. It's not adding vx1
# But then why are sim1 and sim4 not being plot?