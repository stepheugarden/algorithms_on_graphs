# Uses python3

import sys


# Uses python3

import sys
import os
import re
from utilities import read_test_cases

reached = set()


def explore(adj, start):
    reached.add(start)

    for node in adj[start]:
        if node in reached:
            continue
        explore(adj, node)


def number_of_components(adj):
    result = 0
    for node in range(len(adj)):
        if node in reached:
            continue
        result += 1
        explore(adj, node)

    return result


INTERACTIVE = False


def create_adjacency_list(data):
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0 : (2 * m) : 2], data[1 : (2 * m) : 2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    return adj


def parse_input(file_path):
    data = list(map(int, re.split("\s|\n", open(file_path).read())))
    return create_adjacency_list(data)


if __name__ == "__main__":

    if INTERACTIVE:
        input = sys.stdin.read()
        data = list(map(int, input.split()))
        adj = create_adjacency_list(data)
        print(number_of_components(adj))
    else:
        path, files = read_test_cases.return_path_files(
            "week1_graph_decomposition1", "1_finding_exit_from_maze"
        )
        for file in files:
            reached = set()
            reached_finish = False
            file_path = os.path.join(path, file)
            adj = parse_input(file_path)
            res = number_of_components(adj)
            sol = int(open(file_path + ".a").read())

            assert sol == res, f"Error in {file=}"
            print(f"connected components in {file}: {res}")
