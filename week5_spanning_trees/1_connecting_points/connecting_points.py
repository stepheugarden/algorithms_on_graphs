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


def build_priority_queue(x, y):
    pq = queue.PriorityQueue()

    for i in range(len(x)):
        xi, yi = x[i], y[i]
        for j in range(i + 1, len(x)):
            xj, yj = x[j], y[j]
            dij = math.dist((xi, yi), (xj, yj))
            pq.put((dij, i, j))

    return pq


def minimum_distance(x, y):
    result = 0.0
    vertices = list(zip(x, y))
    vert_set = Set(len(vertices))
    pq = build_priority_queue(x, y)

    while not pq.empty():
        dist, i, j = pq.get()
        if vert_set.Find(i) == vert_set.Find(j):
            continue
        vert_set.Union(i, j)
        result += dist
    return result


INTERACTIVE = False

if __name__ == "__main__":
    if INTERACTIVE:
        input = sys.stdin.read()
        data = list(map(int, input.split()))
        n = data[0]
        x = data[1::2]
        y = data[2::2]
        print("{0:.9f}".format(minimum_distance(x, y)))
    else:
        path, files = read_test_cases.return_path_files()
        for file in files:
            file_path = os.path.join(path, file)
            data = list(map(int, re.split("\s|\n", open(file_path).read())))
            n = data[0]
            x = data[1::2]
            y = data[2::2]
            res = minimum_distance(x, y)
            sol = float(open(file_path + ".a").read())

            assert abs(sol - res) <= 10e-6, f"Error in {file=}"
            print(f"minimal spanning tree of {file} has length: {res}")
