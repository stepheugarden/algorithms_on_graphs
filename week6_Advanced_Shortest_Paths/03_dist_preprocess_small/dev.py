import queue
import random
import time
import heapq

# queue are somehow much slower than heapq

if __name__ == "__main__":
    random.seed(11)
    k = 1_000_000
    nums = random.choices(range(100000000), k=k)

    tic = time.time()
    q = []
    heapq.heapify(q)
    for num in nums:
        heapq.heappush(q, num)

    while len(q) > 0:
        _ = heapq.heappop(q)

    toc = time.time()
    print(f"heapq took {toc-tic} seconds")

    del q
    tic = time.time()
    q = queue.PriorityQueue()
    for num in nums:
        q.put(num)

    while not q.empty():
        _ = q.get()

    toc = time.time()
    print(f"queue.PriorityQueue took {toc-tic} seconds")
