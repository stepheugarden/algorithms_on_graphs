# Uses python3

import os
import re
import sys
from utilities import read_test_cases


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


def is_sink(not_used):
    return len(not_used) == 0


def toposort(adj):
    used = [False] * len(adj)
    order = []

    def follow_edges(vertex):
        not_used = [vert for vert in adj[vertex] if not used[vert]]
        if is_sink(not_used):
            used[vertex] = True
            order.append(vertex)
            return

        for vert in not_used:
            if used[vert]:
                continue
            follow_edges(vert)

        follow_edges(vertex)

    for vert in range(len(adj)):
        if used[vert]:
            continue
        follow_edges(vert)

    return list(reversed(order))


def check_topological_order(adj, order):
    while len(order) > 0:
        vertex = order.pop()
        dest = set(adj[vertex])
        for prev in order:
            if prev in dest:
                print(f"{vertex} is reachable from {prev}, i.e. no valid ordering")
                return False
    return True


INTERACTIVE = False

if __name__ == "__main__":
    if INTERACTIVE:
        input = sys.stdin.read()
        data = list(map(int, input.split()))
        adj = create_adjacency_list(data)
        res = toposort(adj)
        for x in res:
            print(x + 1, end=" ")
    else:
        path, files = read_test_cases.return_path_files()
        for file in files:
            file_path = os.path.join(path, file)
            adj = parse_input(file_path)
            order = toposort(adj)
            res = " ".join([str(r + 1) for r in order])

            assert check_topological_order(adj, order), f"Error in {file=}"
            print(f"topological order of {file}: {res}")
