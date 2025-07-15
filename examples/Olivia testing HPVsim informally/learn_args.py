#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 12:27:18 2025

@author: olivialeake
"""

# *args and **kwargs (keyword arguments) are important for designing functions which can 
# take arbitrarily large inputs 

# For example summing all the numbers specified

# *args tells Python:
# "This function can take any number of positional arguments."

def sum_numbers(*args):
    # Here, the * packs all extra positional arguments into a tuple called args.
    # So you don't need to specify * again
    return sum(args)

sum_numbers(5,10,12) # 27



# %%


# **kwargs tell Python:
# "This function can take any number of keyword arguments."

# **kwargs example
def fun(**kwargs):
    for k, val in kwargs.items():
        print(k, val)
        
# In Python, .items() is a method you call on a dictionary, and it returns a view of
# the dictionary’s key-value pairs as tuples.

fun(a=1, b=2, c=3)

# a 1
# b 2
# c 3


# %%


# .get() is a dictionary method in Python. It’s a safe way to retrieve the value for a 
# given key without causing an error if that key doesn’t exist.

my_dict = dict( a= 1, b=2)
# Note that a and b are not variables, they are strings
# this is because dictionaries take in keyword:value
# And therefoere automatically treat the keyword as a string

# Therefore when referring to a again, you must use quotes
value = my_dict.get('a')
print(value) # 1


