# Coursera Course "Algorithms on Graphs"

https://www.coursera.org/learn/algorithms-on-graphs

- Week 1:
  - *Graph decomposition*: depth first reachablity algorithm implemented
  - *Connected components*: get number of connected components in a graph
- Week 2:
  - *Checking graph for cycles*: depth first search with post sorting
  - *Topological ordering of DAGs*: dito
  - *Number of strongly connected components of directed graphs*: DFS with counter update in post sorting
- Week 3:
  - *Shortest path*: using breadth first search for minimal number of steps from one node to an other
  - *Bipartite graphs*: check if a graph is bipartite using BFS
- Week 4:
  - *Shortest path in weighted graph*: impementation of Dijkstra's algorithm
  - *Find negative cycles in directed weighted graph*: using DFS to initialize connected components and then solve the problem using the Bellman-Ford algorithm
  - *Currency exchange*: Bellman-Ford algorithm and DFS for finding exchange rates in a graph with possibly negative cycles
- Week 5:
  - *Minimal spanning tree*: implemented Kruskal's algorithm using set operations with path compression heuristics
  - *Clustering*: minimal distance between clusters using Kruskal's algorithm
- Week 6: Project advanced algorithms
  - *Friend suggestion*: bidirectional Dijkstra 
  - *Distances with coordiantes*: A* algorithm with euclidean distance as potential function for more directed search
  - *Contraction hierarchies small data*: preprocessing graph using heuristic node importance and querying the graph with a bidirectional Dijkstra search while exploiting the rank order of the contracted vertices. The last test case on Coursera is not processed. Error message `(Time used: 0.00/10.00, preprocess time used: 0.47/50.00, memory used: 0/8589934592.)` suggests that the graph data is not loaded at all.
  - *Contraction hierarchies large data*: same as above - passed all tests except the last one with the same message (no memory used, no prepocessing time, no query time used)