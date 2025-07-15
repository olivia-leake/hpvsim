#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 14:49:35 2025

@author: olivialeake
"""

import hpvsim as hpv

# How do multisims handle random seeds?

sim = hpv.Sim()
msim = hpv.MultiSim(sim)
msim.run(n_runs=5)
msim.plot();


sim = hpv.Sim(rand_seed = 2)
msim = hpv.MultiSim(sim)
msim.run(n_runs=5)
msim.plot();

sim = hpv.Sim(rand_seed = 2)
msim = hpv.MultiSim(sim)
msim.run(n_runs=5)
msim.plot();

# Running a multisim with a random seed produces the same multisim each time
# It does not however produce a plot of the same sim multiple times
# ie: each simulation has not used the same random seed within multisim

sim = hpv.Sim(rand_seed = 3)
msim = hpv.MultiSim(sim)
msim.run(n_runs=5)
msim.plot();

# It appears if using the rand_seed = 3 in comparison to rand_Seed = 2 has changed
# only 1 simulation, so the multisim ranodm seed probably handles sims by doing
# sim1 = seed + 1, sim 2+ seed +2 etc..
# So that all except 1 simulation overlap when increasing the random seed by 1


sim = hpv.Sim(rand_seed = 4)
msim = hpv.MultiSim(sim)
msim.run(n_runs=5)
msim.plot();

# This is an issue, however if you make sure seed2 - seed1 > n_runs then you should have
# no overlapping sims
# To be honest, the whole point in running multsims is to run multiple sims, 
# so why would you run multiple, multisims
# If you want more sims, just increase n_runs and this problem should be avoided!