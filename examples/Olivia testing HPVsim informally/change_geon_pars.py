#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 10:07:49 2025

@author: olivialeake
"""
# Changing values of a sciris.objdict

import sciris as sc

# Method 1: treat it like a normal python dictionary
# Method 2: Treat it like an object with attribute acess

## 1)
od = sc.objdict(a=1, b=2)
od
#0. 'a': 1
#1. 'b': 2
od.a = 10
#0. 'a': 10
#1. 'b': 2

## 2)
od['b'] = 20
#0. 'a': 10
#1. 'b': 20

# %%

# Understanding of the function get_genotype_pars


# I think get_genotype_pars is making a dictionary inside a dictionary
# In initialisation, pars is being treated as a noraml dictionary, pars = {}
# But then inside this function get_genotype_pars, it looks like pars is now being treated
# as a sciris object dictionary

# Then inside that dictionary, you create the objects
# 1)  pars.hpv16
# 2) pars.hpv18
# 3) pars.hi5
#4) pars.ohr etc...

# Then each of those objets themselves become a sciris object dictionary, each with 
# objects
# 1) dur_precin
# 2) cin_fn etc....

# Each of these objects are then assigned a value, sometimes this value is a dictionary itself
# But it is a normal dictionary, NOT a sciris object dictionary

# Note that a dictionary is not the same as an object dictionary (although of course dictionaries
# do hold objects, as everything in Python is an object)

# An object dictionary is one which allows 'attribute-style' access
# That means rather than going my_dict['a'] = 2, like you would a normal dictionary,
# You can change values of entries by doing my_dict.a , ie: it's treating the entires as 
# attributes of the dictionary, rather than an object

# %%

import hpvsim as hpv

type(hpv.parameters.make_pars())
# Out[33]: dict


# When you define a variable like pars inside a function, that variable exists only 
# while the function runs.
# You cannot access pars directly from outside the function unless the function returns it.

# Variables defined inside a function are local to that function.
# So pars inside function_a() is totally separate from pars inside function_b().

type(hpv.parameters.get_genotype_pars())
# Out[34]: sciris.sc_odict.objdict

sim = hpv.Sim() # In () want to over-write the genotype parameters
sim = hpv.Sim(location = 'Tanzania') 
# The sim knows 'locatoin' without knowing pars. This is because it takes in kwargs
# The function uses sim.py to run. 
# The functtion starts by using: 
# ' default_pars = hppar.make_pars(version=version) # Start with default pars'
# hppar is the imported parameters.py module

# Then it updates parameters by using the update_pars function which is called
# The update_pars function is defined in baase.py. It works by merging the dictionaries
# pars and kwargs. Anything that is written twice is over-ridden

# looks like the problem with the genotype parameters is they are handled differently
# they are not made in the initialisation using the function make_pars
# instead the instance uses the funtion 'self.init_genotypes() # Initialize the genotypes'


hpv.parameters.get_genotype_pars()
# This function returns pars

# So if you set
genotype_pars = hpv.parameters.get_genotype_pars()
# then genotype_pars is the object dictionary containing all the genotypes

genotype_pars.hpv16.dur_precin['par1'] = 6  
genotype_pars.hpv16.cin_fn['k'] = 0.3
genotype_pars.hpv18.dur_precin['par2'] = 5
genotype_pars.hpv18.cin_fn['k'] = 0.28

genotype_pars # great they have been updated

# NOW, need to ensure that my simulation uses genotype_pars. Wonder if can pass it as kwarg?
# hpv.Sim(genotype_pars) didn't work

sim = hpv.Sim() # This is an instance of the class sim

sim.genotype_pars = genotype_pars

# sim['genotype_pars'] = ...
# sim.genotype_pars = ...       # Either of these work since Sim class inherits from 
                                # sciris.objdict, which suppoers both dot and dict-styole notatoin

# check it has worked
print(sim.genotype_pars)
# YAYYYYY IT'S WORKED !!














# %%


# This is the function that tells you the current genotype parameters
hpv.parameters.get_genotype_pars(genotype='hpv16')

#0. 'dur_precin': {'dist': 'lognormal', 'par1': 3, 'par2': 9}
#1. 'cin_fn':     {'form': 'logf2', 'k': 0.3, 'x_infl': 0, 'ttc': 50}
#2. 'dur_cin':    {'dist': 'lognormal', 'par1': 5, 'par2': 20}
#3. 'cancer_fn':  {'method': 'cin_integral', 'transform_prob': 0.002}
#4. 'rel_beta':   1.0
#5. 'sero_prob':  0.75



# This is the function that sets the genotypes
# def get_genotype_pars(default=False, genotype=None):
#     '''
#     Define the default parameters for the different genotypes
#     '''

#     pars = sc.objdict()

#     pars.hpv16 = sc.objdict()
#     pars.hpv16.dur_precin       = dict(dist='lognormal', par1=3, par2=9)  # Duration of infection prior to precancer, chosen so that ~50% clear after 1 year (Schiffman et al)
#     pars.hpv16.cin_fn           = dict(form='logf2', k=0.3, x_infl=0, ttc=50)  # Function mapping duration of infection to probability of developing cin
#     pars.hpv16.dur_cin          = dict(dist='lognormal', par1=5, par2=20) # Duration of episomal infection prior to cancer
#     pars.hpv16.cancer_fn        = dict(method='cin_integral', transform_prob=2e-3) # Function mapping duration of cin to probability of cancer
#     pars.hpv16.rel_beta         = 1.0  # Baseline relative transmissibility, other genotypes are relative to this
#     pars.hpv16.sero_prob        = 0.75 # https://www.sciencedirect.com/science/article/pii/S2666679022000027#fig1


## These are the names of the genotypes you can change
# def get_genotype_choices():
#     '''
#     Define valid genotype names
#     '''
#     # List of choices available
#     choices = {
#         'hpv16':    ['hpv16', '16'],
#         'hpv18':    ['hpv18', '18'],
#         'hi5':      ['hi5hpv', 'hi5hpv', 'cross-protective'],
#         'ohr':      ['ohrhpv', 'non-cross-protective'],
#         'hr':       ['allhr', 'allhrhpv', 'hrhpv', 'oncogenic', 'hr10', 'hi10'],
#         'lo':       ['lohpv'],
#     }
#     mapping = {name:key for key,synonyms in choices.items() for name in synonyms} # Flip from key:value to value:key
#     return choices, mapping