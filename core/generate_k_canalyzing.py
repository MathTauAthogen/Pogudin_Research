"""Program for generating random k-canalyzing functions"""
import random
import random_partition
import pyximport; pyximport.install()
import discrete_dynamical_system as dds
import random_noncanalysing as rn

def all_numbers_but(exceptions, maxn):
    """Generates a list of all ints besides exceptions less than maxn."""
    k = range(maxn)
    temp = []
    for i in k:
        if i not in exceptions:
            temp.append(i)
    return temp

def find_canalizing_depth( ):


def random_k_canalyzing(num_vars, depth):
    """Method to generate a random k-canalyzing function"""
    if depth == 0:
        return rn.random_noncanalysing_func(num_vars)
    b = random.randint(0, 1)
    variables = range(num_vars)
    canalyzing = random_partition.random_subset(variables, depth)
    non_canalyzing = all_numbers_but(canalyzing, num_vars)
    M_i = random_partition.random_partition(canalyzing)
    offsets = [random.randint(0, 1) for _ in range(depth)]
    core = rn.random_noncanalysing_func(len(non_canalyzing))
    core_table = core.return_truth_table()
    if core_table[0] == 0 and rn.is_uniform(core_table):
        return random_k_canalyzing(num_vars, depth)
    if len(M_i[-1]) == 1 and len(M_i) != 1 and core_table[0] == 1 and rn.is_uniform(core_table):
        return random_k_canalyzing(num_vars, depth)
    if b == 1 and len(M_i[-1]) == 1 and len(M_i) == 1 and core_table[0] == 1 and rn.is_uniform(core_table):
        return random_k_canalyzing(num_vars, depth)

    ####
    def evaluator_non_core(a):
        """Method for evaluating the non core part of the function to create a truth table"""
        start = 0
        for i, subset in enumerate(M_i):
            for j in subset:
                if ((a >> (num_vars - j - 1)) % 2) == offsets[start]:
                    return (b + i) % 2
                start += 1
        return 2
    ####   

    result = [0] * (2 ** num_vars)
    core_values_seen = 0
    core_extra = (b + len(M_i) + 1) % 2
    for a in xrange(2 ** num_vars):
        result[a] = evaluator_non_core(a)
        if result[a] == 2:
            result[a] = core_table[core_values_seen] ^ core_extra
            core_values_seen += 1

    return dds.Truth(result)
