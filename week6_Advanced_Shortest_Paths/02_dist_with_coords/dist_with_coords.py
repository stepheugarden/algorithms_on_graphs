#!/usr/bin/python3

import sys
import queue
import math
from utilities import read_test_cases
import os
import re
from collections import defaultdict


class AStar:
    def __init__(self, n, adj, cost, x, y):
        # See the explanations of these fields in the starter for friend_suggestion
        self.n = n
        self.adj = adj
        self.cost = cost
        self.inf = n * 10**6
        self.d = defaultdict(lambda: n * 10**6)
        self.visited = [0] * n
        self.workset = []
        # Coordinates of the nodes
        self.x = x
        self.y = y

    # See the explanation of this method in the starter for friend_suggestion
    def clear(self):
        self.d = defaultdict(lambda: self.inf)
        self.visited = [0] * self.n
        del self.workset[0 : len(self.workset)]

    def visit(self, q, v, dist, measure):
        # Implement this method yourself
        current_dist = self.d[v]
        if current_dist > dist:
            self.d[v] = dist
            q.put((dist + measure, v))

    def distances_to_t(self, t):
        dist_to_t = {}
        v_t = (self.x[t], self.y[t])
        for i, v_i in enumerate(zip(self.x, self.y)):
            # dist_to_t[i] = math.dist(v_t, v_i)
            dist_to_t[i] = math.sqrt(sum((px - qx) ** 2.0 for px, qx in zip(v_t, v_i)))

        return dist_to_t

    def process(self, v, q, dist_to_t):
        neigh, costs = self.adj[v], self.cost[v]
        dist_v = self.d[v]
        for n, c in zip(neigh, costs):
            dist_n_t = dist_to_t[n]
            self.visit(q, n, c + dist_v, dist_n_t)

    # Returns the distance from s to t in the graph
    def query(self, s, t):
        if s == t:
            return 0

        self.clear()
        q = queue.PriorityQueue()

        dist_to_t = self.distances_to_t(t)
        self.visit(q, s, 0, dist_to_t[s])

        while not q.empty():
            v_dist, v = q.get()
            self.visited[v] += 1
            self.workset.append(v)

            if v == t:
                return self.d[v]

            self.process(v, q, dist_to_t)

        return -1


def readl():
    return map(int, sys.stdin.readline().split())


def parse_input(path):
    data = list(map(int, re.split("\s|\n", open(path).read())))
    n, m = data[:2]
    data = data[2:]

    x, y = [], []
    adj = [[] for _ in range(n)]
    cost = [[] for _ in range(n)]

    for _ in range(n):
        xi, yi = data[:2]
        data = data[2:]
        x.append(xi)
        y.append(yi)

    for _ in range(m):
        v_from, v_to, weight = data[:3]
        data = data[3:]
        adj[v_from - 1].append(v_to - 1)
        cost[v_from - 1].append(weight)

    queries = list(zip(data[1::2], data[2::2]))

    return n, adj, cost, x, y, queries


def parse_solution(path):
    return list(map(int, re.split("\s|\n", open(path + ".a").read())))


INTERACTIVE = False

if __name__ == "__main__":
    if INTERACTIVE:
        n, m = readl()
        x = [0 for _ in range(n)]
        y = [0 for _ in range(n)]
        adj = [[] for _ in range(n)]
        cost = [[] for _ in range(n)]
        for i in range(n):
            a, b = readl()
            x[i] = a
            y[i] = b
        for e in range(m):
            u, v, c = readl()
            adj[u - 1].append(v - 1)
            cost[u - 1].append(c)
        (t,) = readl()
        astar = AStar(n, adj, cost, x, y)
        for i in range(t):
            s, t = readl()
            print(astar.query(s - 1, t - 1))
    else:
        path, files = read_test_cases.return_path_files()
        for file in files:
            file_path = os.path.join(path, file)
            n, adj, cost, x, y, queries = parse_input(file_path)
            astar = AStar(n, adj, cost, x, y)
            res = []
            for s, t in queries:
                if s == 10 and t == 8:
                    x = 10
                res.append(astar.query(s - 1, t - 1))
            sol = parse_solution(file_path)

            assert res == sol, "Error in " + file
            print("bidirectional Dijkstra in " + file + ": " + " ".join(map(str, res)))
