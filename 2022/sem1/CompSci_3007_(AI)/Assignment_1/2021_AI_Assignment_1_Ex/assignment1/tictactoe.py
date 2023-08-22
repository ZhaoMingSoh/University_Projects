# Weizhen Fang
# a1781116
# Artificial Intelligence Assignment 1

import sys
import copy

#store all positions of '-' spaces in a list
def successors(board_state):
    empty_spaces = []
    for i in range(3):
        for j in range(3):
            if (board_state[i][j] == '-'):
                empty_spaces.append((i, j))
    return empty_spaces

# check if space of the action has been replaced
def checkMove(board_state, action):
    row = action[0]
    col = action[1]
    board_copy = copy.deepcopy(board_state)
    number_O = 0
    number_X = 0

    for i in range(3):
        for j in range(3):
            if board_state[i][j] == 'o':
                number_O += 1
            elif board_state[i][j] == 'x':
                number_X += 1

    if(number_X == number_O):
        board_copy[row][col] = 'x'
    elif(number_X > number_O):
        board_copy[row][col] = 'o'
    return board_copy

# check if the game is stop
def ifstop(board_state):
    stop = True
    conti = False

    #If someone wins program ends, stop = true
    if (Checkwin(board_state) == 'x') or (Checkwin(board_state) == 'o'):
        return stop

    #if no one wins, check the number of empty space to see if continuous
    e = 0
    for i in range(3):
        for j in range(3):
            if (board_state[i][j] == '-'):
                e = e + 1
    if(e != 0):
        return conti
    else:
        return stop

# checks the board, checking for victories between player1 and player2
def Checkwin(board_state):
    for a in range(3):
        if (board_state[0][a] == board_state[1][a] == board_state[2][a]) and (board_state[0][a] != '-'):
            return board_state[0][a]

        if (board_state[a][0] == board_state[a][1] == board_state[a][2]) and (board_state[a][0] != '-'):
            return board_state[a][0]

    if ((board_state[0][0] == board_state[1][1] == board_state[2][2]) or (board_state[0][2] == board_state[1][1] == board_state[2][0])) and (board_state[1][1] != '-'):
        return board_state[1][1]
    else:
        return None

def utility(board_state):
    if Checkwin(board_state) == 'x':
        return 1
    elif Checkwin(board_state) == 'o':
        return -1
    else:
        return 0

# function to convert an array to a string
def string_to_array(board_state):
    board_array = [[0 for i in range(3)] for j in range(3)]
    k = 0

    #loop to assign board values to a 2D array
    for i in range(3):
        for j in range(3):
            board_array[i][j] = board_state[k]
            k += 1
    return board_array

# function to convert array to string
def array_to_string(board_state):
    state = ''

    for i in range(3):
        for j in range(3):
            state = state + board_state[i][j]

    return state

# function to find the minimax, and store the all the paths visited in an output file
# the parameter value is a initial position value visit each possible move by recursive operation
def minim(board_state,value):
    # check who's term
    number_O = 0
    number_X = 0
    for i in range(3):
        for j in range(3):
            if board_state[i][j] == 'o':
                number_O += 1
            elif board_state[i][j] == 'x':
                number_X += 1

    # if it's max's term, find the best move and store each possible movements in an output file
    if number_X == number_O:
        if ifstop(board_state) == True:
            return utility(board_state), value

        max_utility = -1000
        best_move = None

        # recursive to find each branch of traversed node, empty_spaces in the every possible move at the first step
        empty_spaces = successors(board_state)
        for action in empty_spaces:
            recur_maxvalue = minim(checkMove(board_state, action), action)

            # updating the max utility when find maximum value in recursive process
            if max_utility < recur_maxvalue[0]:
                max_utility = recur_maxvalue[0]
                best_move = action

            # write each traverse output in the output text file
            output_str = array_to_string(checkMove(board_state, action)) + ' ' + str(recur_maxvalue[0])
            write_to_file(output_str)
        return max_utility, best_move

    # if it's min term, find the best move and store each possible movements in an output file
    elif number_X > number_O:
        if ifstop(board_state) == True:
            return utility(board_state), value

        min_utility = 1000
        best_move = None

        # recursive to find each branch of traversed node, empty_spaces in the every possible move at the first step
        empty_spaces = successors(board_state)
        for action in empty_spaces:
            recur_minvalue = minim(checkMove(board_state, action), action)

            # updating the min utility when find minimum value in recursive process
            if min_utility > recur_minvalue[0]:
                min_utility = recur_minvalue[0]
                best_move = action

            # write each traverse output in the output text file
            output_str = array_to_string(checkMove(board_state, action)) + ' ' + str(recur_minvalue[0])
            write_to_file(output_str)
        return min_utility, best_move

# function for alpha_beta pruning,
# the parameter value is a initial position value visit each possible move by recursive operation
def alpha_beta(board_state,value,alpha,beta):
    # check who's term
    number_O = 0
    number_X = 0
    for i in range(3):
        for j in range(3):
            if board_state[i][j] == 'o':
                number_O += 1
            elif board_state[i][j] == 'x':
                number_X += 1

    # if it's max term, then find the best move of max
    if number_X == number_O:
        if ifstop(board_state) == True:
            return utility(board_state), value

        max_utility = -1000
        best_move = None

        # recursive to find each branch of traversed node, empty_spaces in the every possible move at the first step
        empty_spaces = successors(board_state)
        for action in empty_spaces:
            recur_maxvalue = alpha_beta(checkMove(board_state, action), action, alpha, beta)

            # updating the max utility when find maximum value in recursive process
            if max_utility < recur_maxvalue[0]:
                max_utility = recur_maxvalue[0]
                best_move = action

            # if max_uitility greater and equals to beta, then break
            if max_utility >= beta:
                output_str = array_to_string(checkMove(board_state, action)) + ' ' + str(recur_maxvalue[0])
                write_to_file(output_str)
                return max_utility, best_move

            # update alpha
            if max_utility > alpha:
                alpha = max_utility
            output_str = array_to_string(checkMove(board_state, action)) + ' ' + str(recur_maxvalue[0])
            write_to_file(output_str)

        return max_utility, best_move

    # if it's min term, then find the best move of min
    elif number_X > number_O:
        if ifstop(board_state) == True:
            return utility(board_state), value

        min_utility = 1000
        best_move = None

        # recursive to find each branch of traversed node, empty_spaces in the every possible move at the first step
        empty_spaces = successors(board_state)
        for action in empty_spaces:
            recur_minvalue = alpha_beta(checkMove(board_state, action),action,alpha,beta)

            # updating the min utility when find minimum value in recursive process
            if min_utility > recur_minvalue[0]:
                min_utility = recur_minvalue[0]
                best_move = action

            # if min_uitility less and equals to alpha, then break
            if min_utility <= alpha:
                output_str = array_to_string(checkMove(board_state, action)) + ' ' + str(recur_minvalue[0])
                write_to_file(output_str)
                return min_utility, best_move

            # update beta
            if min_utility < beta:
                beta = min_utility

            output_str = array_to_string(checkMove(board_state, action)) + ' ' + str(recur_minvalue[0])
            write_to_file(output_str)
        return min_utility, best_move

# function to caculate the E(s)
# E(s) = M(s) - O(s), which M(s) is the number of possible winning lines of Max and O(s) is the opposite
def evaluation(boardstate):
    Max_winning_lines = copy.deepcopy(boardstate)
    Min_winning_lines = copy.deepcopy(boardstate)
    Max_win = 0
    Min_win = 0

    # fill rest of the board state to x or o
    for i in range(3):
        for j in range(3):
            if(Max_winning_lines[i][j] == '-'):
                Max_winning_lines[i][j] = 'x'
            if(Min_winning_lines[i][j] == '-'):
                Min_winning_lines[i][j] = 'o'

    # loop tp find the possible winning lines of max
    for a in range(3):
        if (Max_winning_lines[0][a] == Max_winning_lines[1][a] == Max_winning_lines[2][a] == 'x'):
            Max_win += 1
        if (Max_winning_lines[a][0] == Max_winning_lines[a][1] == Max_winning_lines[a][2] == 'x'):
            Max_win += 1
    if (Max_winning_lines[0][0] == Max_winning_lines[1][1] == Max_winning_lines[2][2] == 'x'):
        Max_win += 1
    if (Max_winning_lines[0][2] == Max_winning_lines[1][1] == Max_winning_lines[2][0] == 'x'):
        Max_win += 1

    # caculate the number of possible winning lines of Max
    for a in range(3):
        if (Min_winning_lines[0][a] == Min_winning_lines[1][a] == Min_winning_lines[2][a] == 'o'):
            Min_win += 1
        if (Min_winning_lines[a][0] == Min_winning_lines[a][1] == Min_winning_lines[a][2] == 'o'):
            Min_win += 1
    if (Min_winning_lines[0][0] == Min_winning_lines[1][1] == Min_winning_lines[2][2] == 'o'):
        Min_win += 1
    if (Min_winning_lines[0][2] == Min_winning_lines[1][1] == Min_winning_lines[2][0] == 'o'):
        Min_win += 1

    E = Max_win - Min_win
    return E

# cut-off/terminate early the minimax tree traversal based on a heuristic or evaluation function
def early_termination(board_state, value, alpha, beta, cut_depth, depth):
    # check who's term
    number_O = 0
    number_X = 0
    for i in range(3):
        for j in range(3):
            if board_state[i][j] == 'o':
                number_O += 1
            elif board_state[i][j] == 'x':
                number_X += 1

    # When Max term
    if number_X == number_O:
        # recursive base cases
        if ifstop(board_state) == True:
            return evaluation(board_state), value

        # if traversed depth is greater and equal to defined
        if depth >= cut_depth:
            return evaluation(board_state), value

        max_utility = -1000
        best_move = None

        # recursive to find each branch of traversed node, empty_spaces in the every possible move at the first step
        empty_spaces = successors(board_state)
        for action in empty_spaces:
            recur_maxvalue = early_termination(checkMove(board_state, action), action, alpha, beta, cut_depth, depth+1)

            # updating the max utility when find maximum value in recursive process
            if max_utility < recur_maxvalue[0]:
                max_utility = recur_maxvalue[0]
                best_move = action

            # if max_uitility is grater and equal to beta, then break, write the output in text file
            if max_utility >= beta:
                output_str = array_to_string(checkMove(board_state, action)) + ' ' + str(recur_maxvalue[0])
                write_to_file(output_str)
                return max_utility, best_move

            # update alpha
            if max_utility > alpha:
                alpha = max_utility

            output_str = array_to_string(checkMove(board_state, action)) + ' ' + str(recur_maxvalue[0])
            write_to_file(output_str)
        return max_utility, best_move

    # When Min term
    elif number_X > number_O:
        # revursive base cases
        if ifstop(board_state) == True:
            return evaluation(board_state), value

        # break out when reverse depth is greater than defined cut depth
        if depth >= cut_depth:
            return evaluation(board_state), value

        min_utility = 1000
        best_move = None

        # recursive to find each branch of traversed node, empty_spaces in the every possible move at the first step
        empty_spaces = successors(board_state)
        for action in empty_spaces:
            recur_minvalue = early_termination(checkMove(board_state, action), action, alpha, beta, cut_depth, depth+1)

            # updating the min utility when find minimum value in recursive process
            if min_utility > recur_minvalue[0]:
                min_utility = recur_minvalue[0]
                best_move = action

            # if min_uitility is less and equal to alpha, then break, write the output in text file
            if min_utility <= alpha:
                output_str = array_to_string(checkMove(board_state, action)) + ' ' + str(recur_minvalue[0])
                write_to_file(output_str)
                return min_utility, best_move

            # update beta
            if min_utility < beta:
                beta = min_utility

            output_str = array_to_string(checkMove(board_state, action)) + ' ' + str(recur_minvalue[0])
            write_to_file(output_str)
        return min_utility, best_move

def write_to_file(str):
    file = open(sys.argv[2], "a")
    file.write(str + '\n')
    file.close()

if __name__ == "__main__":
    file = open(sys.argv[2], "w")
    file.write("")
    file.close()

    # capture string input
    board = sys.argv[1]

    state_array = string_to_array(board)

    a = ()
    initial_position = (-10000,-10000)
    initial_alpha = -1000
    initial_beta = 1000
    if(len(sys.argv) == 3):
        a = minim(state_array,initial_position)
    elif(len(sys.argv) == 4):
        a = alpha_beta(state_array,initial_position,initial_alpha,initial_beta)
    elif(len(sys.argv) == 5):
        depth = int(sys.argv[4])
        a = early_termination(state_array,initial_position, initial_alpha, initial_beta,depth,0)

    best_move = checkMove(state_array, a[1])
    print(array_to_string(best_move))