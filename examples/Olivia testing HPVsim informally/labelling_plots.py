#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 14:18:13 2025

@author: olivialeake
"""

## This failed, however I have decided to abandon labelling plots since it will look better
## in overleaf to caption the figures instead.
## In order to keep track of the plots I need to be really careful about labelling them 
## when I save them !

import hpvsim as hpv

pars1 = dict(
    location = 'tanzania', # Use population characteristics for Japan
    n_agents = 10e3, # Have 50,000 people total in the population (NOTE: actual tanzanian pop in 1980 was 19.2million, so 1 agent represents about 380 people)
    start = 1980, # Start the simulation in 1980
    n_years = 50, # Run the simulation for 50 years
    burnin = 10, # Discard the first 20 years as burnin period
    verbose = 0, # Do not print any output
)


sim = hpv.Sim(pars1) 

sim.run()
sim.plot(fig_args = dict(suptitle = 'Legend'))

# fig_args=None, plot_args=None, scatter_args=None, axis_args=None, fill_args=None,
#                 bar_args=None, legend_args=None, date_args=None, show_args=None, style_args=None, contour_args=None, **kwargs):

help(sim.plot)
help(sim.plot())

