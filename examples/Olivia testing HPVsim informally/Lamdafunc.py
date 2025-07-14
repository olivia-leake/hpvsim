#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 09:45:07 2025

@author: olivialeake
"""

# my first lamda func

# Creating a function to add 1
add_1 = lambda x: x + 1 

# To use this function
add_1(5)    # 6
add_1(12)   # 13

result = add_1(5)
print(result)

# The idea in using result and printing it rather than just running the function in
# the console is so that we can use the result moving forward, we create a varible

# Similarly when we create normal function using def, we want to return the output, 
# rather than simply printing it, so that the result can be carried forward if need be

# Now try re-create using def

def add_1_def(x): # will take 1 input x
    return x + 1

result2 = add_1_def(5)
print(result2)    # 6

# Yay!

# Now what is different here

def add_1_def2(x):
    print(x + 1)
    
result3 = add_1_def2(5)     #6

# Well let's try and multiply the result in all 3 cases by 2

r4 = result * 2
r5 = result2 * 2
r6 = result3 * 2

print(r4) # 12
print(r5) # 12 
print(r6) # nameError: name 'r6' is not defined. This is because when you 
# you print x +1, you turn the result x+1 into a string rather than an interger

# %%

# 2 varibale lamda function

add_two_numbers = lambda x, y: x + y   # Notice how you don't need parentheses

r7 = add_two_numbers(3,5)
print(r7)   # 8 

# what would happen if you included parentheses?
add_two_numbers2 = lambda (x, y): x + y 

r8 = add_two_numbers2(3,5)
print(r8) # Get invalid syntax error ! So can't use parentheses

# %%

# Map function - takes some list and applies a function to every value inside of it

mylist = [1, 2, 3, 10, 11, 12]

# want to define a function to square every number within the list

def sqaure(x):
    return x ** 2

# is there a repeat function ie: repeat the list (1,2,3) , 5 times
# is there a start list function, add intervals of 3, do this 10 times?
# potentially way you create a matrix

newlist = [] # Define an empty list

# Fill it in by creating a for loop
for x in mylist:
    newlist.append(square(x)) # append adds an element to the end of an existing list
    
print(newlist)

# However we can do this much faster using the map function 



# The map function takes two arguments, a function and a list
print(list(map(square, mylist) ))
# Notice how I could do this all in 1 line rather than 4! 

# HOWEVER, we don't need to use the sqaure function again and therefore it 
# is easier to just create a lambda function 

# We want to create a new list of the squares of my list
# Remember the list function takes the input function and a list
# So we put the function agument to be the lamda function
squares = list(map(lambda x: x ** 2, mylist))
print(squares)

# %%

# filter function - used for deciding when something is true or false in a list

evens = list(filter( lambda x: x % 2 == 0 , mylist)) # % is modulus operator
print(evens)

# The filter function doesn't give you a boolean array, but rather it just filters out
# the values which are false

# %%

# sorted function 

# Has standard properties which work as expected, ie: sorts into ascending order
a = (1, 11, 2)
x = sorted(a)
print(x)

# To sort into descending order
a = ("h", "b", "a", "c", "f", "d", "e", "g")
x = sorted(a, reverse=True)
print(x)

# Then to override the standard property, you use the key parameter
# ie: sorted takes two inputs, (value: key). key is optional and will refer to default if empyt

a = ("Jenifer", "Sally", "Jane")
x = sorted(a, key=len)
print(x)

# Now using the lamda function as the key to sort the values
values = [(1, 'b', 'hello'), (2, 'a', 'world'), (3, 'c', '')]
# Note the values is a list of tuples. Tuples are list which are structured and can not
# be changed

# Sort the list 
sorted_values = sorted(values, key = lambda x: x[1]) #Recall that lists indexing starts at 0    
# So this sorts the list by the seocnd value
print(sorted_values)


# Quick note on tuples vs lists
v = (1, 2, 3)
new = v + (4) # you can onlu concatenate tuple to tuple (not int)

w = [1, 2, 3]
new2 = w + [4] 
print(new2)






