def file_reading(filename):
    path = "problem-instances/" + filename
    file = open(path, 'r')
    
    # Get number of vertices and groups
    first_line = file.readline().split(' ')
    num_vertices = int(first_line[0])
    num_groups = int(first_line[1])

    # Get limits of the groups
    second_line = file.readline().split(' ')
    groups_limits = []
    for i in range(0, num_groups * 2, 2):
        groups_limits.append((int(second_line[i]), int(second_line[i+1])))

    # Get vertices weights
    third_line = file.readline().split(' ')
    vertices_weights = []
    for i in range(0, num_vertices):
        vertices_weights.append(int(third_line[i]))

    # Get edges
    remaining_lines = file.readlines()
    edges = []
    for i in range(0, len(remaining_lines)):
        current_line = remaining_lines[i].split(' ')
        edges.append((int(current_line[0]), int(current_line[1]), float(current_line[2].replace('\n', ''))))
    
    file.close()

    return num_vertices, num_groups, groups_limits, vertices_weights, edges

def file_writing(filename, groups, score):
    file = open("results/" + filename + ".txt", 'w')
    file.write(str(score) + "\n")
    for g in groups:
        file.write(str(g[0]) + "\n")