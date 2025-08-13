#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 18:35:17 2025

@author: olivialeake
"""

import hpvsim as hpv
import numpy as np

# Make a UK sim function

def make_uk_sim(interventions=None, rand_seed=None,vax=True, **kwargs):
    '''
    Create a UK parameterised simulation
    '''
    # Note the default is to apply the sim to girls. wonder if there is a setting to extend to boys?

    

    
    # First add in the vaccination introduced in Oct 2023 to 9-14 year olds. This is a yearly vaccination. 
    # For fist 10 years 70% of target recieve vaccine, this steps up to 80% thereafter
    if vax == True:
        
        vx1 = [hpv.routine_vx(product='quadrivalent', prob=[0.7]* (10) + [0.8]* (16), years=np.arange(2024, 2050) )] # Needs be a list so it can concatenate with interventions
        
        vx2 = hpv.routine_vx(product='bivalent', age_range=[9,10], prob=0.9, sex=[0,1], years=np.arange(2020,2025)) # Vaccinate boys and girls
        
        
        
    else: vx = None
    
    
    # Ensure vx and interventions are lists (or None)
    if vx is None and interventions is None:
        combined_interventions = None
    else:
        vx = vx or [] # if vx and interventions are both not None, then vx will either be the list that was passed, or is no list was passed, it will default to empty list. You won't have two empty lists, since it both were none would default to none
        interventions = interventions or []
        combined_interventions = vx + interventions


    if rand_seed is None:
        rand_seed = 1
    

    # simulation pars
    sim_pars = dict(
        n_agents = 10e3,
        start = 1990, # Start the simulation in 1990
        end = 2050, # End the simulation in 2050
        burnin = 25, # Discard the first 25 years as burnin period
        dt = 0.25,
        verbose = 0 # Do not print any output
        )
    
    location_pars = dict(
        location = 'Nigeria',
        network = 'default',     # Use layered network rather than random,
        beta = 0.3 # Not a genotype parameter so specify it here. TEMP, update with Fabian parameters
        )
    
# Beta default is 0.25
    
    
    # Parameters specified by layer
    layer_pars = dict(
       # f_partners = None,
       # m_partners = None, #Leave as default for now as using default network and don't have the info for married and casual
       # act = None
       # age_act_pars = None
       # layer_probs = None 
       # dur_pship = None # Don't have info for this
        condoms = dict(m=0.016, c=0.185)
            )
    
    # layer_defaults['default']['mixing'], layer_defaults['default']['layer_probs'] = get_mixing('default')
    
    # Leave layer_probs as defualt. But need to know where to input number
    # of married and casual
    
    
    # Network paramters from Fabian calibration
    net_pars = {
        'f_cross_layer' : 0.05, # temporary until get Fabian calib
        'm_cross_layer' : 0.15 # temporary until get Fabian calib
        }
    
    
    # Combine the dictionaries
    Nigeria_pars = {**location_pars, **layer_pars, **sim_pars, **net_pars}


    Nigeria_sim = hpv.Sim(pars=Nigeria_pars, rand_seed = rand_seed, interventions= combined_interventions, **kwargs)

    
    
    ## Genotype pars have to be added after the sims creation
    
    genotype_pars = hpv.parameters.get_genotype_pars()
    # then genotype_pars is the object dictionary containing all the genotypes

    genotype_pars.hpv16.dur_precin['par1'] = 6  # TEMP # Default = 3
    genotype_pars.hpv16.cin_fn['k'] = 0.3       # TEMP # Default = 0.3
    genotype_pars.hpv18.dur_precin['par1'] = 5  # TEMP # Default = 2.5
    genotype_pars.hpv18.cin_fn['k'] = 0.28      # TEMP # Default = 3


    # Assign the genotype parameters to the simulation
    Nigeria_sim.genotype_pars = genotype_pars
    

    return Nigeria_sim