#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 09:40:03 2025

@author: olivialeake
"""

import hpvsim as hpv

# simulation pars
sim_pars = dict(
    n_agents = 10e3, # Have 50,000 people total in the population (NOTE: actual tanzanian pop in 1980 was 19.2million, so 1 agent represents about 380 people)
    start = 1980, # Start the simulation in 1980
    end = 2030,
    burnin = 25, # Discard the first 20 years as burnin period
    dt = 0.25,
    verbose = 0, # Do not print any output
    )

location_pars = dict(
    location = 'Nigeria',
    network = 'default',     # Use layered network rather than random,
    beta = 0.3 # Not a genotype parameter so specify it here. TEMP, update with Fabian parameters
    )


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

Nigeria_sim = hpv.Sim(Nigeria_pars, label = 'Nigeria sim', rand_seed = 2)
# Should change the random seed if want to produce different sims


### Once the sim has been created, you can the update the genotype parameters

# Genotype parameters from Fabian claibration

genotype_pars = hpv.parameters.get_genotype_pars()
# then genotype_pars is the object dictionary containing all the genotypes

genotype_pars.hpv16.dur_precin['par1'] = 6  # TEMP
genotype_pars.hpv16.cin_fn['k'] = 0.3       # TEMP
genotype_pars.hpv18.dur_precin['par2'] = 5  # TEMP
genotype_pars.hpv18.cin_fn['k'] = 0.28      # TEMP


# Assign the genotype parameters to the simulation
Nigeria_sim.genotype_pars = genotype_pars # Notice genotype pars is instance specific rather than class


# Check got correct parameters by inspecting
print(Nigeria_sim.pars)
# Has beta = 0.3 (default was 0.25 so know it has taken my pars)
# m_cross_layer has also been updated


# 'genotype_pars': objdict() , so need to check this individually
print(Nigeria_sim.genotype_pars)
 #2. 'cin_fn':     {'form': 'logf2', 'k': 0.28, 'x_infl': 0, 'ttc': 50}
 # k = 0.28, so this has updated correctly




# %% Running the sim

Nigeria_sim.run()
second_Nigeria_plot = Nigeria_sim.plot()

hpv.savefig('/Users/olivialeake/Library/CloudStorage/OneDrive-Nexus365/Part B/BSP project/HPV Project/hpvsim/examples/Olivia testing HPVsim informally/Second_Nigeria_plot.png',
            fig = second_Nigeria_plot)

# Note that second nigeria plot has used the same random seed at first nigeria plot
# The plots have changed ever so slighlty taking account for the udpated genotype parametesr
# the genotype parameters are the only thing that is different between them
# Note that First_Nigera_plot iscreated in Nigeria_calibrated_sim_old


# I tried running the sim again but got the error saying that the simulation has already been ran
# The idea is that you need to re-initialise it, because there are certain attributes
# that need to be set at the beginning of the sim for it to run correctly
# ie: initial HPV prevalence is set, then the burn-in period allows it to settle to what it shoudl be
# also woman are expected to start with their target number of partners
# if you re-run the simulation without re-initialising the sim, the parameters will start
# in their end state rather than their beginning state


print(Nigeria_sim.t)
# 203


# re-initialise the rest of the sim
# Nigeria_sim.initialize()
# This didn't work, but this does
Nigeria_sim.initialize(reset= True) # think due to the change in population size
# ie: the sim does not re-set the population size unless do reseet = TRUE

print(Nigeria_sim.t)
# 0 - timestep now 0 so know has reset



# Check that parameters are as I set up
print(Nigeria_sim.pars['beta']) # 0.3 , yes same
print(Nigeria_sim.pars['condoms']) # 0.016 and 0.185, yes same !

# Check genotype pars are same as I set up as these are treated differently
print(Nigeria_sim.genotype_pars)
# k=0.28 for hpv18 cin_fn , so yes this works !!




# %% hpvsim Default parameters



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
    


