#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 11:02:15 2025

@author: olivialeake
"""

# %%


# def stands for define. Going to define a function
def say_hello():                        # say_hello is the function name
    print("Hello, World!")              # The function is designed to print "Hello, World!" when called
# Since indentation has stopped, Python knows you have finished defining the function
    

# Calling the function
say_hello() # Now the function will be performed.

# %%

# This function takes two numbers as input and returns their sum.

def add_numbers(a, b):
    return a + b

# Calling the function
add_numbers(3, 5)

# Equal sign is used to define variables
result = add_numbers(3, 4)
print("The sum is:", result)

# %%

# An f-string allows for inputs of variables which is printed at tun times. Inputs are encompassed by {}
name = 'Olivia'
age = 21

print(f"Hello my name is {name} and I am {age}")

# %%
# This function takes three numbers and returns the largest one.

def find_largest(a, b, c):
    if a > b and a > c:
        return a
    elif b > a and b > c:
        return b
    else:
        return c

# Calling the function
largest = find_largest(3, 7, 5)
print("The largest number is:", largest)

# %%

# Create a class
class MyClass:  # Class name. Classes do not need parentheses() like functions do, unless you are inhereting from another class
  x = 5
  
# Create an object - this does require parentheses() in order for the object to be created!
p1 = MyClass()    # The object is p1          
print(p1.x)
  
# %%

# Examples of classes and instances of classes

## Analogy 

# A class is a blueprint (like an architectural plan for a house).
# An instance is a built house — a specific object created from that plan.
# You can build many houses (instances) from the same blueprint (class), but each one can have different features (data).

class Employee:      # This is a class, it's a blueprint (like an architectural plan for a house)
    pass

emp1 = Employee()       # This is an instance of a class. emp1 is an instance variable (in comparison to a class variable).
emp2 = Employee()       # This is a different instance of a class

print(emp1)
print(emp2)

emp1.first = 'Cory'
emp1.last = 'Smith'
emp1.email = 'cory.smith@gmail.com'
emp1.pay = 50000

emp2.first = 'Test'
emp2.last = 'User'
emp2.email = 'test.user@gmail.com'
emp2.pay = 60000

# Now each of these instances have attributes that are unique to them

print(emp1.email)
print(emp2.email)

# What we have done here is manually set these variables every time, but this is 
# a lot of effort, and that's where classes come in, where we can set up
# these variables automatically when we create the employee

class Employee:    
    def __init__(self): # all classes and functions need a colon
        pass
    
    
# when we create methods (functions within classes), they recieve the instance as
# the first argument automatically. By conention we call this self. 
# self will just be the name of the instance

class Employee:    
    def __init__(self, first, last, pay): # all classes and functions need a colon
        self.first = first  # Creates the variable first. It is assigned to the instance self, and will take the value first as input into the instance
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@gmail.com'
    
# Now to create out instances we just input the variables either in order, or 
# by writing first = 'Cory'. 
# Note that the instance is passed automatically so that we can leave off self
# What this means is emp1 will be passed in as self
    
emp1 = Employee('Cory', 'Smith', 50000)       # This is an instance of a class. emp1 is an instance variable (in comparison to a class variable).
# emp2 = Employee()            
# This produced an error when it was ran. We initialised it, therefore requiring 
# that the arguments 'first', 'last' and 'pay' are entered. 
# If we hadn't initialised it, it would have been fine




# Now going to create a method to display full name
class Employee:    
    def __init__(self, first, last, pay): # all classes and functions need a colon
        self.first = first  # Creates the variable first. It is assigned to the instance self, and will take the value first as input into the instance
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@gmail.com'
        
    def fullname(self):
        return '{} {}'.format(self.first, self.last)
    
# I got the error AttributeError: 'Employee' object has no attribute 'fullname'
# This was because I defined the instance before editing the class
# You must always create the instance after you create the class

# Note that you shouldn't refer to a instance without referring to which class it is from
emp1= Employee('Cory', 'Smith', 50000)
    
# Now the class of employees all have an associated 'fullname' method
# This method can only be used in reference to an instance of the class
# Therefore we call the instance first, and then call which method we want to use from the class
print(emp1.fullname())



# You can also run the method directly from the class which makes it a bit clearer what
# is going on behind the scenes
# When you do this you have to manually pass in the instance as an argument
Employee.fullname(emp1)

# %%

# Class variables

class Employee:  
    
    raise_amount = 1.04
    
    def __init__(self, first, last, pay): # all classes and functions need a colon
        self.first = first  # Creates the variable first. It is assigned to the instance self, and will take the value first as input into the instance
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@gmail.com'
        
    def fullname(self):
        return '{} {}'.format(self.first, self.last)
    
    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount) # pay now takes a new value!
      
emp1= Employee('Cory', 'Smith', 50000)        
      
print(emp1.pay)
emp1.apply_raise()
print(emp1.pay)

print(emp1.__dict__) # dict is a built in python method like init
# This will return all the attributes associated with the object emp1 (which is an instance of the class Employee)
print(Employee.__dict__)


# What happens when we want to edit raise_amount?

Employee.raise_amount = 1.05

print(Employee.raise_amount) #check it works by referring to the class
print(emp1.raise_amount) #check it works by referring to the instance of the class

print(emp1.pay)
emp1.apply_raise()
print(emp1.pay)

# %%

# Dictionaries are used to store data. This can either be done independantly or using classes if you have lots of structured data to define 

# Dictionaries are used to store data values in key:value pairs.

# Independently
dogs = [
    {"name": "Rex", "age": 5, "breed": "Golden Retriever"},
    {"name": "Bella", "age": 3, "breed": "Beagle"},
    {"name": "Max", "age": 7, "breed": "Labrador"}
]

print(dogs[1]["name"])  # Output: Bella


# Using classes

class Dog:                                  
    def __init__(self, name, age, breed):
        self.name = name
        self.age = age
        self.breed = breed
    
    def bark(self):
        print(f"{self.name} says Woof!")

# Create dog objects
dog1 = Dog("Rex", 5, "Golden Retriever")
dog2 = Dog("Bella", 3, "Beagle")

# Put dogs in a list
dogs = [dog1, dog2]

dogs[0].bark()  # Output: Rex says Woof!

# %%

class Dog:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        return f"Woof! I'm {self.name}" # return lets you use the result rather than just print it

    def print_hello(self):
        print(f"Woof! I'm {self.name}")

dog1 = Dog('Millie')
dog1.say_hello()
dog1.print_hello()
