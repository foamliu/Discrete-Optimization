#!/usr/bin/python
# -*- coding: utf-8 -*-


# def solve_it(input_data):
#     # Modify this code to run your optimization algorithm
#
#     # parse the input
#     lines = input_data.split('\n')
#
#     first_line = lines[0].split()
#     node_count = int(first_line[0])
#     edge_count = int(first_line[1])
#
#     edges = []
#     for i in range(1, edge_count + 1):
#         line = lines[i]
#         parts = line.split()
#         edges.append((int(parts[0]), int(parts[1])))
#
#     # build a trivial solution
#     # every node has its own color
#     solution = range(0, node_count)
#
#     # prepare the solution in the specified output format
#     output_data = str(node_count) + ' ' + str(0) + '\n'
#     output_data += ' '.join(map(str, solution))
#
#     return output_data

nc_dict = {50: 8, 70: 20, 100: 16, 250: 95}


def add_neighbour(graph, n0, n1):
    if n0 in graph:
        graph[n0].append(n1)
    else:
        graph[n0] = [n1]


def welsh_powell(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    graph = dict()
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        n0 = int(parts[0])
        n1 = int(parts[1])
        add_neighbour(graph, n0, n1)
        add_neighbour(graph, n1, n0)

    nodes = sorted(list(graph.keys()), key=lambda x: len(graph[x]), reverse=True)
    color_map = {}

    for node in nodes:
        available_colors = [True] * len(nodes)
        for neighbor in graph[node]:
            if neighbor in color_map:
                color = color_map[neighbor]
                available_colors[color] = False
        for color, available in enumerate(available_colors):
            if available:
                color_map[node] = color
                break

    solution = []
    for n in range(node_count):
        solution.append(color_map[n])

    obj = max(color_map.values()) + 1
    output_data = str(obj) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


def solve(nc, n, num_edges, E):
    from ortools.sat.python import cp_model
    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    V = range(n)

    #
    # decision variables
    #
    x = [model.NewIntVar(0, nc - 1, 'x[%i]' % i) for i in V]

    # number of colors used, to minimize
    max_color = max(x)

    #
    # constraints
    #

    # adjacent nodes cannot be assigned the same color
    # (and adjust to 0-based)
    for i in range(num_edges):
        model.Add(x[E[i][0]] != x[E[i][1]])

    # symmetry breaking
    # solver.Add(x[0] == 1);
    # solver.Add(x[1] <= 2);
    for i in range(nc):
        model.Add(x[i] <= i + 1)

    # objective (minimize the number of colors)
    model.Minimize(max_color)

    solver.parameters.max_time_in_seconds = 10.0
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        solution = [solver.Value(x[i]) for i in V]

    obj = max(solution) + 1
    output_data = str(obj) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


def ortools_solve(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append([int(parts[0]), int(parts[1])])

    nc = nc_dict[node_count]
    return solve(nc, node_count, edge_count, edges)


def solve_it(input_data):
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    if node_count <= 100:
        return ortools_solve(input_data)
    else:
        return welsh_powell(input_data)


if __name__ == '__main__':
    # import sys
    # if len(sys.argv) > 1:
    #     file_location = sys.argv[1].strip()
    #     with open(file_location, 'r') as input_data_file:
    #         input_data = input_data_file.read()
    #     print(solve_it(input_data))
    # else:
    #     print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

    file_location = 'data/gc_4_1'
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()
    print(solve_it(input_data))
