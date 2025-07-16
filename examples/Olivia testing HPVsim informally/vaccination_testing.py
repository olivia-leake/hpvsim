#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 12:49:48 2025

@author: olivialeake
"""

## Testing adding in the prophlyactic vaccination introdcued in Oct 2023 for 9-14 year olds

import hpvsim as hpv



# vx = hpv.routine_vx(prob=prob, start_year=2015, age_range=[9,10], product='bivalent')


# # Create the sim with and without interventions
# orig_sim = hpv.Sim(pars, label='Baseline')
# sim = hpv.Sim(pars, interventions = vx, label='With vaccination')

# # Run and plot
# msim = hpv.parallel(orig_sim, sim)
# msim.plot();




from hpvsim.Nigeria_screening.Nigeria_calibrated_sim_new import Nigeria_sim

print(Nigeria_sim.pars)
