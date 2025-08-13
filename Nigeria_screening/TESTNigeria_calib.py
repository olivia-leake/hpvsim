#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 12:36:15 2025

@author: olivialeake
"""

import sys
import os
import numpy as np
import sciris as sc
sys.path.append('/Users/olivialeake/Documents/BSP project/HPV Project/hpvsim')

import hpvsim as hpv

# Going to make the sim from scratch rather than using the function to see if can figure out why the calibration doesn't work when vaccincations are included - indeed,
# for Nigeria it doesn't actually matter as the strategy was added in 2024, and the data is for 2020, so it is fine to stop running the sim at 2021 and not include the vaccination
# it will however be a problem when I deal with the England case. 

# Actually will just do it using the standard sim to simplify

years=np.arange(2020,2025)
# array([2020, 2021, 2022, 2023, 2024])


vx = [hpv.routine_vx(prob=0.9, start_year = 2024, end_year=2050, years=None, age_range=[9,14], product='quadrivalent')]

vx2 = [hpv.routine_vx(prob=0.9, start_year=2020, end_year=2024, years=np.arange(2020,2025), age_range=[9,14], product='quadrivalent')]

vx3 = [hpv.routine_vx(prob=0.9, start_year=None, end_year=None, years=np.arange(2020,2025), age_range=[9,14], product='quadrivalent')]

sim=hpv.Sim(interventions = vx2, end =2050)
sim.run()

print(sim['interventions'])


# [best,lower,upper]
calib_pars = dict(
        beta=[0.05, 0.010, 0.20],
        f_cross_layer = [0.05, 0, 0.20], # Why chosen these?
        m_cross_layer = [0.15,0,0.30] # Why chosen these?
        
    )

genotype_pars = dict(
    hpv16=dict(
        cin_fn=dict(k=[0.5, 0.2, 1.0]),
        dur_cin=dict(par1=[6, 4, 12])
    ),
    hpv18=dict(
        cin_fn=dict(k=[0.5, 0.2, 1.0]),
        dur_cin=dict(par1=[6, 4, 12])
    )
)



# List the datafiles that contain data that we wish to compare the model to:
datafiles=['/Users/olivialeake/Documents/BSP project/HPV Project/hpvsim/docs/tutorials/nigeria_cancer_cases.csv',
           '/Users/olivialeake/Documents/BSP project/HPV Project/hpvsim/docs/tutorials/nigeria_cancer_types.csv']

results_to_plot = ['cancer_incidence', 'asr_cancer_incidence']

# %%

# Create the calibration object, run it, and plot the results
calib = hpv.Calibration(
    sim,
    calib_pars=calib_pars,
    genotype_pars=genotype_pars,
    extra_sim_result_keys=results_to_plot,
    datafiles=datafiles,
    total_trials=2, n_workers=1
)

calib.calibrate(die=False)


calib.plot(res_to_plot=4);


# %%
best_pars = calib.trial_pars_to_sim_pars()
print(best_pars)
