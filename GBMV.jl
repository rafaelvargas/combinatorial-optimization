using JuMP
using GLPKMathProgInterface

m = Model(solver=GLPKSolverMIP(tm_lim=1))

# Should have instance filename
file = open("instances/gbmv240_01.ins")
lines = readlines(arq)

line = split(lines[1])
num_vertices = parse(Int64, line[1])
num_groups = parse(Int64, line[2])

line = split(lines[2])
inferior_limit = Array{Int64}(num_groups)
superior_limit = Array{Int64}(num_groups)
for g = 1:num_groups
    inferior_limit[g] = parse(Int64, line[2*g - 1])
    superior_limit[g] = parse(Int64, line[2*g])
end    

line = split(lines[3])
vertices = Array{Int64}(num_vertices)
for v in 1:num_vertices
    vertices[v] = parse(Int64, line[v])
end

edges = zeros(Float64, num_vertices, num_vertices)
for l = 4:length(lines)
    line = split(lines[l])
    origin = parse(Int64, line[1]) + 1
    destiny = parse(Int64, line[2]) + 1
    weight = parse(Float64, line[3])
    edges[origin, destiny] = weight
end

@variable(m, groups[1:num_groups, 1:num_vertices], Bin)
@variable(m, vertices_connected[1:num_groups, 1:num_vertices, 1:num_vertices], Bin)

@objective(m, Max, sum(vertices_connected[g, v1, v2]*edges[v1, v2]
                      for v1 in 1:num_vertices, v2 in v1:num_vertices, g in 1:num_groups))

@constraints(m, begin [g in 1:num_groups],
                      sum(vertices[v]*groups[g, v]
                      for v in 1:num_vertices) >= inferior_limit[g]
                end)

@constraints(m, begin [g in 1:num_groups],
                      sum(vertices[v]*groups[g, v]
                      for v in 1:num_vertices) <= superior_limit[g]
                end) 

@constraints(m, begin [v in 1:num_vertices],
                      sum(groups[g, v]
                      for g in 1:num_groups) == 1
                end)
                
@constraints(m, begin [v1 in 1:num_vertices, v2 in v1:num_vertices, g in 1:num_groups],
                      vertices_connected[g, v1, v2] <= (groups[g, v1] + groups[g, v2])/2
                end)
                
@constraints(m, begin [v1 in 1:num_vertices, v2 in v1:num_vertices, g in 1:num_groups],
                      vertices_connected[g, v1, v2] >= groups[g, v1] + groups[g, v2] - 1
                end)

solve(m)
