#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 13:16:48 2025

@author: olivialeake
"""
# There are two ways to create a dictionary

# The first is using dictionary module directly

my_dict = dict( 'a' = 1, 'b' = 2)
# SyntaxError: expression cannot contain assignment, perhaps you meant "=="?
my_dict2 = dict( a = 1, b = 2)
                


# the second is using curely brackets

my_second_dict = {'Keyword' : 3, 'keyword2' : 4}


my_second_dict2 = {Keyword : 5, keyword2 : 6}
# NameError: name 'Keyword' is not defined