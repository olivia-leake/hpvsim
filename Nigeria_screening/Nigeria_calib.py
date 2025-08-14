#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 12:36:15 2025

@author: olivialeake
"""

# TODO : Change number of trails back to 5000

import sys
import os
import numpy as np
import sciris as sc
sys.path.append('/Users/olivialeake/Documents/BSP project/HPV Project/hpvsim')

import hpvsim as hpv

from Nigeria_screening.Nigeria_sim_fn import make_nigeria_sim


# Make the sim that will calibrate to data. 
# This only works when vax =False  ????? Doesn't matter for nigeria as data is before vaccination
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
# NOte that results_to_plot = [] works as well.. not sure in the point of this

# %%

# Create the calibration object, run it, and plot the results
calib = hpv.Calibration(
    sim,
    calib_pars=calib_pars,
    genotype_pars=genotype_pars,
    extra_sim_result_keys=results_to_plot,
    datafiles=datafiles,
    total_trials=5, n_workers=3
)

calib.calibrate(die=False)


calib.plot();
# What does res to plot do? - number of results to plot. if None, plot them all
# Surely we want them all
# calib.plot(res_to_plot=1) #single best result is plotted alongside the data - according to Fabian at least


# %%
best_pars = calib.trial_pars_to_sim_pars()
print(best_pars)


# {'genotype_pars': #0. 'hpv16':
#     #0. 'dur_precin': {'dist': 'lognormal', 'par1': 3, 'par2': 9}
#     #1. 'cin_fn':     {'form': 'logf2', 'k': 0.3273872197367011, 'x_infl': 0,
#     'ttc': 50}
#     #2. 'dur_cin':    {'dist': 'lognormal', 'par1': 9.305958327050217, 'par2':
#     20}
#     #3. 'cancer_fn':  {'method': 'cin_integral', 'transform_prob': 0.002}
#     #4. 'rel_beta':   1.0
#     #5. 'sero_prob':  0.75
# #1. 'hpv18':
#     #0. 'dur_precin': {'dist': 'lognormal', 'par1': 2.5, 'par2': 9}
#     #1. 'dur_cin':    {'dist': 'lognormal', 'par1': 4.422936044382016, 'par2':
#     20}
#     #2. 'cin_fn':     {'form': 'logf2', 'k': 0.2790805197830855, 'x_infl': 0,
#     'ttc': 50}
#     #3. 'cancer_fn':  {'method': 'cin_integral', 'transform_prob': 0.002}
#     #4. 'rel_beta':   0.75
#     #5. 'sero_prob':  0.56
# #2. 'hi5':
#     #0. 'dur_precin': {'dist': 'lognormal', 'par1': 2.5, 'par2': 9}
#     #1. 'dur_cin':    {'dist': 'lognormal', 'par1': 4.5, 'par2': 20}
#     #2. 'cin_fn':     {'form': 'logf2', 'k': 0.2, 'x_infl': 0, 'ttc': 50}
#     #3. 'cancer_fn':  {'method': 'cin_integral', 'transform_prob': 0.0015}
#     #4. 'rel_beta':   0.9
#     #5. 'sero_prob':  0.6, 'hiv_pars': {'cd4states': ['lt200', 'gt200'], 'cd4statesfull': ['CD4<200', '200<CD4<500'], 'cd4_lb': [0, 200], 'cd4_ub': [200, 500], 'rel_sus': {'lt200': 2.2, 'gt200': 2.2}, 'rel_sev': {'lt200': 1.5, 'gt200': 1.2}, 'rel_imm': {'lt200': 0.36, 'gt200': 0.76}, 'rel_reactivation_prob': 3, 'model_hiv_death': True, 'time_to_hiv_death_shape': 2, 'time_to_hiv_death_scale': <function HIVsim.__init__.<locals>.<lambda> at 0x127aa5ab0>, 'hiv_death_adj': 1, 'cd4_start': {'dist': 'normal', 'par1': 594, 'par2': 20}, 'cd4_trajectory': <function HIVsim.__init__.<locals>.<lambda> at 0x141c93d00>, 'cd4_reconstitution': <function HIVsim.__init__.<locals>.<lambda> at 0x141c905e0>, 'art_failure_prob': 0.0, 'dt_art': 1.0}, 'beta': 0.03167112974082747, 'f_cross_layer': 0.14009651580765883, 'm_cross_layer': 0.04608416890111761}
    
    
    
    
    
    
    
    