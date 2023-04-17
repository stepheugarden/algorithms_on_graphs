# Uses python3

import sys
import queue
import os
import re
from utilities import read_test_cases


def create_adjacency_list(data):
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0 : (2 * m) : 2], data[1 : (2 * m) : 2]))
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    return adj


def parse_input(file_path):
    data = list(map(int, re.split("\s|\n", open(file_path).read())))
    path_start, path_end = data[-2] - 1, data[-1] - 1
    return create_adjacency_list(data), path_start, path_end


def distance(adj, s, t):
    q = queue.Queue()
    q.put(s)
    dist = [None] * len(adj)
    dist[s] = 0

    while not q.empty():
        current_vertex = q.get()
        current_dist = dist[current_vertex]
        for neigh in adj[current_vertex]:
            if dist[neigh] is None:
                dist[neigh] = current_dist + 1
                q.put(neigh)
            if neigh == t:
                return dist[neigh]

    return -1


INTERACTIVE = False

if __name__ == "__main__":
    if INTERACTIVE:
        input = sys.stdin.read()
        data = list(map(int, input.split()))
        path_start, path_end = data[-2] - 1, data[-1] - 1
        adj = create_adjacency_list(data)
        print(distance(adj, path_start, path_end))
    else:
        path, files = read_test_cases.return_path_files(
            "week3_paths_in_graphs1", "1_flight_segments"
        )
        for file in files:
            file_path = os.path.join(path, file)
            adj, path_start, path_end = parse_input(file_path)
            res = distance(adj, path_start, path_end)
            sol = int(open(file_path + ".a").read())

            assert sol == res, f"Error in {file=}"
            print(f"shortest path in graph {file}: {res}")
