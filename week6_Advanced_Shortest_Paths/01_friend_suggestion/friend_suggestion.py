#!/usr/bin/python3

import sys
import queue
import os
import re
from collections import defaultdict
import math
from utilities import read_test_cases


# TODO: maybe faster with self.visited as a set
# TODO: reconstruct best path
class BiDij:
    def __init__(self, n):
        self.n = n
        # Number of nodes
        self.d = [
            defaultdict(lambda: math.inf),
            defaultdict(lambda: math.inf),
        ]  # Initialize distances for forward and backward searches
        self.workset = []  # All the nodes visited by forward or backward search
        self.visited = [
            False
        ] * n  # # visited[v] == True iff v was visited by forward or backward search

    def clear(self):
        """Reinitialize the data structures for the next query after the previous query."""
        for v in self.workset:
            self.visited[v] = False
        self.d[0].clear()
        self.d[1].clear()
        del self.workset[0 : len(self.workset)]

    def visit(self, q, side, v_from, v_to, dist):
        """Try to relax the distance to node v from direction side by value dist."""
        current_dist = self.d[side][v_to]
        if current_dist > dist:
            self.d[side][v_to] = dist
            q[side].put((dist, v_from, v_to))

    def process(self, v, q, side, adj, cost):
        neigh, costs = adj[side][v], cost[side][v]
        dist_v = self.d[side][v]
        self.workset.append(v)

        for n, c in zip(neigh, costs):
            self.visit(q, side, v, n, c + dist_v)

    def find_shortest_path(self):
        distance = math.inf

        for v in self.workset:
            iter_dist = self.d[0][v] + self.d[1][v]
            if iter_dist < distance:
                distance = iter_dist

        return distance if distance < math.inf else -1

    def query(self, adj, cost, s, t):
        self.clear()

        if s == t:
            return 0

        q = [queue.PriorityQueue(), queue.PriorityQueue()]
        self.visit(q, 0, s, s, 0)
        self.visit(q, 1, t, t, 0)

        while not q[0].empty() and not q[1].empty():
            dist_iter, v_from, v_to = q[0].get()
            self.process(v_to, q, 0, adj, cost)
            if self.visited[v_to]:
                best_dist = self.find_shortest_path()
                return best_dist
            self.visited[v_to] = True

            dist_iter, v_from, v_to = q[1].get()
            self.process(v_to, q, 1, adj, cost)
            if self.visited[v_to]:
                best_dist = self.find_shortest_path()
                return best_dist
            self.visited[v_to] = 1

        return -1


def readl():
    return map(int, sys.stdin.readline().split())


def parse_input(path):
    data = list(map(int, re.split("\s|\n", open(file_path).read())))
    n, m = data[:2]
    data = data[2:]

    adj = [[[] for _ in range(n)], [[] for _ in range(n)]]
    cost = [[[] for _ in range(n)], [[] for _ in range(n)]]

    for _ in range(m):
        u, v, c = data[:3]
        data = data[3:]
        adj[0][u - 1].append(v - 1)
        cost[0][u - 1].append(c)
        adj[1][v - 1].append(u - 1)
        cost[1][v - 1].append(c)

    queries = list(zip(data[1::2], data[2::2]))

    return n, adj, cost, queries


def parse_solution(path):
    return list(map(int, re.split("\s|\n", open(path + ".a").read())))


INTERACTIVE = False

if __name__ == "__main__":
    if INTERACTIVE:
        n, m = readl()
        adj = [[[] for _ in range(n)], [[] for _ in range(n)]]
        cost = [[[] for _ in range(n)], [[] for _ in range(n)]]
        for e in range(m):
            u, v, c = readl()
            adj[0][u - 1].append(v - 1)
            cost[0][u - 1].append(c)
            adj[1][v - 1].append(u - 1)
            cost[1][v - 1].append(c)
        (t,) = readl()
        bidij = BiDij(n)
        for i in range(t):
            s, t = readl()
            print(bidij.query(adj, cost, s - 1, t - 1))
    else:
        path, files = read_test_cases.return_path_files()
        for file in files:
            file_path = os.path.join(path, file)
            n, adj, cost, queries = parse_input(file_path)
            bidij = BiDij(n)
            res = []
            for s, t in queries:
                res.append(bidij.query(adj, cost, s - 1, t - 1))
            sol = parse_solution(file_path)

            assert res == sol, "Error in " + file
            print("bidirectional Dijkstra in " + file + ": " + " ".join(map(str, res)))
