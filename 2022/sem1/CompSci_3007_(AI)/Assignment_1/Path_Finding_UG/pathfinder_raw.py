import sys
import math

lines = []
algorithm_selection = ""
heuristic = ""

# Read contents from the text file from the command line at argv[1]
if len(sys.argv) > 1:
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    if len(sys.argv) == 3:
        algorithm_selection = sys.argv[2]

    if len(sys.argv) == 4:
        algorithm_selection = sys.argv[2]
        heuristic = sys.argv[3]
else:
    print("Missing arguments from command line !!")

lines_no_newline = []
for s in lines:
    lines_no_newline.append(s.strip())

# The size of the adjacency matrix
r,c = lines_no_newline[0].split()

# The initial position and end position
start_row, start_col = lines[1].split()
end_row, end_col = lines[2].split()

start_row = int(start_row)- 1
start_col = int(start_col) - 1
end_row = int(end_row) - 1
end_col = int(end_col) - 1

# print(f'matrix size : {r}x{c}')
# print(f'starting point : [{start_row},{start_col}]')
# print(f'ending point : [{end_row},{end_col}]')

# The adjacency matrix
matrix_A = []
row_list = []

for index in range(3, len(lines_no_newline)):
    row_list = lines_no_newline[index].split()
    matrix_A.append(row_list)

## BFS Algorithm
# Row Queue and Column Queue - tracks which vertex should be explored
vrow_queue_BFS = [] 
vcol_queue_BFS = []

# # Variables that keep track of the number of steps taken to reach the end point
# move_count = 0
# nodes_left_in_layer = 1
# nodes_in_next_layer = 0

# Visited Matrix of size r*c which tracks which 
visited = [[False]*int(c) for _ in range(int(r))]
parent_ = [["Empty"]*int(c) for _ in range(int(r))]

# Direction vectors 
row_move = [-1,+1,0,0]
col_move = [0,0,-1,+1]

# Boolean to check if the end point was reached
bool_destination = False

def BFS_Action(curr_r_vertex, curr_c_vertex):
    # global nodes_in_next_layer

    for i in range(0, 4):
        # print(f'i iter {i}')
        move_r = curr_r_vertex + row_move[i]
        move_c = curr_c_vertex + col_move[i]

        # Skip current iteration when the neighboring cell is out of bound
        # The row element cannot be < 0 or >= r size
        # The col element cannot be < 0 or >= c size
        if move_r < 0 or move_c < 0:
            # print(f"Skip 1 : [{move_r},{move_c}] out of bound")
            continue
        if move_r >= int(r) or move_c >= int(c):
            continue
        
        # If the current cell has already been visited
        # If the current cell has the value of 'X' (blocked cell)
        if visited[move_r][move_c]:
            # print(f"Skip 3 : [{move_r},{move_c}] is visited.")
            continue
        if matrix_A[move_r][move_c] == 'X':
            # print(f"Skip 4 : [{move_r},{move_c}] blocked")
            continue

        # If none of the above occurs, then the neighbour cell is an unvisited,
        # non-blockade, in boundary cell.
        vrow_queue_BFS.insert(0, move_r)
        vcol_queue_BFS.insert(0, move_c)
        visited[move_r][move_c] = True
        parent_[move_r][move_c] = str(curr_r_vertex) + " " + str(curr_c_vertex)
        # print(f'    neighbor_node : [{move_r},{move_c}]')
        # nodes_in_next_layer += 1


def backtrace_parents():
    row = end_row
    col = end_col
    path_to_des = [str(row) + " " + str(col)]
    while parent_[row][col] != "Empty":
        path_to_des.append(parent_[row][col])
        row, col = parent_[row][col].split()
        row = int(row)
        col = int(col)
    path_to_des.reverse()
    if path_to_des[0] == (str(start_row) + " " + str(start_col)):
        return path_to_des
    else:
        return []


def print_result(matrix_B):
    # Join all the elements from each row into a string and print it out
    for row in matrix_B:
        print(' '.join(row))


def resulting_matrix(path):
    matrix_B = list(matrix_A)
    for i in path:
        row, col = i.split()
        matrix_B[int(row)][int(col)] = '*'
    return matrix_B


def BFS():
    # global move_count, nodes_left_in_layer, nodes_in_next_layer
    count = 0
    # Insert the starting point into the queue where the row-th element
    # is placed in the row_queue and the col-th element is placed into the
    # col_queue
    vrow_queue_BFS.insert(0, start_row)
    vcol_queue_BFS.insert(0, start_col)

    # Visited Matrix - Set the starting vertex to true
    visited[start_row][start_col] = True

    while len(vrow_queue_BFS) != 0:
        count += 1
        # pop the unexplored vertex from the queue
        current_row_v = vrow_queue_BFS.pop()
        curr_c_vertex = vcol_queue_BFS.pop()
        
        # print("-" * 100)
        # print("Count : " + str(count))
        # print("What's in the queue : ")
        # for i in range(len(vrow_queue)):
        #     print(f'[{vrow_queue[i]},{vcol_queue[i]}]')
        # print(f'    Current Vertex : [{current_row_v},{curr_c_vertex}]')

        # if we have reached the end point, set bool_destination = True
        # and break out of the whileloop
        if current_row_v == end_row and curr_c_vertex == end_col:
            bool_destination = True
            break

        # Move up, down, left and right to explore the current vertex neighbours
        BFS_Action(current_row_v, curr_c_vertex)
        # print(f"Nodes_left_in_layer : {nodes_left_in_layer}")
        # nodes_left_in_layer -= 1
        # print(f"Nodes_left_in_layer - 1 : {nodes_left_in_layer}")
        # print(f"Nodes_in_next_layer : {nodes_in_next_layer}")
        # if nodes_left_in_layer == 0:
        #     nodes_left_in_layer = nodes_in_next_layer
        #     nodes_in_next_layer = 0
        #     move_count += 1
        # print(f"Move_count : {move_count}")
        # print("-" * 100)
        
    # if bool_destination:
    #     return move_count

    return -1


## UCS Algorithm
pqueue_UCS = []
dist_UCS = [[math.inf]*int(c) for _ in range(int(r))]

# Tracks order in which a neighbour is explored, this ensure that when we have neighbors that have
# the same total path cost, the pqueue will arrange them in the order in which they were explored
l_order = 0

def USC_Action(curr_r_vertex, curr_c_vertex, path_cost):
    global l_order
    for i in range(4):
        move_r = curr_r_vertex + row_move[i]
        move_c = curr_c_vertex + col_move[i]

        # Skip the current iteration of the loop if the new row or col position is out of bound
        if move_r < 0 or move_c < 0:
            # print(f'Skip 1 :[{move_r}, {move_c}] is out of bound.')
            continue

        if move_r >= int(r) or move_c >= int(c):
            continue
        
        # Skip the current iteration of the loop if the new row or col position is either 'X'(blocked)
        # or is already visited
        if visited[move_r][move_c]:
            # print(f'Skip 3: [{move_r}, {move_c}] is already visited.')
            continue

        if matrix_A[move_r][move_c] == 'X':
            # print(f'Skip 4: [{move_r}, {move_c}] is blocked.')
            continue

        # If none of the above condition occur:
        #   1. Calculate the gcost(a,b,c,d,M) = 1 + M(c,d) + M(a,d) which is the cost of moving
        #      from the current vertex to its neighbour
        #   2. Calculate the total distance from the current vertex to its neigbour using the gcost
        #   3. enqueue the neighbors - total distance pair onto the priority queue
        l_order += 1
        # print(f'        neighbor node : [{move_r}, {move_c}]')
        M_cost = int(matrix_A[move_r][move_c]) - int(matrix_A[curr_r_vertex][curr_c_vertex])
        gcost = 0
        if M_cost > 0:
            gcost = 1 + M_cost
        else:
            gcost = 1
        # print(f'[{move_r}, {move_c}] gcost = {gcost}')
        t_distance = path_cost + gcost
        dist_UCS[move_r][move_c] = t_distance
        # print(f'[{curr_r_vertex}, {curr_c_vertex}] ---> [{move_r}, {move_c}] path cost = {t_distance}')
        visited[move_r][move_c] = True
        pqueue_UCS.append([t_distance, l_order, str(move_r)+" "+str(move_c)])
        parent_[move_r][move_c] = str(curr_r_vertex) + " " + str(curr_c_vertex)


def UCS():
    global l_order
    # count = 0
    # change the distance of the starting position in the distance matrix to 0
    dist_UCS[start_row][start_col] = 0
    # enqueue the starting position into the priority queue and set its visited to true
    pqueue_UCS.append([0, l_order+1, str(start_row)+ " "+str(start_col)])
    visited[start_row][start_col] = True

    # Using loop to explore all the neighbors of the currently selected vertex
    while len(pqueue_UCS) != 0:
        # count += 1
        # dequeue the vertex with the (smallest total distance from the starting vertex)
        # sort the priority queue according to:
        #   1. The order in which the vertex is added to the queue
        #   2. The least path cost from the starting position to the current vertex
        pqueue_UCS.sort(key = lambda x : x[1])
        # print(f'pqueue_UCS order by key: {pqueue_UCS}')
        pqueue_UCS.sort(reverse = True)
        # print(f'pqueue_UCS order : {pqueue_UCS}')
        temp = pqueue_UCS.pop()
        path_cost, curr_vertex = [temp[i] for i in [0,2]]
        curr_r_vertex, curr_c_vertex = curr_vertex.split()
        curr_r_vertex = int(curr_r_vertex)
        curr_c_vertex = int(curr_c_vertex)
        # print('-' * 100)
        # print(f'count : {count}')
        # print(f"What is in the pqueue :")
        # print(pqueue_UCS)
        # print(f'Current_Vertex : [{curr_r_vertex},{curr_c_vertex}], total_distance : {path_cost}')

        # if the current vertex is the end point, end the loop
        if curr_r_vertex == end_row and curr_c_vertex == end_col:
            bool_destination = True
            break

        # Explore the current vertex neighbors by moving up, down, left and right
        USC_Action(curr_r_vertex, curr_c_vertex, path_cost)
        # print('-' * 100)


## A* search Algorithm
# Matrix of size r * c to store the following:
#   1. the g(a,b,c,d) --> cost of going from point(a,b) to point(c,d)
#   2. the f(a,b,end_row,end_col) --> the total cost of going from point(a,b) to the endpoint(end_row, end_col)
g_cost_Astar = [[math.inf] * int(c) for _ in range(int(r))]
f_cost_Astar = [[math.inf] * int(c) for _ in range(int(r))]
pqueue_Astar = []
# visited_Astar = [[False]*int(c) for _ in range(int(r))]

def hueristic_cal(curr_r_vertex, curr_c_vertex):
    temp = -1
    if heuristic == "manhattan":
        temp = abs(curr_r_vertex - end_row) + abs(curr_c_vertex - end_col)
    elif heuristic == "euclidean":
        temp = math.sqrt((curr_r_vertex - end_row)**2 + (curr_c_vertex - end_col)**2)
    return temp


def Astar_Action(curr_r_vertex, curr_c_vertex):
    global l_order, pqueue_Astar
    # Each cell can move up, down, left and right
    for i in range(4):
        new_r = curr_r_vertex + row_move[i]
        new_c = curr_c_vertex + col_move[i]

        # Skip current iteration :
        # 1. if the new cell is out of bound
        if new_r < 0 or new_c < 0:
            # print(f'Skip 1: [{new_r}, {new_c}] is out of bound')
            continue
        if new_r >= int(r) or new_c >= int(c):
            # print(f'Skip 2: [{new_r}, {new_c}] is out of bound')
            continue
        # 2. if the new cell is blocked
        if matrix_A[new_r][new_c] == 'X':
            # print(f'Skip 3: [{new_r}, {new_c}] is blocked')
            continue
        
        # If 1. and 2. did not occur:
        #   - Calculate the g_cost, h_cost and f_cost of the new cell.
        #   - Check if the new cell has already been visited or that the new f_cost < old f_cost
        #       [Explanation for checking new f_cost < old f_cost] :
        #        - Let's say we have a cell b that has a g_cost = 1, calculated from a --> b, as b was the neighbour
        #          of cell a. Now that cell b is the parent and cell a is the children, to go from cell a to the end point
        #          through cell b would mean going from a ---> b ----> a (double counted), this change will be reflected
        #          in the f_cost of cell a. Thus, increasing the f_cost of cell a.
        M_cost = int(matrix_A[new_r][new_c]) - int(matrix_A[curr_r_vertex][curr_c_vertex])
        elevation_cost = 0
        if M_cost > 0:
            elevation_cost = 1 + M_cost
        else:
            elevation_cost = 1
        g_cost = g_cost_Astar[curr_r_vertex][curr_c_vertex] + elevation_cost
        f_cost = g_cost + hueristic_cal(new_r, new_c)
        # print(f'    neighbor : [{new_r}, {new_c}], g_cost : {g_cost}, h(n) : {hueristic_cal(new_r, new_c)}, f_cost : {f_cost}')
        l_order += 1
        if f_cost < f_cost_Astar[new_r][new_c]: 
            g_cost_Astar[new_r][new_c] = g_cost
            f_cost_Astar[new_r][new_c] = f_cost
            pqueue_Astar.insert(0, [f_cost_Astar[new_r][new_c], l_order, hueristic_cal(new_r, new_c), str(new_r)+" "+str(new_c)])
            parent_[new_r][new_c] = str(curr_r_vertex)+" "+str(curr_c_vertex)


def Astar():
    global l_order
    count = 0
    # Initialise the starting vertex
    g_cost_Astar[start_row][start_col] = 0
    f_cost_Astar[start_row][start_col] = int(g_cost_Astar[start_row][start_col]) + hueristic_cal(start_row, start_col)
    visited[start_row][start_col] = True
    pqueue_Astar.insert(0, [l_order + 1, f_cost_Astar[start_row][start_col], hueristic_cal(start_row, start_col), str(start_row)+" "+str(start_col)])

    # Explore the neighbours of the vertex with the least f_cost
    while len(pqueue_Astar) != 0:
        count += 1
        # For every newly added vertex in the priority queue:
        #   1. sort it according to the order in which they are discovered
        #   2. sort them in terms of their f_cost from smallest to the biggest
        #   3. again, sort according to the value of the hueristic from smallest to the biggest
        # print(f'pqueue_Astar before sort : {pqueue_Astar}')
        pqueue_Astar.sort(key = lambda x: (x[0], x[1], x[2]))
        pqueue_Astar.reverse()
        # print(f'pqueue_Astar after sort : {pqueue_Astar}')

        # Dequeue the vertex with the least f_cost from the priority queue
        temp = pqueue_Astar.pop()
        f_cost_var, h, curr_vertex = [temp[i] for i in [0,2,3]]
        curr_r_vertex, curr_c_vertex = curr_vertex.split()
        curr_r_vertex = int(curr_r_vertex)
        curr_c_vertex = int(curr_c_vertex)
        # print('-'*100)
        # print(f'count = {count}')
        # print(f'Current Vertex : [{curr_r_vertex},{curr_c_vertex}], h(n) : {h}, f_cost : {f_cost_var}')

        if curr_r_vertex == end_row and curr_c_vertex == end_col:
            bool_destination = True
            break
        Astar_Action(curr_r_vertex, curr_c_vertex)
        # print('-'*100)


if algorithm_selection == "bfs":
    BFS()
    path = backtrace_parents()
    if len(path) == 0:
        print("Null")
    else:
        matrix_B = resulting_matrix(path)
        print_result(matrix_B)
elif algorithm_selection == 'ucs':
    UCS()
    path = backtrace_parents()
    if len(path) == 0:
        print("Null")
    else:
        matrix_B = resulting_matrix(path)
        print_result(matrix_B)
elif algorithm_selection == 'astar':
    Astar()
    path = backtrace_parents()
    if len(path) == 0:
        print("null")
    else:
        matrix_B = resulting_matrix(path)
        print_result(matrix_B)
# print(f"Total number of moves : {move}")
# print(path)

