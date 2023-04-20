# Uses python3

import sys
import os
import re
import math
from utilities import read_test_cases


def shortet_paths(adj, cost, start):
    distances = [math.inf] * len(adj)
    distances[start] = 0

    # Bellman-Ford
    for _ in range(len(adj)):
        relaxed_vertices = []
        for u in range(len(adj)):
            for indx, neig in enumerate(adj[u]):
                dist_u = distances[u]
                cost_u = cost[u]
                dist_neig = dist_u + cost_u[indx]
                if distances[neig] > dist_neig:
                    distances[neig] = dist_neig
                    relaxed_vertices.append(u)

    # find reachable vertices from negative cylce
    negative_vertex = set()

    def dfs(start, adj):
        if start in negative_vertex:
            return
        negative_vertex.add(start)
        for neig in adj[start]:
            dfs(neig, adj)

    for vert in relaxed_vertices:
        dfs(vert, adj)

    # combine and construct output
    result = ["*"] * len(distances)
    for vert in negative_vertex:
        result[vert] = "-"

    for indx, vert in enumerate(distances):
        if vert == math.inf or result[indx] == "-":
            continue
        result[indx] = str(vert)

    return result


def return_adjecency_weights(data):
    n, m = data[0:2]
    data = data[2:]
    edges = list(
        zip(zip(data[0 : (3 * m) : 3], data[1 : (3 * m) : 3]), data[2 : (3 * m) : 3])
    )
    data = data[3 * m :]
    adj = [[] for _ in range(n)]
    cost = [[] for _ in range(n)]
    for (a, b), w in edges:
        adj[a - 1].append(b - 1)
        cost[a - 1].append(w)
    return adj, cost


def parse_input(file_path):
    data = list(map(int, re.split("\s|\n", open(file_path).read())))
    adj, cost = return_adjecency_weights(data)
    start = data[-1] - 1
    return adj, cost, start


INTERACTIVE = True

if __name__ == "__main__":
    if INTERACTIVE:
        input = sys.stdin.read()
        data = list(map(int, input.split()))
        adj, cost = return_adjecency_weights(data)
        start = data[-1] - 1
        print(shortet_paths(adj, cost, start))
    else:
        path, files = read_test_cases.return_path_files()
        for file in files:
            file_path = os.path.join(path, file)
            adj, cost, start = parse_input(file_path)
            res = shortet_paths(adj, cost, start)
            sol = re.split("\s|\n", open(file_path + ".a").read())

            assert sol == res, f"Error in {file=}"
            print(f"graph {file} currency exchange: {res}")
