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



# %%


# From tutorial 4 you can see the function used to show all locations
# Q : Is this in the API reference?

hpv.data.show_locations() 

# I have recieved an error when trying to pass this 
# I want to know which file contains this function so hopefully can 
# use the help function to get the Method resolution order

print(help(hpv.data.show_locations() ))

# I got the error
# AttributeError: module 'hpvsim.data' has no attribute 'show_locations'
# So I need to look at the module/file , 'hpvsim.data'

print(help(hpv.data)) 
# searching the package data from the hpvsim repo (note called it a package not a module now, so it recongnises that
# the data folder is indeed a folder rather than a .py file) 

# Have searched up show_locations in the Find pane, it shows 6 matches in 3 files
# One of the files is this one and contains 3 matches
# Another of the files is hpv_t4.py which contains 2 matches
# The final is tut_people.ipynb which contains one match

