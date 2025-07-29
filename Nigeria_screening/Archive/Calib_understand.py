#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 11:23:06 2025

@author: olivialeake
"""

"""
Checking if the sexual network parameters have an effect on the calibration. Result was yes, they do.
This makes sense when looking at the calibration process ! Optuna suggests parameters, then with the fixed parameters
you input, a simulation is ran, then a goodness of fit test is done comparing the simulation outputs with the data inputs
"""

import hpvsim as hpv

# Configure a simulation with some parameters
pars = dict(location='nigeria',verbose=0) # base test
sim = hpv.Sim(pars)

# Specify some parameters to adjust during calibration.
# The parameters in the calib_pars dictionary don't vary by genotype,
# whereas those in the genotype_pars dictionary do. Both kinds are
# given in the order [best, lower_bound, upper_bound].
calib_pars = dict(
        beta=[0.05, 0.010, 0.20],
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

# List extra results that we don't have data on, but wish to include in the
# calibration object so we can plot them.
results_to_plot = ['cancer_incidence', 'asr_cancer_incidence']

# Create the calibration object, run it, and plot the results
calib = hpv.Calibration(
    sim,
    calib_pars=calib_pars,
    genotype_pars=genotype_pars,
    extra_sim_result_keys=results_to_plot,
    datafiles=datafiles,
    total_trials=3, n_workers=2
)

calib.calibrate(die=True)


calib.plot(res_to_plot=4);
# %%
update_pars = dict(location='nigeria',verbose=0, 
    f_cross_layer = 0.05, 
    m_cross_layer = 0.15 
)

test_sim = hpv.Sim(update_pars)

# Create the calibration object, run it, and plot the results
update_calib = hpv.Calibration(
    test_sim,
    calib_pars=calib_pars,
    genotype_pars=genotype_pars,
    extra_sim_result_keys=results_to_plot,
    datafiles=datafiles,
    total_trials=3, n_workers=2
)

update_calib.calibrate(die=True)


update_calib.plot(res_to_plot=4);


# Okay was good test. Looks like data points have moved, this is not true the scale has just changed. 
# The best estimates have changed though, so looks like the specific pars are being used in the calibration
