from collections import defaultdict

def createGraph (Inputfile, graph, source, vertices, directed_bool) :
    with open(Inputfile, 'r') as f:
        for line in f:
            if(line.startswith('#')):
                if(line.strip() == "#directed"):
                    directed_bool = True
            elif(line.startswith('V')): # Number of vertices
                vertices = int(line.split()[1])
            elif(line.startswith('S')): # The starting vertex
                start = int(line.split()[1])
            else:
                source, destination, weight = map(int, line.split())
                graph[source].append((destination, weight))
                # Initialise undirected which goes both ways
                if(directed_bool == False):
                    graph[destination].append((source, weight))
    # Add the vertices with no outgoing links to the graph
    if(directed_bool):
        for vertex in range(1,vertices+1):
            if(vertex not in graph):
                graph[vertex].append((0,0))
    return graph, start, vertices, directed_bool

def singleSource_BellmanFord (graph, start, vertices, directed_bool):
    keys = graph.keys() # All the vertices
    # Initialise every distance from all vertices to infinity because we do not know if they are reachable or not.
    distances = {vertex : float('inf') for vertex in keys}
    distances[start] = 0 # distance to itself is 0
   
    # Relax the edges |V|-1 times
    for _ in range(vertices-1):
        for u in graph:
            for v, weight in graph[u]:
                if v in keys and distances[u] + weight < distances[v] :
                    distances[v] = distances[u] + weight

    # Check for negative weighted cycles
    # Repeat to find nodes caught in a negative cycle
    # The resulting distance to those vertices will become '-inf' to signify where the negative cycles are
    if(directed_bool):
        for _ in range(vertices-1):
            for u in graph:
                for v, weight in graph[u]:
                    if v in keys and distances[u] + weight < distances[v] :
                        distances[v] = float('-inf')

    # In the case of an undirected graph, there shouldn't be any negative weights as it be counted as a loop.
    # Only run bellman ford for an undirected graph that has no negative weights
                
    return distances

graph = defaultdict(list)
start = 0
vertices = 0
directed_bool = False
graph, start, vertices, directed_bool = createGraph("input5.txt", graph, start, vertices, directed_bool)
print("Graph :")
print(graph)
print()

# Run the algo to find the shortest path from '1' to every other vertices
print(directed_bool)
distances = singleSource_BellmanFord(graph, start, vertices, directed_bool)
print(distances)

