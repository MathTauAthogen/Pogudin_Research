"""Find attractors using the other new method discussed at the meeting on 6/3/18"""

import numpy as np
import pyximport
pyximport.install()

cdef dfs(int vertex, int old_v, graph, visited, the_vars):
    """Standard DFS with a twist that you can't go back in the direction you were just going in. Now with less recursion!"""
    visited[vertex] = 1
    the_vars["basin size"] = the_vars["basin size"] + 1
    cdef int old_count = 0
    cdef int i
    for i in graph[vertex]:
        if i == vertex:
            the_vars["attractor piece"] = i
        elif i == old_v:
            old_count += 1
            if old_count == 2:
                the_vars["attractor piece"] = old_v
        else:
            if visited[i] == 1:
                the_vars["attractor piece"] = i
            else:
                dfs(i, vertex, graph, visited, the_vars)

def to_state_function(functions):
    """Converts a numpy matrix of functions to a state function"""
    temp = np.matrix(functions).T
    power_vector = np.power(2, np.arange(temp.shape[1] - 1, -1, -1)).T
    return np.dot(temp, power_vector)[0, :].tolist()[0]

cdef to_graph(state_function):
    """Converts a state function to a graph"""
    graph = [[] for _ in range(len(state_function))]
    for i, val in enumerate(state_function):
        graph[i].append(val)
        graph[val].append(i)
    return graph

def find_attractors_and_basins(functions):
    """Find the attractors and basins of a DDS with f_i = functions[i]
    Input notes:
    functions is a numpy matrix that is just the matrix version of a list of functions
    in list form
    Output notes:
    A list of tuples is output where the first element is the size of the attractor and
    the second the size of the corresponding basin"""
    state_function = to_state_function(functions)
    graph = to_graph(state_function)
    a_and_b_tuples = []
    visited = [0] * len(state_function)
    for i in range(len(state_function)):
        if visited[i] == 1:
            continue
        the_vars = {"basin size" : 0, "attractor piece" : -1}
        dfs(i, -1, graph, visited, the_vars)
        attractor_length = 1
        point_on_attractor = the_vars["attractor piece"]
        move = state_function[point_on_attractor]
        while move != point_on_attractor:
            move = state_function[move]
            attractor_length += 1
        a_and_b_tuples.append([attractor_length, the_vars["basin size"]])
    return a_and_b_tuples
