# Uses python3
import sys
import os
import re
import math
import queue
from utilities import read_test_cases
from dataclasses import dataclass, field


@dataclass
class Set:
    """Set logic with path compression heuristic

    Returns:
        _type_: _description_
    """

    n: int
    parent: list = field(init=False, default_factory=list)
    rank: list = field(init=False, default_factory=list)

    def Find(self, i: int):
        """Find parent and compress path

        Args:
            i (int): zero indexed element

        Returns:
            _type_: _description_
        """
        if self.parent[i] != i:
            self.parent[i] = self.Find(self.parent[i])
        return self.parent[i]

    def Union(self, i: int, j: int):
        i_id = self.Find(i)
        j_id = self.Find(j)

        if i_id == j_id:
            return

        if self.rank[i_id] > self.rank[j_id]:
            self.parent[j_id] = i_id
        else:
            self.parent[i_id] = j_id
            if self.rank[i_id] == self.rank[j_id]:
                self.rank[j_id] += 1

    def __post_init__(self):
        self.parent = list(range(self.n))
        self.rank = [0] * self.n


@dataclass
class KeepTop:
    """keep k largest values in a sorted list

    Returns:
        _type_: _description_
    """

    top_k: int
    low: float = -math.inf
    values: list = field(init=False, default_factory=list)

    def __update(self):
        self.values.sort()
        if len(self.values) > self.top_k:
            self.values = self.values[1:]
        assert len(self.values) <= self.top_k
        self.low = self.values[0]

    def add(self, val):
        if len(self.values) < self.top_k or val > self.low:
            self.values.append(val)
            self.__update()

    def getMin(self):
        return self.low


def build_priority_queue(x, y):
    pq = queue.PriorityQueue()

    for i in range(len(x)):
        xi, yi = x[i], y[i]
        for j in range(i + 1, len(x)):
            xj, yj = x[j], y[j]
            dij = math.dist((xi, yi), (xj, yj))
            pq.put((dij, i, j))

    return pq


def clustering(x, y, k):
    result = 0.0
    vert_set = Set(len(x))
    pq = build_priority_queue(x, y)

    # we have to cut the minimial spanning tree k-1 times to get k clusters
    # keep always largest distances (we are cutting there). The minimum of these
    # k-1 distances is the number we are looking for
    kt = KeepTop(k - 1)

    while not pq.empty():
        dist, i, j = pq.get()
        if vert_set.Find(i) == vert_set.Find(j):
            continue
        vert_set.Union(i, j)
        kt.add(dist)
        result += dist
    return kt.getMin()


INTERACTIVE = False

if __name__ == "__main__":
    if INTERACTIVE:
        input = sys.stdin.read()
        data = list(map(int, input.split()))
        n = data[0]
        data = data[1:]
        x = data[0 : 2 * n : 2]
        y = data[1 : 2 * n : 2]
        k = data[-1]
        print("{0:.9f}".format(clustering(x, y, k)))
    else:
        path, files = read_test_cases.return_path_files()
        for file in files:
            file_path = os.path.join(path, file)
            data = list(map(int, re.split("\s|\n", open(file_path).read())))
            n = data[0]
            data = data[1:]
            x = data[0 : 2 * n : 2]
            y = data[1 : 2 * n : 2]
            k = data[-1]
            res = clustering(x, y, k)
            sol = float(open(file_path + ".a").read())

            assert abs(sol - res) <= 10e-6, f"Error in {file=}"
            print(f"minimal distance in {k} clusters of {file}: {res}")
