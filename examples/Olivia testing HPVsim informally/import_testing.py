#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 09:18:00 2025

@author: olivialeake
"""

import hpvsim as hpv

pars = dict(
    location = 'India',
    n_agents = 10e3,
    genotypes = [16, 18, 'hr'], # Simulate genotypes 16 and 18, plus all other high-risk HPV genotypes pooled together
    start = 1980,
    end = 2030,
)

# sexualnetwork_pars = dict(
#     )



# # When should you start and end the sim ? How long is the model reliable for ?

sim1  = hpv.Sim()

sim2  = hpv.Sim(location = 'uk')
# Looks like deomgraphic data for UK not available !

# %%

hpv.make_pars()
  # Create the parameters for the simulation. Typically, this function is used
  # internally rather than called by the user; e.g. typical use would be to do
  # sim = hpv.Sim() and then inspect sim.pars, rather than calling this function
  # directly.

# This function returns pars(dict) the parameters of the simulation.
# That said, I'm not sure how it knows which simulation to do

# Actually, right now the argument is empty, but if you add in pars as defined above,
# I'm sure it'll adapt the parameters it returns


# hpv.make_pars(pars)
# I got an error when trying to pass pars as the argument. This is because I have input pars
# as a positional argument, whereas the function takes keyword arguments.
# To check what inputs the function takes you must can use the help function :

help(hpv.make_pars)
# Help on function make_pars in module hpvsim.parameters:

# make_pars(**kwargs)
#     Create the parameters for the simulation. Typically, this function is used
#     internally rather than called by the user; e.g. typical use would be to do
#     sim = hpv.Sim() and then inspect sim.pars, rather than calling this function
#     directly.
    
#     Args:
#         version       (str):  if supplied, use parameters from this version
#         kwargs        (dict): any additional kwargs are interpreted as parameter names
    
#     Returns:
#         pars (dict): the parameters of the simulation


# Note that this has been written by the designer. 
# And actually isn't that helpful in this instance. Instead either use the 

print(sim1.pars)
# The console is not big enough to show all the parameter inputs
# An alternative is to check parameters individually ie:
    
print(sim1.pars['location']) # nigeria
# This helps check parameters, but not necessarily to find what the parameter inputs are
# The best way to see what the parameter inputs are is to checl the script itself

# hpv.reset_layer_pars()
# %%

# this
from hpvsim.data import loaders
# is equivalent to this
import hpvsim.data.downloaders


loaders.get_country_aliases()
# This works as loaders in the namespace now it's been impported

# You could not do hpvsim.data.loaders.get_country_aliases() since loaders was not apart
# of the dunder init file in hpvism 









