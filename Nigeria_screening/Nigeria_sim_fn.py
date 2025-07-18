#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 10:00:57 2025

@author: olivialeake
"""
import hpvsim as hpv


# Make a Nigeria sim function

def make_nigeria_sim(interventions=None, rand_seed=None,vax=True, **kwargs):
    '''
    Create a Nigeria parameterised simulation
    '''
    
    # First add in the vaccination introduced in Oct 2023 to 9-14 year olds. This is a yearly vaccination
    if vax == True:
        vx = [hpv.routine_vx(prob=0.9, start_year = 2024, age_range=[9,14], product='quadrivalent')] # Needs be a list so it can concatenate with interventions
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

    genotype_pars.hpv16.dur_precin['par1'] = 6  # TEMP
    genotype_pars.hpv16.cin_fn['k'] = 0.3       # TEMP
    genotype_pars.hpv18.dur_precin['par2'] = 5  # TEMP
    genotype_pars.hpv18.cin_fn['k'] = 0.28      # TEMP


    # Assign the genotype parameters to the simulation
    Nigeria_sim.genotype_pars = genotype_pars
    
    

    return Nigeria_sim

# %%



# # Works alone
# sim1 = make_nigeria_sim(label = 'no vax 9 to 10, vax 9 to 14')
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
# vx1 = hpv.routine_vx(prob=0.6, start_year=2015, age_range=[9,10], product='bivalent')
# sim4 = make_nigeria_sim(interventions = [vx1], label = 'vax 9 to 10 and vax 9 to 14')
# sim4.run()
# sim4.plot()
# sim4['interventions'] 
# # Out[134]: 
# # [hpv.routine_vx(product=quadrivalent, prob=None, age_range=[9, 14], sex=0, eligibility=None, label=None),
# #  hpv.routine_vx(product=bivalent, prob=None, age_range=[9, 10], sex=0, eligibility=None, label=None)]
# # Not sure why prob = None
# # That said, if you compare it to Sim1, cancer incidence per age is the same up to 2015,
# # and declines after that, therefore am sure that it is being applied
# print(type(sim4['interventions'])) # list, not a dictionary, so can't call elements by name
# sim4['interventions'][0]

# # Lets you remove the vax
# sim5 = make_nigeria_sim(vax=False)
# sim5.run()
# sim5.plot()



# # Plot comparison 
# # msim.plot(sim1, sim4) # note this doesn't work because it only works if you used
# # multisim to create the plots in the first place

# # You don't need to run them again, but you do have to create a multisim in order
# # to compare them

# msim = hpv.MultiSim([sim1,sim4])

# msim.plot()

# # Now let's compare both sim1 and sim4 to themselves but with the vax in 2024 removed
# # sim1 no vax
# sim1_nv =make_nigeria_sim(vax=False, label = 'no vax at all')
# sim1_nv.run()
# sim4_nv = make_nigeria_sim(vax=False, interventions = [vx1], label = 'vax 9 to 10 and no vax 9 to 14')
# sim4_nv.run()

# msim_comp = hpv.MultiSim([sim1, sim1_nv, sim4, sim4_nv]) # I forgot to put the sims as a list and it didn't work !
# msim_comp.plot()

# # I think the issue is when I put vax = False, I can't then override it. It's not adding vx1
# # But then why are sim1 and sim4 not being plot?


