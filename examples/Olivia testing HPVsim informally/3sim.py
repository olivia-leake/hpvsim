#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 16:25:06 2025

@author: olivialeake
"""

import os
import sys

print(">>> Current working directory:", os.getcwd())
print(">>> hpvsim is imported from:", sys.modules.get("hpvsim"))
print(">>> sys.path:")
for p in sys.path:
    print("    ", p)



# %%



import hpvsim as hpv

hpv.Sim()

# %%



pars = dict( location = 'nigeria', )

sim1 = hpv.Sim(pars = pars, label = 'testsim')

help(hpv.pars)