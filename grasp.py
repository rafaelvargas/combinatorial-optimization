from sys import argv

from functions import greedy_randomized, local_search, checking
from file_io import file_reading, file_writing

def grasp(num_vertices, num_groups, groups_limits, vertices_weights, edges):
    groups = greedy_randomized(1, num_vertices, num_groups, groups_limits, vertices_weights, edges)
    groups = local_search(50, groups, edges, groups_limits)
    return groups

def main(argv):
    filename = argv[1]
    num_vertices, num_groups, groups_limits, vertices_weights, edges = file_reading(filename)
    groups = grasp(num_vertices, num_groups, groups_limits, vertices_weights, edges)
    score = checking(groups, edges)
    file_writing(filename, groups, score)


if __name__ == "__main__":
    main(argv)