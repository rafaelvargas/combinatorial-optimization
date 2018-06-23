from file_reading import file_reading

# Sort edges by their values
def construct_candidate_set(edges):
    return sorted(edges, key=lambda edge: edge[2])



num_vertices, num_groups, groups_limits, vertices_weights, edges = file_reading("gbmv480_04.ins")
print(edges)


