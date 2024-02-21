# Single Source Bellman Ford Algorithm

### Things to note :

undirected vs directed graphs

1. bellman ford mustn't contain any negative weights if it is running an undirected graph because the negative cycles will count as a loop which will lead to -inf distances for every vertices due to how negative cycles are detected.
2. bellman ford can contain negative weights if is running a directed graph, the distances will only become -inf if there are any negative cycles.

# Distance Vector Routing Algorithm

### How the order of the edges can affect the order of the adjacency list in the code :

### Compare [1] edges to [2] edges :

1 2 2
1 4 1 \*\*
2 3 3
2 4 7
3 4 11

1 2 2
2 3 3
1 4 1 \*\*
2 4 7
3 4 11

You can that [1] will lead to adjacency list of this order 1,2,4,3 & [2] will produce adjacency list of this order 1,2,3,4
The difference lies in the order of the numbers being laid out in the input file : - 1st & 2nd digits need to be laid out in ascending order.

### Why does it matter ?

It complicates how the router object and distance vector routing table is populated in the code.
