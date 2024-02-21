from collections import defaultdict

class DVRTable:
    def __init__(self) -> None:
        # [source : [dest : cost]], N*N - 2d matrix that stores the cost of going from source to dest
        self.distance_table = [] # Distance Vector Routing Table
        self.num_vertices = 0
        self.num_links = 0
        self.num_c_links = 0
        self.id_vertices = []
        self.step = 0
        self.routers = [] # all routers are stored here
    
    def set_routers_DVR(self, inputFile):
        # Initialise all of the routers from the given vertices in the graph
        # starts by creating a router from the source
        print("\n#START\n")

        with open(inputFile, 'r') as file:
            for line in file:
                parts = line.split()
                if(line.startswith('#')):
                    continue
                elif(line.startswith('V')):
                    self.num_vertices = int(line.split()[1])
                elif(line.startswith('L')):
                    self.num_links = int(line.split()[1])
                elif(len(parts) == 1):
                    self.id_vertices.append(int(line))
                else:
                    break
    
            # Create the routers from the id first
            for id in self.id_vertices:
                router = Router(id, self.num_vertices)
                self.routers.append(router)

            # Initialise the routers with the given link info
            for _ in range(self.num_links):
                source, destination, cost = map(int, line.split())
                line = file.readline()
                for i in range(self.num_vertices):
                    if(source == self.id_vertices[i]): # check if the source is one of the vertices
                        for j in range(self.num_vertices):
                            if(destination == self.id_vertices[j]): # check if the destination is one of the vertices
                                self.routers[i].dist[j] = cost
                                self.routers[i].via[j] = destination
                                self.routers[j].dist[i] = cost
                                self.routers[j].via[i] = source

                                print(f"t={self.step} distance from {source} to {destination} via {self.routers[i].via[j]} is {cost}")
                                print(f"t={self.step} distance from {destination} to {source} via {self.routers[j].via[i]} is {cost}")
            self.step += 1

    
        # The distance of a source to itself is always 0
        for source in range(self.num_vertices):
            for dest in range(self.num_vertices):
                if(source == dest):
                    self.routers[source].dist[dest] = 0

        # Initialise the DVR table first
        self.distance_table = [[float('inf')]*self.num_vertices for _ in range(self.num_vertices)]
        # Populate the DVR with the router's dist costs
        for source in range(self.num_vertices):
            for dest in range(self.num_vertices):
                self.distance_table[source][dest] = self.routers[source].dist[dest]

    def update_table(self, max_iterations=100):
        count = 0
        iters = 0
        if(self.step == 1):
            print("\n#INITIAL\n")
        else:
            print("\n#UPDATE\n")
   
        # Bellman-Ford Algorithm
        for _ in range(max_iterations):
            iters += 1
            for i in range(self.num_vertices): # Source, x
                for dest in range(self.num_vertices): # Destination, y
                    for inter_node in range(self.num_vertices): # Intermediary Node, k
                        if(self.routers[i].dist[dest] > self.distance_table[i][inter_node] + self.routers[inter_node].dist[dest]): # dx(y) => min k {c(x,k) + dk(y)}
                            print(f"{self.routers[i].dist[dest]} > {self.distance_table[i][inter_node] + self.routers[inter_node].dist[dest]}")
                            self.routers[i].dist[dest] = self.distance_table[i][inter_node] + self.routers[inter_node].dist[dest]
                            self.routers[dest].dist[i] = self.routers[i].dist[dest]
                            self.routers[i].via[dest] = inter_node+1
                            self.routers[dest].via[i] = inter_node+1
                            count += 1
            if(count == 0):
                break
            count = 0
        
        if(iters == 100):
            print("Count-to-infinity")

        for i in range(self.num_vertices):
            for dest in range(self.num_vertices):
                if(i != dest):
                    print(f"t={self.step} distance from {self.routers[i].id} to {dest+1} via {self.routers[i].via[dest]} is {self.routers[i].dist[dest]}")
        
        self.step += 1

        # Populate the DVR with the router's dist costs
        for source in range(self.num_vertices):
            for dest in range(self.num_vertices):
                    self.distance_table[source][dest] = self.routers[source].dist[dest]
        
        # for i in range(self.num_vertices):
        #     print(self.routers[i].id)
        #     print(self.routers[i].dist)

    def update_changedInput(self,changedInputFile):
        with open(changedInputFile,'r') as file:
            line = file.readline()
            self.num_c_links = int(line.split()[1])
            
            # Set the changed links
            for _ in range(self.num_c_links):
                line = file.readline()
                source, destination, new_cost = map(int, line.split())
                for i in range(self.num_vertices):
                    if(source == self.id_vertices[i]):
                        for j in range(self.num_vertices):
                            if(destination == self.id_vertices[j]):
                                self.routers[i].dist[j] = new_cost
                                self.routers[i].via[j] = destination
                                self.routers[j].dist[i] = new_cost
                                self.routers[j].via[i] = source

        # Populate the DVR with the router's dist costs
        for source in range(self.num_vertices):
            for dest in range(self.num_vertices):
                self.distance_table[source][dest] = self.routers[source].dist[dest]

    def final_table(self):
        print("\n#FINAL\n")
        for i in range(self.num_vertices):
            for dest in range(self.num_vertices):
                if(i != dest):
                    print(f"t={self.step} distance from {self.routers[i].id} to {dest+1} via {self.routers[i].via[dest]} is {self.routers[i].dist[dest]}")
        self.step += 1


class Router:
    def __init__(self, id, vertices) -> None:
        self.id = id
        self.dist = [float('inf')]*vertices # [dest : cost], 1*N the distance matrix of this router to the destination
        self.via = [None]*vertices # [via], 1*N Router, id -> Dest from Via

def create_graph(inputFile, graph, vertices, links, router_Ids):
    with open(inputFile, 'r') as f:
        for line in f:
            parts = line.split()
            if(line.startswith('#')):
                continue
            elif(line.startswith('V')):
                vertices = int(line.split()[1])
            elif(line.startswith('L')):
                links = int(line.split()[1])
            elif(len(parts) == 1):
                router_Ids.append(int(line))
            else:
                source, destination, cost = map(int, line.split())
                graph[source].append((destination, cost))
                graph[destination].append((source, cost))

    return graph, vertices, links, router_Ids

def update_graph(changeInputFile, graph, c_links):
    with open(changeInputFile, 'r') as f:
        for line in f:
            if(line.startswith('C')):
                c_links = int(line.split()[1])
            else:
                source, destination, cost = map(int, line.split())
                for i, (dest, cost) in enumerate(graph[source]):
                    if(destination == dest):
                        graph[source][i] = (destination, cost)
                        break
                    if(destination == source):
                        graph[destination][i] = (source, cost)
                        break
    return graph, c_links

graph = defaultdict(list)
vertices = 0
links = 0
router_Ids = [] 
c_links = 0
# Initial Graph - inputN.txt
graph, vertices, links, router_Ids = create_graph("./distance_vector_inputs/input1.txt", graph, vertices, links, router_Ids)
print(graph)
# Changed Graph - changeInputN.txt
graph, c_links = update_graph("./distance_vector_inputs/changeInput1.txt", graph, c_links)
print(graph)

# The actual algorithm starts here
DVR = DVRTable()
# print("Initial DVR Table :")
# print(DVR.distance_table)
DVR.set_routers_DVR("./distance_vector_inputs/input1.txt")
# for i in range(vertices):
#     print(DVR.routers[i].id)
#     print(DVR.routers[i].dist)
# print("[1] Updated DVR Table :")
# print(DVR.distance_table)
DVR.update_table()
# print("[2] Updated DVR Table :")
# print(DVR.distance_table)
DVR.update_changedInput("./distance_vector_inputs/changeInput1.txt")
DVR.update_table()
DVR.final_table()