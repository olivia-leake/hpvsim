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

from Nigeria_screening.Nigeria_sim_fn import make_nigeria_sim


# Make the sim that will calibrate to data. 
# This only works when vax =False  ?????
sim = make_nigeria_sim(vax=False)

# Note this sim DOES contain genotype parameters, beta parameters and f/m_cross layer already - all pars we want
# to calibrate. This doesn't matter, as calib uses the best pars specified here anyways as first guess

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
    total_trials=5000, n_workers=4
)

calib.calibrate(die=True)


calib.plot(res_to_plot=4);


# %%
best_pars = calib.trial_pars_to_sim_pars()
print(best_pars)
