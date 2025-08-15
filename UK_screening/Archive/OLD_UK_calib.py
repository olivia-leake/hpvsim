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

import hpvsim as hpv

# Discovered can calibtrate fine, but cannot plot

sim = hpv.Sim(end = 2050) # TOD: update using a UK sim


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




# Nigeria data
datafiles=['/Users/olivialeake/Documents/BSP project/HPV Project/hpvsim/docs/tutorials/nigeria_cancer_cases.csv',
           '/Users/olivialeake/Documents/BSP project/HPV Project/hpvsim/docs/tutorials/nigeria_cancer_types.csv']
# WORKS FINE

# Tested putting UK data into the Nigeria data and this works fine, so problem is to do with column names - could have exta space for e
datafiles=['/Users/olivialeake/Documents/BSP project/HPV Project/UK data/csv_files/TESTnigeria_cancer_cases.csv',
           '/Users/olivialeake/Documents/BSP project/HPV Project/UK data/csv_files/TESTnigeria_cancer_types.csv',
           # '/Users/olivialeake/Documents/BSP project/HPV Project/UK data/csv_files/cancer_deaths.csv']
           '/Users/olivialeake/Documents/BSP project/HPV Project/UK data/csv_files/edited_cancer_deaths.csv']
           
           # however weirdly does not work with the deaths now




# UK data
# List the datafiles that contain data that we wish to compare the model to:
datafiles=['/Users/olivialeake/Documents/BSP project/HPV Project/UK data/csv_files/edited_genotype_distrib_cancer.csv',
           '/Users/olivialeake/Documents/BSP project/HPV Project/UK data/csv_files/edited_new_cervical_cancer_cases.csv',]
           
           #'/Users/olivialeake/Documents/BSP project/HPV Project/UK data/csv_files/cancer_deaths.csv']

# Deaths works stand alone, and deaths works with UK cancer types and UK cancer cases
# UK cancer cases works stand alone
# UK cancer types works stand alone
# BUT UK cancer types and cases produces erroer : x and y must be the same



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

calib.calibrate(die=True)


calib.plot();
# %%
best_pars = calib.trial_pars_to_sim_pars()
print(best_pars)





# %%

# could be to do with the plotting itself then ?
# Try nigeria cases and types adding in uk deaths

datafiles=[#'/Users/olivialeake/Documents/BSP project/HPV Project/hpvsim/docs/tutorials/nigeria_cancer_cases.csv',
           '/Users/olivialeake/Documents/BSP project/HPV Project/hpvsim/docs/tutorials/nigeria_cancer_types.csv',
           '/Users/olivialeake/Documents/BSP project/HPV Project/UK data/csv_files/cancer_deaths.csv']

# Again got this error - however, did see 3 pltos produced, but 2 were empty
# Nigeria deaths works with UK cases
# Nigeria deaths doesn't work with UK types 



# %%


# Test Uk genotype, Nig cancer cases
datafiles=['/Users/olivialeake/Documents/BSP project/HPV Project/UK data/csv_files/genotype_distrib_cancer.csv',
           '/Users/olivialeake/Documents/BSP project/HPV Project/hpvsim/docs/tutorials/nigeria_cancer_cases.csv'] 
# ERROR: x and y must be the same


# Test Nig genotype, UK cancer cases
datafiles = ['/Users/olivialeake/Documents/BSP project/HPV Project/hpvsim/docs/tutorials/nigeria_cancer_types.csv',
             '/Users/olivialeake/Documents/BSP project/HPV Project/UK data/csv_files/new_cervical_cancer_cases.csv']
# ERROR : x and y must be the same


