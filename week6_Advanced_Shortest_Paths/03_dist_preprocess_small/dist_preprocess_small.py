#!/usr/bin/python3

import sys
import os
import re
import heapq
from utilities import read_test_cases
from collections import defaultdict, namedtuple
import time

in_out_degree = namedtuple("in_out_degree", ["indeg", "outdeg"])

# Maximum allowed edge length
MAXLEN = 2 * 10**6

# preprocessing must take max. 50 seconds
TIMELIMIT = 50
TIMEBUFFER = 1


class DistPreprocessSmall:
    def __init__(self, n, adj, cost):
        self.n = n
        self.INFINITY = n * MAXLEN
        self.adj = adj
        self.cost = cost
        self.bidistance = [
            defaultdict(lambda: self.INFINITY),
            defaultdict(lambda: self.INFINITY),
        ]
        self.visited = set()
        self.importance_q = []
        self.level = defaultdict(lambda: 0)
        self.rank = defaultdict(lambda: n)
        self.in_out_degree = [None] * n
        self.preprocess_time = TIMELIMIT - TIMEBUFFER
        self.tic = time.time()
        self.preprocessing()

    def preprocessing(self):
        self.add_in_out_degree()
        self.build_importance_queue()
        self.augment_graph()

    def return_preprocessed_time(self):
        return time.time() - self.tic

    def has_remaining_preprocess_time(self):
        return self.return_preprocessed_time() < self.preprocess_time

    def augment_graph(self):
        rank = 0
        while self.has_remaining_preprocess_time() and len(self.importance_q) > 0:
            min_imp, min_node = self.get_minimal_importance()
            self.contract_node(min_node)
            rank += 1
            self.rank[min_node] = rank

    def contract_node(self, v):
        # check all paths from s->v->t
        for s, cost_s in zip(self.adj[1][v], self.cost[1][v]):
            for t, cost_t in zip(self.adj[0][v], self.cost[0][v]):
                cost_s_t = cost_s + cost_t
                has_path = self.has_witness_path(s, v, t, cost_s_t, 10)
                if not has_path:
                    # add shortcut or update distance
                    self.add_arc(s, t, cost_s_t)

                    # update in out degrees of new shortcut nodes
                    self.set_in_out_degree(s)
                    self.set_in_out_degree(t)

                    # update node levels
                    self.update_node_levels(v)

    def has_witness_path(self, s, v, t, cost_s_t, max_hops=10):
        dists = defaultdict(lambda: self.INFINITY)
        dists[s] = 0
        dists[t] = cost_s_t
        q = []
        heapq.heapify(q)
        heapq.heappush(
            q, (0, 0, s)
        )  # (cost, hops, node v) triple (cost from s to node v, number of hops from s to node v, node v)

        # this is Dijkstra with early stopping
        while len(q) > 0:
            if not self.has_remaining_preprocess_time():
                return False
            if dists[t] < cost_s_t:
                # if we found at least one path that is smaller than the initial path we are done
                return True
            next_cost, next_hops, next_node = heapq.heappop(q)
            for to_node, to_cost in zip(
                self.adj[0][next_node], self.cost[0][next_node]
            ):
                if to_node == v:
                    # exclude the to be contracted node v
                    continue
                updated_cost = dists[next_node] + to_cost
                if updated_cost > dists[t]:
                    # this path is not better than the one we already know
                    continue
                if next_hops >= max_hops:
                    # too many hops already
                    continue
                if dists[to_node] > updated_cost:
                    dists[to_node] = updated_cost
                    heapq.heappush(q, (updated_cost, next_hops + 1, to_node))

        return dists[t] < cost_s_t

    def get_minimal_importance(self):
        min_imp, min_node = heapq.heappop(self.importance_q)
        min_imp_upd = self.caculate_edge_importance(min_node)

        if min_imp == min_imp_upd:
            return min_imp, min_node

        # otherwise put it back and call function recursively
        heapq.heappush(self.importance_q, (min_imp_upd, min_node))
        return self.get_minimal_importance()

    def caculate_edge_importance(self, v):
        return (
            self.edge_difference(v)
            + self.number_of_contracted_neigh(v)
            + self.shortcut_cover(v)
            + self.level[v]
        )

    def build_importance_queue(self):
        heapq.heapify(self.importance_q)
        for v in range(len(self.adj[0])):
            heapq.heappush(self.importance_q, (self.caculate_edge_importance(v), v))

    def add_in_out_degree(self):
        for v in range(len(self.adj[0])):
            self.set_in_out_degree(v)

    def set_in_out_degree(self, v):
        deg = in_out_degree(len(self.adj[1][v]), len(self.adj[0][v]))
        self.in_out_degree[v] = deg

    def edge_difference(self, v):
        indeg = self.in_out_degree[v].indeg
        outdeg = self.in_out_degree[v].outdeg
        delta = indeg * outdeg - indeg - outdeg
        return max([0, delta])

    def number_of_contracted_neigh(self, v):
        out_contr = [x for x in self.adj[0][v] if x in self.rank]
        in_contr = [x for x in self.adj[1][v] if x in self.rank]

        return len(out_contr) + len(in_contr)

    def shortcut_cover(self, v):
        from_v_importance = 0
        for u in self.adj[0][v]:
            v_to_u = self.in_out_degree[u].indeg
            from_v_importance += 1 / v_to_u if v_to_u > 0 else 0

        to_v_importance = 0
        for w in self.adj[1][v]:
            w_to_v = self.in_out_degree[w].outdeg
            to_v_importance += 1 / w_to_v if w_to_v > 0 else 0

        return from_v_importance + to_v_importance

    def update_node_levels(self, v):
        """update all neighbors of v. This function is called when v is contracted

        Args:
            v (_type_): _description_
        """
        level_v = self.level[v]
        for n in self.adj[0][v]:
            self.level[n] = max([level_v + 1, self.level[n]])

        for n in self.adj[1][v]:
            self.level[n] = max([level_v + 1, self.level[n]])

    def add_arc(self, u, v, c):
        """adds an arc or updates its cost. This function is called while adding a shortcut

        Args:
            u (_type_): from-vertex
            v (_type_): to-vertex
            c (_type_): cost
        """

        def update(adj, cost, u, v, c):
            for i in range(len(adj[u])):
                if adj[u][i] == v:
                    cost[u][i] = min(cost[u][i], c)
                    return
            adj[u].append(v)
            cost[u].append(c)

        update(self.adj[0], self.cost[0], u, v, c)
        update(self.adj[1], self.cost[1], v, u, c)

    # See description of this method in the starter for friend_suggestion
    def clear(self):
        self.bidistance = [
            defaultdict(lambda: self.INFINITY),
            defaultdict(lambda: self.INFINITY),
        ]
        self.visited = set()
        self.level = defaultdict(lambda: 0)

    # See description of this method in the starter for friend_suggestion
    def visit(self, q, side, v, dist):
        if self.bidistance[side][v] > dist:
            self.bidistance[side][v] = dist
            heapq.heappush(q[side], (dist, self.rank[v], v))

    def process(self, q, side, node, node_rank, estimate):
        current_dist = self.bidistance[side][node]
        for to_node, to_cost in zip(self.adj[side][node], self.cost[side][node]):
            to_rank = self.rank[to_node]
            if to_rank < node_rank:
                # only higher ranks are traversed
                continue
            to_dist = current_dist + to_cost
            if estimate < to_dist:
                # if we already have a better estimate there is no need to process
                continue
            self.visit(q, side, to_node, to_dist)

    def update_estimate(self, processed_node, estimate):
        if processed_node in self.visited:
            new_dist = (
                self.bidistance[0][processed_node] + self.bidistance[1][processed_node]
            )
            if new_dist < estimate:
                return new_dist
        return estimate

    # Returns the distance from s to t in the graph
    def query(self, s, t):
        if s == t:
            return 0

        self.clear()
        q = [[], []]
        heapq.heapify(q[0]), heapq.heapify(q[1])
        estimate = self.INFINITY
        self.visit(q, 0, s, 0)
        self.visit(q, 1, t, 0)

        while len(q[0]) > 0 or len(q[1]) > 0:
            if len(q[0]) > 0:
                processed_dist, processed_rank, processed_node = heapq.heappop(q[0])
                if processed_dist <= estimate:
                    self.process(q, 0, processed_node, processed_rank, estimate)

                # update estimate and mark as visited
                estimate = self.update_estimate(processed_node, estimate)
                self.visited.add(processed_node)

            if len(q[1]) > 0:
                processed_dist, processed_rank, processed_node = heapq.heappop(q[1])
                if processed_dist <= estimate:
                    self.process(q, 1, processed_node, processed_rank, estimate)

                # update estimate and mark as visited
                estimate = self.update_estimate(processed_node, estimate)
                self.visited.add(processed_node)

            # check if visited
        return -1 if estimate == self.INFINITY else estimate


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

        ch = DistPreprocessSmall(n, adj, cost)
        print("Ready")
        sys.stdout.flush()
        (t,) = readl()
        for i in range(t):
            s, t = readl()
            print(ch.query(s - 1, t - 1))
    else:
        path, files = read_test_cases.return_path_files()
        for file in files:
            file_path = os.path.join(path, file)
            n, adj, cost, queries = parse_input(file_path)
            ch = DistPreprocessSmall(n, adj, cost)
            res = []
            for s, t in queries:
                res.append(ch.query(s - 1, t - 1))
            sol = parse_solution(file_path)

            assert res == sol, "Error in " + file
            print("distances in " + file + ": " + " ".join(map(str, res)))
