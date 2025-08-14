#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 15:18:43 2025

@author: olivialeake
"""

import sys
import os
import numpy as np
import sciris as sc
sys.path.append('/Users/olivialeake/Documents/BSP project/HPV Project/hpvsim')

from UK_screening.UK_sim_fn import make_uk_sim
import hpvsim as hpv

# Discovered can calibtrate fine, but cannot plot

sim = make_uk_sim() # TODO: update using a UK sim

# TODO: get it to work with interventions included

# %%
# Test with simpler sim 

sim =hpv.Sim()

vx = [hpv.routine_vx(prob=0.9, start_year = 2001, end_year=2050, age_range=[9,14], product='quadrivalent')]

sim=hpv.Sim(interventions = vx, end =2050)

# %%


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
# %%


# UK data
# List the datafiles that contain data that we wish to compare the model to:
datafiles=['/Users/olivialeake/Documents/BSP project/HPV Project/UK data/csv_files/new_cervical_cancer_cases.csv',
           '/Users/olivialeake/Documents/BSP project/HPV Project/UK data/csv_files/cancer_deaths.csv',
           '/Users/olivialeake/Documents/BSP project/HPV Project/UK data/csv_files/genotype_distrib_cancer.csv']


results_to_plot = ['cancer_incidence', 'asr_cancer_incidence']

# %%

# Create the calibration object, run it, and plot the results
calib = hpv.Calibration(
    sim,
    calib_pars=calib_pars,
    genotype_pars=genotype_pars,
    extra_sim_result_keys=results_to_plot,
    datafiles=datafiles,
    total_trials=10, n_workers=3
)

calib.calibrate(die=False)


calib.plot();
# %%
best_pars = calib.trial_pars_to_sim_pars()
print(best_pars)



