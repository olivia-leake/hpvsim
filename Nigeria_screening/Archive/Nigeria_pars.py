#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 09:40:03 2025

@author: olivialeake
"""

### LOOK AT nigeria_calibrated_sim_new FOR THE CORRECT WAY TO DO THIS

import hpvsim as hpv

# simulation pars
sim_pars = dict(
    n_agents = 10e3, # Have 50,000 people total in the population (NOTE: actual tanzanian pop in 1980 was 19.2million, so 1 agent represents about 380 people)
    start = 1980, # Start the simulation in 1980
    end = 2030,
    burnin = 25, # Discard the first 20 years as burnin period
    dt = 0.25,
    verbose = 0, # Do not print any output
    rand_seed = 2 # Should change the random seed if want to produce different sims
    )

location_pars = dict(
    location = 'Nigeria',
    network = 'default',     # Use layered network rather than random
    beta = 0.3 # Note that beta is NOT a genotype parameter, but is an epidemiological param
    )

# %%


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


## These are the defaults for the defualt network

    # # Specify defaults for basic sexual network with marital, casual, and one-off partners
    # layer_defaults['default'] = dict(
    #     m_partners = dict(
    #         m=dict(dist='poisson1', par1=0.01), # Everyone in this layer has one marital partner; this captures *additional* marital partners. If using a poisson distribution, par1 is roughly equal to the proportion of people with >1 spouse
    #         c=dict(dist='poisson1', par1=0.5)
    #     ),  # If using a poisson distribution, par1 is roughly equal to the proportion of people with >1 casual partner within a single time step
    #     f_partners = dict(
    #         m=dict(dist="poisson1", par1=0.01),
    #         c=dict(dist='poisson', par1=1), # Defaults: {'0': 0.36, '1': 0.37, '2': 0.19, '3': 0.06, '4+':0.02}
    #     ),
    #     acts         = dict(m=dict(dist='neg_binomial', par1=80, par2=40), # Default number of acts per year for people at sexual peak
    #                         c=dict(dist='neg_binomial', par1=50, par2=5)), # Default number of acts per year for people at sexual peak
    #     age_act_pars = dict(m=dict(peak=30, retirement=100, debut_ratio=0.5, retirement_ratio=0.1), # Parameters describing changes in coital frequency over agent lifespans
    #                         c=dict(peak=25, retirement=100, debut_ratio=0.5, retirement_ratio=0.1)),
    #     dur_pship   = dict(m=dict(dist='neg_binomial', par1=80, par2=3), # This gives: mar_dur = {'0-5y': 0.015, '5-10y': 0.025, '10-20y':0.06, '20-50y':0.25, '50+':0.65}
    #                        c=dict(dist='lognormal', par1=1, par2=2)), # This gives: cas_dur = {'0-3m': 0.33, '3-6m': 0.22, '6-12m': 0.2, '1-2y':0.15, '2-5y':0.1}
    #     condoms     = dict(m=0.01, c=0.2),  # Default proportion of acts in which condoms are used
    # )
    # layer_defaults['default']['mixing'], layer_defaults['default']['layer_probs'] = get_mixing('default')
    
# %% Try running code without changing genotype pars

# Combine the dictionaries
Nigeria_pars = {**location_pars, **layer_pars, **sim_pars}

Nigeria_sim = hpv.Sim(Nigeria_pars, label = 'Nigeria sim') # This is an instance of the class Sim

Nigeria_sim.run()
first_Nigeria_plot = Nigeria_sim.plot()

hpv.savefig('/Users/olivialeake/Library/CloudStorage/OneDrive-Nexus365/Part B/BSP project/HPV Project/hpvsim/examples/Olivia testing HPVsim informally/First_Nigeria_plot.png',
            fig = first_Nigeria_plot)

# %%

#======================= DON'T USE THIS, INSTEAD SEE change_geon_pars.py !!!




# Genotype parameters from Fabian claibration






geno_pars = {
        'beta': 0.3,  # temporary until get Fabian calib
        'genotype_pars': {
            'hpv16': {
                'dur_precin': {'par1': 6},
                'cin_fn': {'k': 0.3},
            },
            'hpv18': {
                'dur_precin': {'par2': 5},
            },
        },
    }



# geno_pars = dict(
#     beta = 0.3, # temporary until get Fabian calib
#     pars['hpv16']['dur_precin']['par1'] = 6,  # temporary until get Fabian calib
#     pars['hpv16']['cin_fn']['k'] = 0.28,  # temporary until get Fabian calib
#     pars['hpv18']['dur_precin']['par2'] = 5,  # temporary until get Fabian calib
#     pars['hpv16']['cin_fn']['k'] = 0.3  # temporary until get Fabian calib
#     )

# Network paramters from Fabian calibration
net_pars = {
    'f_cross_layer' : 0.05, # temporary until get Fabian calib
    'm_cross_layer' : 0.15 # temporary until get Fabian calib
    }


Nigeria_pars_updated = {**location_pars, **layer_pars, **sim_pars, **geno_pars, **net_pars}

Nigeria_sim = hpv.Sim(pars = Nigeria_pars_updated, label = 'Nigeria sim updated')
# Check got correct parameters by inspecting
# print(Nigeria_sim.pars)

# Has beta = 0.3 (default was 0.25 so know it has taken my pars)
# m_cross_layer has also been updated
# genotype parameters have also been updated ! So this is correct !

## Fine, but does it run?
Nigeria_sim.run() # Nope it doesn't run. Lets check if it's just because of **geno_pars


# %%




# TEST
Nigeria_pars_test = {**location_pars, **layer_pars, **sim_pars, **net_pars}
Nigeria_test_sim = hpv.Sim(Nigeria_pars_test, label = 'Nigeria test')

Nigeria_test_sim.run()
# Yes, this runs fine. So it is just the genotype pars causing the error


# %%




Nigeria_pars_test = {**location_pars, **layer_pars, **sim_pars, **net_pars}
Nigeria_test_sim2 = hpv.Sim(Nigeria_pars_test, label = 'Nigeria test')

Nigeria_test_sim2.pars['genotype_pars']['hpv16']['dur_precin']['par1'] = 6

# %%

# geno_pars = hpv.parameters.get_genotype_pars(genotype= ['hpv16', 'hpv18', 'hi5']) # gets the full default dictionary for all genotypes
geno_pars = hpv.parameters.get_genotype_pars(default= True)

# Change specific values within that dictionary

geno_pars.hpv16.dur_precin['par1'] = 6
geno_pars.hpv16.cin_fn['k'] = 0.28
geno_pars.hpv18.dur_precin['par2'] = 5


# You can't merge normal dicitonaries and sc.obdict like normal

# Now add geno_pars to pars, and create the sim
Nigeria_pars = {**location_pars, **layer_pars, **sim_pars, **net_pars}

# Now modify the dictionary to include geno_pars
Nigeria_pars['genotype_pars'] = geno_pars

nig_sim = hpv.Sim(Nigeria_pars, label = 'Nigeria', rand_seed = 2)

nig_sim.run()
## This didn't work as by default the sim only includes genotypes 16, 18 and hi5
## But when getting the full dictionary you 


parameters.get_genotype_pars(genotype = )




# %%





Nigeria_pars_updated = {**location_pars, **layer_pars, **sim_pars, **net_pars}

Nigeria_pars_updated['genotype_pars']['hpv16']['dur_precin']['par1'] = 6
Nigeria_pars_updated['genotype_pars']['hpv16']['cin_fn']['k'] = 0.28
Nigeria_pars_updated['genotype_pars']['hpv18']['dur_precin']['par2'] = 5


Nigeria_sim.pars['genotype_pars']['hpv16']['dur_precin']['par1'] = 6
Nigeria_pars_updated['genotype_pars']['hpv16']['cin_fn']['k'] = 0.28
Nigeria_pars_updated['genotype_pars']['hpv18']['dur_precin']['par2'] = 5


Nigeria_sim = hpv.Sim(pars = Nigeria_pars_updated, 
                      pars['genotype_pars']['hpv16']['dur_precin']['par1'] = 6
                      label = 'Nigeria sim updated')




## Default hpv genotype parameters

# Basic disease transmission parameters
# pars['beta']                = 0.25


# pars.hpv16 = sc.objdict()
# pars.hpv16.dur_precin       = dict(dist='lognormal', par1=3, par2=9)  # Duration of infection prior to precancer, chosen so that ~50% clear after 1 year (Schiffman et al)
# pars.hpv16.cin_fn           = dict(form='logf2', k=0.3, x_infl=0, ttc=50)  # Function mapping duration of infection to probability of developing cin
# pars.hpv16.dur_cin          = dict(dist='lognormal', par1=5, par2=20) # Duration of episomal infection prior to cancer
# pars.hpv16.cancer_fn        = dict(method='cin_integral', transform_prob=2e-3) # Function mapping duration of cin to probability of cancer
# pars.hpv16.rel_beta         = 1.0  # Baseline relative transmissibility, other genotypes are relative to this
# pars.hpv16.sero_prob        = 0.75 # https://www.sciencedirect.com/science/article/pii/S2666679022000027#fig1

# pars.hpv18 = sc.objdict()
# pars.hpv18.dur_precin       = dict(dist='lognormal', par1=2.5, par2=9)  # Duration of infection prior to precancer, chosen so that ~50% clear after 6m (Schiffman et al)
# pars.hpv18.dur_cin          = dict(dist='lognormal', par1=5, par2=20) # Duration of infection prior to cancer
# pars.hpv18.cin_fn           = dict(form='logf2', k=0.25, x_infl=0, ttc=50)  # Function mapping duration of infection to probability of developing cin
# pars.hpv18.cancer_fn        = dict(method='cin_integral', transform_prob=2e-3)  # Function mapping duration of infection to severity
# pars.hpv18.rel_beta         = 0.75  # Relative transmissibility, current estimate from Harvard model calibration of m2f tx
# pars.hpv18.sero_prob        = 0.56 # https://www.sciencedirect.com/science/article/pii/S2666679022000027#fig1


## Default netowrk parameters

# pars['f_cross_layer']   = 0.05  # Proportion of females who have concurrent cross-layer relationships - by layer
# pars['m_cross_layer']   = 0.30  # Proportion of males who have concurrent cross-layer relationships - by layer



