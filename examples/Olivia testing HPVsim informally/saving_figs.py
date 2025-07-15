#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 13:59:57 2025

@author: olivialeake
"""

import hpvsim as hpv

sim = hpv.Sim()
sim.run()

fig_to_save = sim.plot()

# You can save a figure using. You need to label your plots, then tell the savefig function
# which plot you want it to save
hpv.savefig('/Users/olivialeake/Library/CloudStorage/OneDrive-Nexus365/Part B/BSP project/HPV Project/hpvsim/examples/Olivia testing HPVsim informally/practise-save.png', fig = fig_to_save)      

hpv.get_png_metadata('/Users/olivialeake/Library/CloudStorage/OneDrive-Nexus365/Part B/BSP project/HPV Project/hpvsim/examples/Olivia testing HPVsim informally/practise-save.png')
