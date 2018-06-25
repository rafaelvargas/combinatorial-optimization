from sys import argv
from time import time

from functions import greedy_randomized, local_search, check_group_value
from file_io import file_reading, file_writing
from copy import deepcopy


def grasp(parameters, num_vertices, num_groups, groups_limits,
          vertices_weights, edges):
    # Parameters
    num_iter = int(parameters[0])
    restricted_candidate_list_size = int(parameters[1])
    num_local_iter = int(parameters[2])
    
    # Current best value
    best_value = 0.0

    # Getting time elapsed
    start = time()

    for i in range(int(num_iter)):
        print("GRASP iteration - " + str(i))
        groups = greedy_randomized(restricted_candidate_list_size, num_vertices, num_groups,
                                    groups_limits, vertices_weights, edges)
        initial_solution = deepcopy(groups)
        groups = local_search(num_local_iter, groups, edges, groups_limits)
        new_value = check_group_value(groups, edges)
        if (new_value > best_value):
            best_solution = deepcopy(groups)
            best_initial_solution = deepcopy(initial_solution)
            best_value = new_value

    end = time()
    time_elapsed = end - start
    
    return best_solution, best_initial_solution, time_elapsed


def main(argv):
    filename = argv[1]
    parameters = argv[2:]
    num_vertices, num_groups, groups_limits, vertices_weights, edges = file_reading(
        filename)
    groups, initial_groups, time_elapsed = grasp(parameters, num_vertices, num_groups, groups_limits,
                   vertices_weights, edges)
    score = check_group_value(groups, edges)
    initial_score = check_group_value(initial_groups, edges)
    file_writing(filename, groups, score, initial_score, time_elapsed, parameters)


if __name__ == "__main__":
    # Arguments given are filename | num. of grasp iter. | RCL size | num. of local search iter.
    main(argv)