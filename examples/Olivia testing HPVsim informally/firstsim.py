#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 09:42:48 2025

@author: olivialeake
"""

import hpvsim as hpv


pars = dict(
    location = 'tanzania', # Use population characteristics for Japan
    n_agents = 10e3, # Have 50,000 people total in the population (NOTE: actual tanzanian pop in 1980 was 19.2million, so 1 agent represents about 380 people)
    start = 1980, # Start the simulation in 1980
    n_years = 50, # Run the simulation for 50 years
    burnin = 10, # Discard the first 20 years as burnin period
    verbose = 0, # Do not print any output
)


sim = hpv.Sim() 
sim.run()
fig = sim.plot()