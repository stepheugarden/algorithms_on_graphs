# Uses python3

import sys
import os
import re
import queue
import math
from utilities import read_test_cases


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
    return adj, cost


def negative_cycle(adj, cost):
    dist = [math.inf] * len(adj)

    # initialize all connected components using depth first
    connected_comp = [None] * len(adj)

    def dfs(start, adj, comp_id):
        if connected_comp[start] is not None:
            return
        connected_comp[start] = comp_id
        for neig in adj[start]:
            dfs(neig, adj, comp_id)

    for vert in range(len(adj)):
        dfs(vert, adj, vert)

    for indx in list(set(connected_comp)):
        dist[indx] = 0

    # Bellman-Ford algorithm
    for _ in range(len(adj)):
        relaxed_vertices = []
        for u in range(len(adj)):
            for indx, neig in enumerate(adj[u]):
                dist_u = dist[u]
                cost_u = cost[u]
                dist_neig = dist_u + cost_u[indx]
                if dist[neig] > dist_neig:
                    dist[neig] = dist_neig
                    relaxed_vertices.append(u)

    return 0 if len(relaxed_vertices) == 0 else 1


INTERACTIVE = False

if __name__ == "__main__":
    if INTERACTIVE:
        input = sys.stdin.read()
        data = list(map(int, input.split()))
        adj, cost = return_adjecency_weights(data)
        dest, start = list(map(int, data[-1:-3:-1]))
        print(negative_cycle(adj, cost))
    else:
        path, files = read_test_cases.return_path_files(
            "week4_paths_in_graphs2", "1_minimum_flight_cost"
        )
        for file in files:
            file_path = os.path.join(path, file)
            adj, cost = parse_input(file_path)
            res = negative_cycle(adj, cost)
            sol = int(open(file_path + ".a").read())

            assert sol == res, f"Error in {file=}"
            print(f"graph {file} has negative cycle: {res==1}")
