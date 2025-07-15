#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:28:57 2025

@author: olivialeake
"""

import hpvsim as hpv

pars = hpv.make_pars()
pars['rand_seed'] = 2
pars['n_agents'] = 10_000

sim1 = hpv.Sim(pars)
sim1.run()

sim2 = hpv.Sim(pars)
sim2.run()


sim1.plot()
sim2.plot()

# Note that these plots are the same, so random seed appears to be working

# What about if you don't directly set random seed? Should be the same as the default random
# seed is 1 

sim3 = hpv.Sim()
sim3.run()

sim4 = hpv.Sim()
sim4.run()


sim3.plot()
sim4.plot()

# Yes, still the same !
# To run different simulations to compare, does that mean I should set different random seeds?
# Yes. Or look at multisims maybe