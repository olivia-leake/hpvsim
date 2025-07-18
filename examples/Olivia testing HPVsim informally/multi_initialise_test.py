#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 09:58:18 2025

@author: olivialeake
"""

## Testing to see if Multisim re-initializes the sims when you call it

import hpvsim as hpv

sim1 = hpv.Sim(beta=0.5)

sim2= hpv.Sim()

test_multi = hpv.MultiSim(([sim1,sim2]))

test_multi.run()

# Does not work when you try re-run it because you need to re-initialize
test_multi.run()


test_multi.initialize(reset=True)
# AttributeError: 'MultiSim' object has no attribute 'initialize'

# This error occurs because instead you need to initialize each one seperately

sim1.initialize(reset=True)
sim1.people=None
sim2.initialize(reset=True)
sim2.people=None

test_multi.run()

# Okay this doesn't work

# It doesn't actually matter though because you can just run from the beginning
# Lets just do that because it is not worth the time right now