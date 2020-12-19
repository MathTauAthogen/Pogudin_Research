"""Generates a random noncanalysing function."""

#Import statements
import math
import random
import pyximport; pyximport.install()
import discrete_dynamical_system as dds

#Boilerplates

def rand_string(length):
    """Genererates a random binary string of length length.
    Output format notes:
    Outputs a list representing a binary string.
    """
    k = random.randint(0, 2 ** length - 1)
    return map(int, list(dds.binary_fixed_length(k, length)))

def near_rand_string(length, exceptions):
    """Generates a random binary string of length length that is not any of the exceptions.
    Input format notes:
    exceptions as a list of lists representing binary strings.
    Output format notes:
    Outputs a list representing a binary string."""
    string = rand_string(length)
    while True:
        try:
            _ = exceptions.index(string)
            string = rand_string(length)
        except ValueError:
            break
    return string

def get_first_vals_list(num, val):
    """Generates a list of lists denoting when the variable number list-index is val."""
    num = 2 ** num
    my_rows = []
    for k in range(num):
        my_rows.append(list(
            [int(i) for i in dds.binary_fixed_length(k, int(math.log(num, 2)))]))
    outerlist = []
    for i in range(int(math.log(num, 2))):
        innerlist = []
        for j in range(num):
            if my_rows[j][i] == val:
                innerlist.append(j)
        outerlist.append(innerlist)
    return outerlist

def is_uniform(my_list):
    """Checks to see if a list only consists of one distinct element."""
    try:
        initial = my_list[0]
        for _, val in enumerate(my_list):
            if val != initial:
                return False
        return True
    except IndexError:
        return False #Needed specifically for this program to default here

def random_int_with(length, conditions):
    """Generate a random binary string with length length and that fits the condtions.
    Input format notes:
    conditions is an array of length length composed of 0, 1, and -1, where if the
    value at some index is not -1, the value of the output at that index has to be the given value.
    Output format notes:
    Outputs a list representing a binary string."""
    #Please try to make this better.
    temp = [0] * length
    #while is_uniform(temp):
    temp = conditions[:]
    for i, val in enumerate(temp):
        if val == -1:
            temp[i] = random.randint(0, 1)
    return temp

def merge_at(initial, offset_list, at_list):
    """Writes the elements of offset_list into inital at the locations in at_list."""
    for i, val in enumerate(offset_list):
        index = at_list[i]
        initial[index] = val

def overwrite_at(my_list, index, seq):
    """Overwrites elements my_list starting from index using seq as a template"""
    for i, val in enumerate(seq):
        my_list[index + i] = val

def is_canalizing(table, var):
    """Checks whether var (counting from the right) is a canalizing for a function given by the table"""
    io_pairs_seen = {}
    for i in range(len(table)):
        inp = (i >> var) % 2
        io_pairs_seen[table[i] * 2 + inp] = 1
        if len(io_pairs_seen) == 4:
            return False
    return len(io_pairs_seen) < 4

def is_canalizing_function(table):
    for var in range(len(table)):
        if is_canalizing(table, var):
            return True
            break
    return False

def find_canalizing_depth(table):
    depth = 0
    for var in range(len(table)):
        new_table = table[var:]
        if is_canalizing(new_table, len(table)-1-var):
            depth = depth +1
        if is_canalizing_function(table[var+1:]) == False:
            break
    return depth





#Main function
def random_noncanalysing_func(num_vars):
    """Generates a random non-canalysing function on num_vars variables.
    Output format notes:
    It outputs a class with the format we agreed upon.
    """
    ready = False
    while not ready:
        table = [random.getrandbits(1) for _ in xrange(2 ** num_vars)]
        ready = True
        for i in range(num_vars):
            if is_canalizing(table, i):
                ready = False
        if is_uniform(table):
            ready = True
    return dds.Truth(table)



if __name__ == "__main__":
    print(random_noncanalysing_func(3).return_truth_table())
