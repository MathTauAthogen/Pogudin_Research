import unittest
import pyximport
pyximport.install()
import numpy as np
from math import *
import sys
sys.path.insert(0, '../../core')
import discrete_dynamical_system as dds 
import generate_k_canalyzing as gkc 

def generate_boolean_functions(length):
    rows = [] 
    functionvalues = []
    for j in range(2**length):
            rows.append(list([int(i)for i in dds.binary_fixed_length(j,length)]))
            functionvalues.append(0)
            rows.append(list([int(i)for i in dds.binary_fixed_length(j,length)]))
            functionvalues.append(1)
    return  rows, functionvalues


def find_canalizing_depth(table):
    depth = 0
    for var in range(len(table)):
        new_table = table[var:]
        if gkc.is_canalizing(new_table, len(table)-1-var):
            depth = depth +1
        if gkc.is_canalizing_function(table[var+1:]) == False:
            break
    return depth

class Test(unittest.TestCase):
    def setUp(self): 
        pass

    def test_boolean_functions(self): 
        n = 10 
        (rows, functionvalues) = generate_boolean_functions(n)

        flag = True 

        if len(rows) != 2**(2**n): 
            flag = False 

        """ check whether number of boolean functions are correct """

        self.assertEqual (flag, True)

    def test_find_canalyzing_depth(self):
        num_vars = 10 
        depth = 5 

        flag = True 
        table = gkc.random_k_canalyzing(num_vars,depth)

        if find_canalizing_depth(table) != depth:
            flag = False
        
        self.assertEqual (flag, True)
  
if __name__ == '__main__':
    unittest.main()
