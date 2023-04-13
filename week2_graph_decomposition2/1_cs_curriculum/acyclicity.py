# Uses python3

import os
import re
import sys
from utilities import read_test_cases


def create_adjacency_list(data):
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0 : (2 * m) : 2], data[1 : (2 * m) : 2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    return adj


def parse_input(file_path):
    data = list(map(int, re.split("\s|\n", open(file_path).read())))
    return create_adjacency_list(data)


def acyclic(adj):
    visited = [False] * len(adj)
    has_cycle = False

    # recursively follow paths
    def follow_edges(vertex, has_cycle):
        if visited[vertex]:
            has_cycle = True
            return has_cycle
        visited[vertex] = True

        for vert in adj[vertex]:
            has_cycle = follow_edges(vert, has_cycle)
        visited[vertex] = False

        return has_cycle

    for vert in range(len(adj)):
        if has_cycle:
            break
        if len(adj[vert]) > 0:
            has_cycle = follow_edges(adj[vert][0], has_cycle)

    return 1 if has_cycle else 0


INTERACTIVE = False

if __name__ == "__main__":

    if INTERACTIVE:
        input = sys.stdin.read()
        data = list(map(int, input.split()))
        adj = create_adjacency_list(data)
        print(acyclic(adj))
    else:
        path, files = read_test_cases.return_path_files(
            "week2_graph_decomposition2", "1_cs_curriculum"
        )
        for file in files:
            file_path = os.path.join(path, file)
            adj = parse_input(file_path)
            res = acyclic(adj)
            sol = int(open(file_path + ".a").read())

            assert sol == res, f"Error in {file=}"
            print(f"{file} is DAG: {res == 0}")
