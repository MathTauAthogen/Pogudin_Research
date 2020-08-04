"""
This is my boilerplate code.
"""

import math
import numpy as np

def binary_not(val):
    """Does the binary not operation on val."""
    if val == 1:#pylint: disable=no-else-return
        return 0
    else:
        return 1

def remove(my_list, element):
    """ Removes all instances of element from my_list"""
    try:
        index = my_list.index(element)
        my_list.pop(index)
        remove(my_list, element)
    except ValueError:
        pass

def binary(my_int):
    """Returns the binary representation of my_int as a string."""
    return "{0:b}".format(my_int)


def binary_fixed_length(my_int, length):
    """ Returns a zero-padded (of length length) binary representation of my_int"""
    return binary(my_int).zfill(length)

def invert(strings, length):
    """Outputs a list of all of the binary strings with length digits that aren't in strings."""
    temp = []
    for k in range(2**(length - 1)):
        test = list([int(i) for i in binary_fixed_length(k, length)])
        if test not in strings:
            temp.append(test)
    return temp

class Truth(object):
    """This is how I store functions."""
    def __init__(self, table):
        self.table = table
        self.num = len(self.table)
        if math.log(self.num, 2).is_integer():
            pass
        else:
            raise Exception(
            	   "No. Just no. You have to pass in a function representation of valid length!")

        self.my_rows = []

        for k in range(self.num):
            self.my_rows.append(list(
            	   [int(i)for i in binary_fixed_length(k, int(math.log(self.num, 2)))]))

    def function_format(self, row):  #returns -1 upon failure or else the correct 0 or 1 value.
        """Plug in a row to get the corresponding value of the function"""
        try:
            i = self.my_rows.index(row)
            return self.table[i]
        except ValueError:
            return -1

    def return_truth_table(self):
        """ Get the truth table in our agreed-upon format."""
        return self.table

class Dynamical(object):
    """The class that stores the discrete dynamical system"""
    def __init__(self, initial, functions):
        self.functions = functions
        self.current = initial
        #temp = map(list, zip(*functions))
        temp = np.matrix(functions).T
        power_vector = np.power(2, np.arange(temp.shape[1] - 1, -1, -1)).T
        self.states = np.dot(temp, power_vector)[0,:].tolist()[0]
        #print(self.states)

    def iterate(self):
        """ Increases the time by 1"""
        self.current = self.states[self.current]

    def placeholder(self):
        """ Not enough public methods otherwise"""
        pass


def generate_boolean_functions(length):
    rows = [] """rows"""
    functionvalues = [] """ values"""
    for j in range(2**length):
            rows.append(list(
            	   [int(i)for i in binary_fixed_length(j,length)]))
            functionvalues.append(0)
            rows.append(list(
            	   [int(i)for i in binary_fixed_length(j,length)]))
            functionvalues.append(1)
    """appended twice as it can be 0 or 1 """

    return  rows, functionvalues
    """ith element of functionvalues is the value for the ith element of row"""



