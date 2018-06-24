from random import shuffle, randint

from file_reading import file_reading

# Sort edges by their values
def construct_candidate_set(edges):
    return sorted(edges, key=lambda edge: edge[2], reverse = True)

# Check if a vertex is in another group
def in_another_group(groups, current_group, vertex):
    in_group = False
    for i in range(0, len(groups)):
        if(i != current_group):
            if(vertex in groups[i][0]):
                in_group = True
    return in_group

# Generates a restricted list of candidates
def generate_rcl(group_vertices, edges, num_vertices, groups, current_group):
    costs = [[i, 0.0] for i in range(0, num_vertices)]
    for i in range(0, len(edges)):
        for v in group_vertices:
            if(v == edges[i][0] and not in_another_group(groups, current_group, edges[i][1])
                and (edges[i][1] not in group_vertices)):
                costs[edges[i][1]][1] = costs[edges[i][1]][1] + edges[i][2]
            if(v == edges[i][1] and not in_another_group(groups, current_group, edges[i][0]) 
                and (edges[i][0] not in group_vertices)):
                costs[edges[i][0]][1] = costs[edges[i][0]][1] + edges[i][2]
    s_costs = sorted(costs, key=lambda cost: cost[1], reverse = True)
    return s_costs
        
                
def checking(groups, edges):
    current = 0.0
    for g in groups:
        for e in edges:
            if((e[0] in g[0]) and (e[1] in g[0])):
                current = current + e[2]
    print("Final value: " + str(current))


def greedy(num_vertices, num_groups, groups_limits, vertices_weights, edges):
    # Initialize groups -> vertices / weights / edges
    groups = [[[], []] for i in range(0, num_groups)]

    # Insert random initial vertices
    is_not_valid = True
    for g, gl, i in zip(groups, groups_limits, range(0, num_groups)):
        while(is_not_valid):
            random_vertex = randint(0, num_vertices-1)
            if(not in_another_group(groups, i, random_vertex)):
                g[0].append(random_vertex)
                g[1].append(vertices_weights[random_vertex])
                is_not_valid = False
        is_not_valid = True
    
    # Insert vertices in groups until partial weight passes inferior limit
    current_value = 0.0
    for g, gl, i in zip(groups, groups_limits, range(0, num_groups)):
        rcl = generate_rcl(g[0], edges, num_vertices, groups, i)
        while(sum(g[1]) < gl[0]):
            g[0].append(rcl[0][0])
            g[1].append(vertices_weights[rcl[0][0]])
            current_value = current_value + rcl[0][1]
            rcl = generate_rcl(g[0], edges, num_vertices, groups, i)

    # Complete groups with the remaining vertices
    v_sums = 0
    for g, gl, i in zip(groups, groups_limits, range(0, num_groups)):
        vertex_inserted = True
        while(sum(g[1]) < gl[1] and vertex_inserted):
            rcl = generate_rcl(g[0], edges, num_vertices, groups, i)
            if(sum(g[1]) + vertices_weights[rcl[0][0]] < gl[1] and not(rcl[0][0] in g[0]) and rcl[0][1] != 0.0):
                g[0].append(rcl[0][0])
                g[1].append(vertices_weights[rcl[0][0]])
                current_value = current_value + rcl[0][1]
            else:
                vertex_inserted = False
    
        v_sums = v_sums + len(g[0])
        print("Group " + str(i) + " -> " + str(g[0]))
    print("Total weight: " + str(v_sums))
    print("Expected weight: " + str(num_vertices))
    print("Score: " + str(current_value))



# tests
num_vertices, num_groups, groups_limits, vertices_weights, edges = file_reading("gbmv240_01.ins")
greedy(num_vertices, num_groups, groups_limits, vertices_weights, edges)


