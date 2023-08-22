# numbers = [3,6,2,8,4,10]
# max = numbers[0]

# for num in numbers:
#     if(num > max):
#         max = num
# print(f'max number is {max}')

## Remove duplicates from list
# list = [2,1,4,5,2]
# list.sort()
# left_pointer = 1
# for right_pointer in range(1,len(list)):
#     if list[right_pointer] != list[right_pointer-1]:
#         list[left_pointer] = list[right_pointer]
#         left_pointer += 1
# list.pop()
# print(list)

# Classes 
# class Person:
#     def __init__(self, name):
#         self.name = name
    
#     def talk(self):
#         print(f"Hi, I am {self.name}")

# person_1 = Person("Zhao Ming Soh")
# person_1.talk()

## Breadth First Search example:

size = 5
matrix_A = [
    [0,1,1,1,0],
    [1,0,1,0,0],
    [1,1,0,1,1],
    [1,0,1,0,1],
    [0,0,1,1,0]
]

# bfs_q = queue.Queue()
# visited_q = [0] * size
# current_vertex = '';

# # Starts from vertex 0
# bfs_q.put(0)
# visited_q[0] = 1

# # explore all the vertex neighbours
# while not bfs_q.empty():
#     current_vertex = bfs_q.get()
#     for v in range(len(matrix_A[current_vertex])):
#         if matrix_A[current_vertex][v] == 1 and visited_q[v] == 0:
#             print(v)
#             bfs_q.put(v)
#             visited_q[v] = 1


# "William Fiset" example of Breadth First Search
def solve(s):
    vertex_q = []
    vertex_q.insert(0, s) # enqueueing the source vertex to the queue

    visited_q = [False] * size
    visited_q[s] = True

    prev = [None] * size

    # Explore each of the selected vertex's neighbors
    while len(vertex_q) != 0:
        curr_vertex = vertex_q.pop()

        for neigh in range(len(matrix_A[curr_vertex])):
            if matrix_A[curr_vertex][neigh] == 1 and visited_q[neigh] == False:
                visited_q[neigh] = True
                vertex_q.insert(0, neigh)
                print(curr_vertex)
                prev[neigh] = curr_vertex

    return prev

def reconstruct_Path(s,e,prev):
    path = []
    at = e
    while at != None:
        print(at)
        path.append(at)
        at = prev[at]
    path.reverse()
    if path[0] == s:
        return path


def bfs(s, e):
    prev = solve(s)
    print(prev)
    path = reconstruct_Path(s,e,prev)

    return path
    # return reconstruct_Path(s,e,prev)

p = bfs(0,4)
print(p)