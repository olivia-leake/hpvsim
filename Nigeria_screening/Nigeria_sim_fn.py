#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 10:00:57 2025

@author: olivialeake
"""
import hpvsim as hpv


# Make a Nigeria sim function

def make_nigeria_sim(interventions=None, rand_seed=None, **kwargs):
    
    if rand_seed is None:
        rand_seed = 1
    

    # simulation pars
    sim_pars = dict(
        n_agents = 10e3, # Have 50,000 people total in the population (NOTE: actual tanzanian pop in 1980 was 19.2million, so 1 agent represents about 380 people)
        start = 1980, # Start the simulation in 1980
        end = 2030,
        burnin = 25, # Discard the first 20 years as burnin period
        dt = 0.25,
        verbose = 0 # Do not print any output
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


    Nigeria_sim = hpv.Sim(pars=Nigeria_pars, rand_seed = rand_seed, interventions=interventions, **kwargs)
    
    
    
    ## Genotype pars have to be added after the sims creation
    
    genotype_pars = hpv.parameters.get_genotype_pars()
    # then genotype_pars is the object dictionary containing all the genotypes

    genotype_pars.hpv16.dur_precin['par1'] = 6  # TEMP
    genotype_pars.hpv16.cin_fn['k'] = 0.3       # TEMP
    genotype_pars.hpv18.dur_precin['par2'] = 5  # TEMP
    genotype_pars.hpv18.cin_fn['k'] = 0.28      # TEMP


    # Assign the genotype parameters to the simulation
    Nigeria_sim.genotype_pars = genotype_pars
    
    
    
    
    return Nigeria_sim


# # Works alone
# sim1 = make_nigeria_sim(label = 'no vax')
# sim1.run()
# sim1.plot()

# # Works changing random seed
# sim2 = make_nigeria_sim(rand_seed = 2)
# sim2.run()
# sim2.plot()

# # Accepts keyword args
# sim3 = make_nigeria_sim(location = 'india')
# sim3.run()
# sim3.plot()
# sim3['location'] # india


# # Accepts interventions
# vx = hpv.routine_vx(prob=0.6, start_year=2015, age_range=[9,10], product='bivalent')
# sim4 = make_nigeria_sim(interventions = vx, label = 'vax')
# sim4.run()
# sim4.plot()
# sim4['interventions'] 
# # Out[328]: [hpv.routine_vx(product=bivalent, prob=None, age_range=[9, 10], sex=0, eligibility=None, label=None)]
# # Not sure why prob = None
# # That said, if you compare it to Sim1, cancer incidence per age is the same up to 2015,
# # and declines after that, therefore am sure that it is being applied
# print(type(sim4['interventions'])) # list, not a dictionary, so can't call elements by name
# sim4['interventions'][0]


# # Plot comparison 
# msim.plot(sim1, sim4) # note this doesn't work because it only works if you used
# # multisim to create the plots in the first place

# # You don't need to run them again, but you do have to create a multisim in order
# # to compare them

# msim = hpv.MultiSim([sim1,sim4])

# msim.plot()




