# Uses python3

import os
import re
import sys
from utilities import read_test_cases

sys.setrecursionlimit(200000)


def parse_input(file_path):
    data = list(map(int, re.split("\s|\n", open(file_path).read())))
    return create_adjacency_list(data)


def create_adjacency_list(data):
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0 : (2 * m) : 2], data[1 : (2 * m) : 2]))
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a - 1].append(b - 1)
    return adj


def number_of_strongly_connected_components(adj):
    result = 0
    component = [None] * len(adj)

    def follow_edges(from_vertex, connected_component_num):
        next_vertices = adj[from_vertex]

        # is sink
        if len(next_vertices) == 0:
            return

        # already visited
        if component[from_vertex] is not None:
            return

        component[from_vertex] = connected_component_num

        for next_vertex in next_vertices:
            follow_edges(next_vertex, connected_component_num)

    for vertex in range(len(adj)):
        if component[vertex] is not None:
            continue
        result += 1
        follow_edges(vertex, result)

    return result


INTERACTIVE = False

if __name__ == "__main__":
    if INTERACTIVE:
        input = sys.stdin.read()
        data = list(map(int, input.split()))
        adj = create_adjacency_list(data)
        res = number_of_strongly_connected_components(adj)
        for x in res:
            print(x + 1, end=" ")
    else:
        path, files = read_test_cases.return_path_files(
            "week2_graph_decomposition2", "3_intersection_reachability"
        )
        for file in files:
            file_path = os.path.join(path, file)
            adj = parse_input(file_path)
            res = number_of_strongly_connected_components(adj)
            sol = int(open(file_path + ".a").read())

            assert sol == res, f"Error in {file=}"
            print(f"number of connected components in {file}: {res}")
