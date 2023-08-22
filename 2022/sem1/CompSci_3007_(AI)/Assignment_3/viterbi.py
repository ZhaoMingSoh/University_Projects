import sys
import numpy as np

# Global Var
num_row = 0
num_col = 0
transition_Matrix = []
list_empty_cells = {}
observation_Matrix = []
trellis = []


def readFiles(filepath):
    lines = []
    with open(filepath) as f:
        l = f.readline().rstrip("\n")
        while l:
            lines.append(l)
            l = f.readline().rstrip("\n")
    return lines

def find_actual_bit_seq(cur_row_pos, cur_col_pos, map):
    row_Dvector = [-1,+1,0,0] # -1 -> going up, +1 -> going down
    col_Dvector = [0,0,-1,+1] # -1 -> going left, +1 -> going right
    bit_seq = [0,0,0,0]

    for i in range(0,4):
        new_r_pos = cur_row_pos + row_Dvector[i]
        new_c_pos = cur_col_pos + col_Dvector[i]

        # print(f"New Position - [{new_r_pos},{new_c_pos}]")

        # When the currently selected empty cell's new position is out of bound
        if new_r_pos < 0: # new row position is negative --> North side is out of bound
            bit_seq[0] = 1
            continue
        if new_c_pos < 0: # new col position is negative --> West side is out of bound
            bit_seq[3] = 1
            continue
        if new_r_pos >= num_row: # new row is greater than the max row number of the map --> South side is out of bound
            bit_seq[2] = 1
            continue
        if new_c_pos >= num_col: # new col is greater than the max col number of the map --> East side is out of bound
            bit_seq[1] = 1
            continue

        # When the currently selected empty cell's new position is blocked
        if map[new_r_pos][new_c_pos] == 'X':
            # print("blocked")
            if new_r_pos == cur_row_pos + 1: # new row position is 1 greater than the current --> South side is blocked
                bit_seq[2] = 1
            if new_r_pos == cur_row_pos - 1: # new row position is 1 smaller than the current --> North side is blocked
                bit_seq[0] = 1
            if new_c_pos == cur_col_pos + 1: # new col position is 1 greater than the current --> East side is blocked
                bit_seq[1] = 1
            if new_c_pos == cur_col_pos - 1: # new col position is 1 smaller than the current --> West side is blocked
                bit_seq[3] = 1
    
    # print(f"bit_seq = {bit_seq}")

    return bit_seq

# Find the number and the index of the neighbours of the currently selected position in the map
def cal_num_Neighbours(cur_row_pos, cur_col_pos, map):
    row_Dvector = [-1,+1,0,0] # -1 -> going up, +1 -> going down
    col_Dvector = [0,0,-1,+1] # -1 -> going left, +1 -> going right

    num_neighbours = 0
    neighbours = []

    for i in range(0,4):
        new_r_pos = cur_row_pos + row_Dvector[i]
        new_c_pos = cur_col_pos + col_Dvector[i]
        # print(f"new_position = [{new_r_pos},{new_c_pos}]")

        # Check if moving up, down, left, right from the current position lead to a blocked position
        # 1) check if the new row or col is < 0
        if new_r_pos < 0 or new_c_pos < 0:
            # print(f"                      -- out_of_bound")
            continue
        # 2) check if the new row or col is >= r or c of the map
        if new_r_pos >= num_row or new_c_pos >= num_col:
            # print(f"                      -- out_of_bound")
            continue
        # 3) check if the new row or col is an empty or blocked cell
        if map[new_r_pos][new_c_pos] == '0':
            num_neighbours += 1
            neighbours.append([new_r_pos, new_c_pos])
        else:
            # print(f"                      -- is blocked")
            continue

    return num_neighbours, neighbours

# Build the Transition Matrix for the transversable cells (empty cells) by identifying the number and index of the neighbours
# from the currently selected empty cells in the map.
def construct_TransitionMatrix(num_empty_cells, map):
    starting_empty_cells_pos = 0 # indicate the ordering of the currently selected empty cell
    neighbour_pos = 0 # indicate the ordering of the neighbouring empty cell in relation to the currently selected empty cell
    all_neighbours = {}
    for r in range(num_row):
        for c in range(num_col):
            #1) Loop through the map and find the empty cell position(row, col) in the map
            if map[r][c] == '0':   
                starting_empty_cells_pos += 1 # increment the ordering of the currently selected empty cell to indicate which empty cell is being processed
                # print("-"*100)
                # print(f'starting_empty_cells_pos({starting_empty_cells_pos}) : [{r},{c}]')
                #2) find the number of neighbours and the index(row, col) of the neighbouring empty cells of currently selected empty cell in the map
                num_neighbours, neighbours = cal_num_Neighbours(cur_row_pos=r, cur_col_pos=c, map=map)
                # print(f"num_neighbours = {num_neighbours}, neighbours = {neighbours}")
                list_empty_cells[starting_empty_cells_pos]["neighbours"] = neighbours
                
    #3) If the neighbouring empty cells exist :
    for order in range(num_empty_cells):
        for key, info in list_empty_cells.items():
            if key-1 == order:
                n = info["neighbours"]
                if len(n) > 0:
                    for el in n:
                        r = el[0]
                        c = el[1]
                        for neigh_order, neigh_pos in list_empty_cells.items():
                            # find out ordering of the neighbouring empty cells from the dictionary that recorded all the empty cells index(row,col) from the map and their relative orders
                            if neigh_pos["index"][0] == r and neigh_pos["index"][1] == c:
                                neighbour_pos = neigh_order
                        # Assign the probability(1/Number of neighbours) to the currently selected empty cell position in the Transition Matrix
                        # -> row of Transition Matrix = ordering of the currently selected empty cell
                        # -> col of Transition Matrix = ordering of the neighbouring empty cell from the currently selected empty cell
                        transition_Matrix[order][neighbour_pos-1] = 1/len(n)
            
                
def construct_ObservationMatrix(num_empty_cells, map, error_rate, four_bit_seq):
    actual_bit_seq = []
    for r in range(num_row):
        for c in range(num_col):
            if map[r][c] == '0':
                print("-"*100)
                print(f"Empty_Cells = [{r},{c}]")
                bit_seq = find_actual_bit_seq(cur_row_pos=r, cur_col_pos=c, map=map)
                actual_bit_seq.append(bit_seq)
    

    print(f"actual_bit_seq = {actual_bit_seq}")
    d_it_matrix = []
    for num_ob in four_bit_seq:
        print(f"observation_bit_seq = [{num_ob}]")
        ob_d_it_matrix = []
        for bit in actual_bit_seq:
            count_diff_bit = 0
            for i in range(4):
                if bit[i] != int(num_ob[i]):
                    count_diff_bit += 1
            ob_d_it_matrix.append(count_diff_bit)
        print(f"ob_d_it_matrix = {ob_d_it_matrix}")
        d_it_matrix.append(ob_d_it_matrix)

    for ob in range(len(d_it_matrix)):
        ob_matrix = np.zeros((num_empty_cells,num_empty_cells))
        for d_it in range(len(d_it_matrix[ob])):
            observation_val = ((1-error_rate)**(4-d_it_matrix[ob][d_it]))*((error_rate)**(d_it_matrix[ob][d_it]))
            ob_matrix[d_it][d_it] = observation_val
        observation_Matrix.append(ob_matrix)

def viterbi_algo(num_empty_cells, num_observation):
    initial_prob = [1/num_empty_cells]*num_empty_cells
    # print(f"\nInitial_pi :")
    # print(initial_prob)
    time_step = 0

    while time_step<num_observation:
        time_step += 1
        current_state_trellis = []
        print("*"*100)
        print(f"Time_Step : {time_step}")
        for t in range(num_empty_cells):
            max_prob = 0
            print(f"Starting State : S_{t}:")
            for t_1 in range(num_empty_cells):
                current_state_prob = 0
                if time_step == 1:
                    current_state_prob = initial_prob[t_1]
                    print(f"P[S_{t}|S_{t_1}] = {initial_prob[t_1]}")
                else:
                    current_state_prob = transition_Matrix[t_1][t] * trellis[time_step-2][t_1]
                    print(f"P[S_{t}|S_{t_1}] = transition_Matrix[{t_1}][{t}] * trellis[{time_step-2}][{t_1}] = {transition_Matrix[t_1][t]} * {trellis[time_step-2][t_1]} = {current_state_prob}")

                if current_state_prob > max_prob:
                    max_prob = current_state_prob
            print(f"Max_prob : {max_prob}")
            prob_of_currentstate_given_evidence = observation_Matrix[time_step-1][t][t] * max_prob
            print(f"observation val : {observation_Matrix[time_step-1][t][t]}")
            current_state_trellis.append(prob_of_currentstate_given_evidence)
            print("current_state_trellis:")
            print(current_state_trellis)
            print()
        trellis.append(current_state_trellis)
        print("trellis :")
        print(trellis)

    return trellis

def calculate_prob_empty_cells(map, num_observation):
    prob_of_location_at_each_time_step = []
    time_step = 0

    while time_step < num_observation:
        prob_at_each_location = np.zeros((num_row, num_col))
        time_step += 1
        
        # print(f"\nTime_Step : {time_step}")
        order_empty_cells = 0
        for r in range(num_row):
            for c in range(num_col):
                if map[r][c] == '0':
                    order_empty_cells += 1
                    num_neighbours, neighbours = cal_num_Neighbours(cur_row_pos=r, cur_col_pos=c, map=map)
                    # if num_neighbours > 0:
                    prob_at_each_location[r][c] = trellis[time_step-1][order_empty_cells-1]
                    # else:
                    #     prob_at_each_location[r][c] = trellis[time_step-1][order_empty_cells-1]
                    # print(f"{order_empty_cells} : [{r},{c}] --> {trellis[time_step-1][order_empty_cells-1] * num_neighbours}")
        # print(prob_at_each_location)
        prob_of_location_at_each_time_step.append(prob_at_each_location)

    return prob_of_location_at_each_time_step

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        lines = readFiles(filepath = filepath)

    # print(lines)
    map_row, map_col = lines[0].split()
    num_row = int(map_row)
    num_col = int(map_col)
    # print(f'map_row = {num_row}, map_col = {num_col}')

    # Store the 2d map into a 2d list
    map = []
    for row in range(int(map_row)):
        split_string = [item for item in lines[row+1] if (item == '0' or item == 'X')]
        map.append(split_string)
    
    # for i in map:
    #     print()
    #     for j in i:
    #         print(j , end = " ")

    # Calculate the number of empty cells and blocked cells in the map & record the position of the empty cells
    empty_cells  = 0
    blocked_cells = 0
    for i in range(num_row):
        for j in range(num_col):
            if map[i][j] == '0':
                empty_cells += 1
                pos_dict = {"index":[i,j]}
                list_empty_cells[empty_cells] = pos_dict
            else:
                blocked_cells += 1
            
    # print(f'empty_cells = {empty_cells}, blocked_cells = {blocked_cells}')
    # print(f'list of empty_cells position : {list_empty_cells}')

    # Number of sensor observations
    num_observation = int(lines[int(map_row)+1])

    # Four-Bit sequence of compass direction for blocked cells
    four_bit_seq = []
    for i in range(int(map_row) + 2, int(map_row) + 2 + int(num_observation)):
        split_string = [item for item in lines[i]]
        four_bit_seq.append(split_string)
    # print(four_bit_seq)

    # Error Rate of the sensor
    error_rate = float(lines[-1])
    # print(f'Error_Rate = {error_rate}')
    
    # Step 1: Construct the Transition Matrix for all the possible empty cells
    transition_Matrix = np.zeros((empty_cells,empty_cells))
    # print(f"transition_Matrix size : [{empty_cells},{empty_cells}]")
    construct_TransitionMatrix(num_empty_cells=empty_cells, map=map)
    # for i in transition_Matrix:
    #     print()
    #     for j in i:
    #         print(j, end=" ")
    # print(list_empty_cells)
    # Step 2: Construct the Observation Matrix for all the given observations from the sensor
    construct_ObservationMatrix(num_empty_cells=empty_cells, map=map, error_rate=error_rate, four_bit_seq=four_bit_seq)
    # print(list_empty_cells)
    count = 0
    for i in observation_Matrix:
        count += 1
        print(f"observation_Matrix : {count}")
        for j in i:
            print(j, end=" ")
    print()

    # Step 3: Calculate the Trellis using the viterbi algorithm
    trellis = viterbi_algo(num_empty_cells=empty_cells, num_observation=num_observation)
    # count = 0
    # for i in trellis:
    #     count += 1
    #     print(f"Trellis : {count}")
    #     for j in i:
    #         print(j)
    # # # Step 4: Caculate the probability of each empty cells for each of the different observations
    prob_at_each_location_for_each_t = calculate_prob_empty_cells(map=map, num_observation=num_observation)
    print(prob_at_each_location_for_each_t)
    np.savez("output.npz", *prob_at_each_location_for_each_t)


    
    



