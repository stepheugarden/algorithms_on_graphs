# Uses python3

import sys
import os
import re
from utilities import read_test_cases

reached = set()
reached_finish = False


def explore(adj, start, finish):
    reached.add(start)
    global reached_finish

    if start == finish:
        reached_finish = True

    for node in adj[start]:
        if reached_finish:
            return 0
        if node in reached:
            continue
        explore(adj, node, finish)


def reach(adj, x, y):
    if min([len(adj[x]), len(adj[y])]) == 0:
        # if x or y is not connected to any other vertices there will be no path
        return 0

    # follow smaller adj-list
    if len(adj[x]) < len(adj[y]):
        start, finish = x, y
    else:
        start, finish = y, x

    _ = explore(adj, start, finish)

    return 1 if reached_finish else 0


INTERACTIVE = False


def create_adjacency_list(data):
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0 : (2 * m) : 2], data[1 : (2 * m) : 2]))
    x, y = data[2 * m :]
    adj = [[] for _ in range(n)]
    x, y = x - 1, y - 1
    for a, b in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    return x, y, adj


def parse_input(file_path):
    data = list(map(int, re.split("\s|\n", open(file_path).read())))
    return create_adjacency_list(data)


if __name__ == "__main__":
    if INTERACTIVE:
        input = sys.stdin.read()
        data = list(map(int, input.split()))
        x, y, adj = create_adjacency_list(data)
        print(reach(adj, x, y))
    else:
        path, files = read_test_cases.return_path_files()
        for file in files:
            reached = set()
            reached_finish = False
            file_path = os.path.join(path, file)
            x, y, adj = parse_input(file_path)
            res = reach(adj, x, y)
            sol = int(open(file_path + ".a").read())

            assert sol == res, f"Error in {file=}"
            if res == 1:
                reachable = "reachable"
            else:
                reachable = "not reachable"
            print(f"solved reachability in graph in {file} ({reachable})")
