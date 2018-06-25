from random import randint, seed
from copy import deepcopy


# Sort edges by their values
def construct_candidate_set(edges):
    return sorted(edges, key=lambda edge: edge[2], reverse=True)


# Check if a vertex is in another group
def in_another_group(groups, current_group, vertex):
    in_group = False
    for i in range(0, len(groups)):
        if (i != current_group):
            if (vertex in groups[i][0]):
                in_group = True
    return in_group


# Generates a restricted list of candidates
def generate_rcl(size, group_vertices, edges, num_vertices, groups,
                 current_group):
    # Initialize costs array
    costs = [[i, 0.0] for i in range(0, num_vertices)]

    for i in range(0, len(edges)):
        for v in group_vertices:
            if (v == edges[i][0] and
                    not in_another_group(groups, current_group, edges[i][1])
                    and (edges[i][1] not in group_vertices)):
                costs[edges[i][1]][1] = costs[edges[i][1]][1] + edges[i][2]
            if (v == edges[i][1] and
                    not in_another_group(groups, current_group, edges[i][0])
                    and (edges[i][0] not in group_vertices)):
                costs[edges[i][0]][1] = costs[edges[i][0]][1] + edges[i][2]
    s_costs = sorted(costs, key=lambda cost: cost[1], reverse=True)
    return s_costs[:size]


def check_group_value(groups, edges):
    current = 0.0
    for g in groups:
        for e in edges:
            if ((e[0] in g[0]) and (e[1] in g[0])):
                current = current + e[2]
    return current


def greedy_randomized(rcl_size, num_vertices, num_groups, groups_limits,
                      vertices_weights, edges):
    # Initialize groups -> [vertices , weights]
    groups = [[[], []] for i in range(0, num_groups)]

    seed()
    # Insert random initial vertices
    is_not_valid = True
    for g, gl, i in zip(groups, groups_limits, range(0, num_groups)):
        while (is_not_valid):
            random_vertex = randint(0, num_vertices - 1)
            if (not in_another_group(groups, i, random_vertex)):
                g[0].append(random_vertex)
                g[1].append(vertices_weights[random_vertex])
                is_not_valid = False
        is_not_valid = True

    seed()
    # Insert vertices in groups until partial weight passes inferior limit
    current_value = 0.0
    for g, gl, i in zip(groups, groups_limits, range(0, num_groups)):
        rcl = generate_rcl(rcl_size, g[0], edges, num_vertices, groups, i)
        random_candidate = randint(0, len(rcl) - 1)
        while (sum(g[1]) < gl[0]):
            g[0].append(rcl[random_candidate][0])
            g[1].append(vertices_weights[rcl[random_candidate][0]])
            current_value = current_value + rcl[random_candidate][1]
            rcl = generate_rcl(rcl_size, g[0], edges, num_vertices, groups, i)

    seed()
    # Complete groups with the remaining vertices
    v_sums = 0
    while (num_vertices > v_sums):
        v_sums = 0
        for g, gl, i in zip(groups, groups_limits, range(0, num_groups)):
            vertex_inserted = True
            while (sum(g[1]) < gl[1] and vertex_inserted):
                rcl = generate_rcl(rcl_size, g[0], edges, num_vertices, groups,
                                   i)
                random_candidate = randint(0, len(rcl) - 1)
                if (sum(g[1]) + vertices_weights[rcl[random_candidate][0]] <=
                        gl[1] and not (rcl[random_candidate][0] in g[0])
                        and not in_another_group(groups, i,
                                                 rcl[random_candidate][0])):
                    g[0].append(rcl[random_candidate][0])
                    g[1].append(vertices_weights[rcl[random_candidate][0]])
                    current_value = current_value + rcl[random_candidate][1]
                else:
                    vertex_inserted = False

            #print("Group " + str(i) + " -> " + str(g[0]))
            v_sums = v_sums + len(g[0])
    # print("Total num. vertices: " + str(v_sums))
    # print("Expected num. vertices: " + str(num_vertices))
    print("Initial solution score: " + str(current_value))

    return groups


def local_search(K, groups, edges, groups_limits):

    old_score = check_group_value(groups, edges)
    best_sol = deepcopy(groups)
    best_score = old_score
    improved = True
    while (improved):
        improved = False
        for i in range(K):
            seed()
            # Define random insertion and removing groups
            insert_group, remove_group = 0, 0
            while (insert_group == remove_group):
                remove_group = randint(0, len(groups) - 1)
                insert_group = randint(0, len(groups) - 1)

            # Define random vertices from remove group
            random_vertex = randint(0, len(groups[remove_group][0]) - 1)

            # Create a copy from groups
            modified_groups = deepcopy(groups)

            modified_groups[insert_group][0].append(
                groups[remove_group][0][random_vertex])
            modified_groups[insert_group][1].append(
                groups[remove_group][1][random_vertex])

            del modified_groups[remove_group][0][random_vertex]
            del modified_groups[remove_group][1][random_vertex]
            if (sum(modified_groups[remove_group][1]) >=
                    groups_limits[remove_group][0]
                    and sum(modified_groups[insert_group][1]) <=
                    groups_limits[insert_group][1]):
                new_score = check_group_value(modified_groups, edges)

                if (new_score > best_score):
                    #print("new score: " + str(new_score))
                    best_score = new_score
                    best_sol = modified_groups
                    improved = True
        if (improved):
            print("New local optimum found: " + str(best_score))
            groups = best_sol

    return groups