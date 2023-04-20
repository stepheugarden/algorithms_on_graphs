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
    destination, start = list(map(int, data[-1:-3:-1]))
    adj, cost = return_adjecency_weights(data)
    return start - 1, destination - 1, adj, cost


def distance(adj, cost, s, t):
    dist = [math.inf] * len(adj)
    dist[s] = 0

    q = queue.PriorityQueue()
    for vert in range(len(dist)):
        q.put((dist[vert], vert))

    while not q.empty():
        _, u = q.get()
        dist_u = dist[u]
        cost_u = cost[u]

        for indx, neig in enumerate(adj[u]):
            dist_neig = dist_u + cost_u[indx]
            if dist[neig] > dist_neig:
                dist[neig] = dist_neig
                q.put((dist_neig, neig))

    return dist[t] if dist[t] < math.inf else -1


INTERACTIVE = False

if __name__ == "__main__":
    if INTERACTIVE:
        input = sys.stdin.read()
        data = list(map(int, input.split()))
        adj, cost = return_adjecency_weights(data)
        dest, start = list(map(int, data[-1:-3:-1]))
        print(distance(adj, cost, start - 1, dest - 1))
    else:
        path, files = read_test_cases.return_path_files()
        for file in files:
            file_path = os.path.join(path, file)
            start, dest, adj, cost = parse_input(file_path)
            res = distance(adj, cost, start, dest)
            sol = int(open(file_path + ".a").read())

            assert sol == res, f"Error in {file=}"
            print(f"shortest path from {start} -> {dest} in graph {file}: {res}")
