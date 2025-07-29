#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 12:49:48 2025

@author: olivialeake
"""
## Didn't like have to make a deep copy so don't use this
## Created a Nigeria sim function instead


## Need to access the simulation made in Nigeria_screening
import sys
import os
import sciris as sc
sys.path.append("/Users/olivialeake/Library/CloudStorage/OneDrive-Nexus365/Part B/BSP project/HPV Project/hpvsim")


from Nigeria_screening.Nigeria_calibrated_sim_new import Nigeria_sim
import hpvsim as hpv

print(Nigeria_sim.pars) # Check everything has been imported properly


# Try running the sim
Nigeria_sim.run() # works

# %%

## Testing adding in the routine prophlyactic vaccination introdcued in Oct 2023 for 9-14 year olds
# according to google they have quadrivalent vaccination (testing on random sim first)


vx = hpv.routine_vx(prob=0.9, start_year=2000, age_range=[8,14], product='quadrivalent')
# vaccinate 90% of girls aged 9 to 14 every year starting from 2023 


# Create the sim with and without interventions

# Can you add intervention after creating the sim?
# Yes! 
# Create a deep copy of the original, then update certain pars

# Alternatively you would need to create a whole new sim with the old parameters which
# I think is risky in case you mess something up

orig_sim = hpv.Sim(label='no vax')

new_sim = sc.dcp(orig_sim) # dcp is a sciris module which creates a fully independent copy
# of the old sim so that changes to the new one doesn't effect the old one


new_sim['label'] ='vax'
new_sim.label ='vax'

new_sim['interventions'] =vx
new_sim.interventions =vx


print(new_sim.pars)




new_sim['interventions'] = [vx]

# Check it's worked
print(orig_sim.label) # no vax
print(new_sim.label)  # vax

# Re-initialize before running to apply the new intervention
new_sim.initialize()

print(new_sim.interventions[0])

# Run and plot
msim = hpv.parallel(orig_sim, new_sim)
msim.plot();

# %%

# Different method
diff_meth = hpv.Sim(interventions = [vx])

print(diff_meth['interventions'])



# %%
# Note this doesn't work, show label is interbentio specific apparenlty
test_sim = hpv.Sim(label='test', show_label = True)
test_sim.run()
test_sim.plot()

test_vx = hpv.routine_vx(label ='label', show_label=True, prob=0.9, start_year=2000, age_range=[8,14], product='quadrivalent')

test2_sim = hpv.Sim(interventions = test_vx)
test2_sim.run()
test2_sim.plot()
# NO label is shown..? Maybe show label only works for multisims?

