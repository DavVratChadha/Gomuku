#Project 2
#Gomoku game
#By- Dav Vrat Chadha and Mehul Bhardwaj

import math

def print_board(board):
    """Print the Gomoku board"""
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def score(board):
    """Compute and return the score for the position of the board, assuming black just moved."""
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def play_gomoku(board_size):
    """Allow user to play the game against the computer"""
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        #analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        #analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x

def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))

def is_empty(board):
    """Return True if there is no stone on the board"""
    for y in board:
        for x in y:
            if x != " ": #if board not empty
                return False
    return True #else True

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    """Analyse the sequence of length 'length' which ends at location (y end, x end). Return "OPEN" if the sequence is open, "SEMIOPEN" if the sequence if semi-open, and "CLOSED" if the sequence is closed."""
    #check for end_1
    end_point_mark = board[y_end][x_end] #w or b
    extend_y1 = y_end + d_y
    extend_x1 = x_end + d_x
    end_1 = end_checker(board, extend_y1, extend_x1, end_point_mark)

    #check for end_2
    extend_y2 = y_end - length * d_y
    extend_x2 = x_end - length * d_x
    end_2 = end_checker(board, extend_y2, extend_x2, end_point_mark)

    if end_1 == end_2: #both ends open/closed
        if end_1 == "OPEN":
            return "OPEN"
        else:
            return "CLOSED"
    else:
        return "SEMIOPEN"

def end_checker(board, extend_y, extend_x, end_point_mark):
    size = len(board) - 1
    if extend_y > size or extend_y < 0 or extend_x > size or extend_x < 0:
        end = "CLOSED"
    else:
        extend_end_mark = board[extend_y][extend_x] #w or b or " "
        if extend_end_mark == end_point_mark or extend_end_mark == " ":
            end = "OPEN"
        else:
            end = "CLOSED"
    return end

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    """Return a tuple whose first element is the number of open
sequences of colour 'col' of length 'length' in the row, and whose second element is the number of semi-open sequences of colour 'col' of length 'length' in the row."""
    marks = []
    marks_coord = []
    counter = 0
    prev_coord_index = -1
    open_seq_count = 0
    semi_open_seq_count = 0
    key = False
    limit = limiter(board, y_start, x_start, d_y, d_x)

    for i in range(limit):
        marks_coord.append([y_start + d_y*i,x_start + d_x*i])
        marks.append(board[marks_coord[i][0]][marks_coord[i][1]])

        if marks[i] == col:
            counter += 1
            prev_coord_index = i
            if i == limit - 1 and counter == length:
                key = True

        elif counter == length:
            key = True

        else:
            counter = 0
            prev_coord_index = -1
            key = False

        if key:
            y_end = marks_coord[prev_coord_index][0]
            x_end = marks_coord[prev_coord_index][1]
            bound = is_bounded(board, y_end, x_end, counter, d_y, d_x)
            if bound == "OPEN":
                open_seq_count += 1
            elif bound == "SEMIOPEN":
                semi_open_seq_count += 1
            counter = 0
            prev_coord_index = -1
            key = False
    return open_seq_count, semi_open_seq_count

def limiter(board, y_start, x_start, d_y, d_x):
    if d_y < 0:
        y_limit = y_start
    #y_limit is the number of steps you can go in a given y direction
    elif d_y == 0:
        y_limit = math.inf
    else:
        y_limit = len(board) - 1 - y_start

    if d_x < 0:
        x_limit = x_start
    #x_limit is the number of steps you can go in a given x direction
    elif d_x == 0:
        x_limit = math.inf
    else:
        x_limit = len(board) -1 - x_start

    limit = min(y_limit, x_limit) + 1

    return limit


def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    a,b,c,d,e,f,g,h,k,l,m,n = 0,0,0,0,0,0,0,0,0,0,0,0

    for i in range(len(board)):
        a, b = detect_row(board, col, i, 0, length, 0, 1) #each row
        c, d = detect_row(board, col, 0, i, length, 1, 0) #each column
        e, f = detect_row(board, col, i, 0, length, 1, 1)
        #each right down diagonal from left edge

        if i != 0: #coz right down diagonal already considered
            g, h = detect_row(board, col, 0, i, length, 1, 1)
            #each right down diagonal from top edge

        k, l = detect_row(board, col, i, 0, length, -1, 1)
        #each right up diagonal from left edge
        if i != 0:
            m, n = detect_row(board, col, len(board)-1, i, length, -1, 1)
            #each right up diagonal from left edge

        open_seq_count += a + c + e + g + k + m
        semi_open_seq_count += b + d + f + h + l + n

    return open_seq_count, semi_open_seq_count


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()


def search_max(board):
    score_list = []
    ind_list = []

    for row in range(len(board)):
        for column in range(len(board[0])):
            new_board = board_duplicator(board)
            if new_board[row][column] == " ":
                new_board[row][column] = "b"
                new_score = score(new_board)
                score_list.append(new_score)
                ind_list.append([row,column])

    max_ind = score_list.index(max(score_list))
    move_y = ind_list[max_ind][0]
    move_x = ind_list[max_ind][1]

    return move_y, move_x


def board_duplicator(board):
    similar_new_board = []
    for row in board: #creating a deep copy
        similar_new_board.append(row.copy())
    return similar_new_board



def is_win(board):
    col = ["b", "w"]
    color = ["Black", "White"]

    for i in range(len(col)):
        closed = closed_detect_rows(board, col[i], 5)
        open, semi_open = detect_rows(board, col[i], 5)
        total = closed + open + semi_open
        if total >= 1:
            return color[i] + " won"

    draw = full_board_covered(board)
    if draw:
        return "Draw"
    #if no color won and board is fully covered, its a tie

    else:
        return "Continue playing"

def full_board_covered(board):
    """Return True if there is no empty place on the board"""
    for y in board:
        for x in y:
            if x == " ": #if board not fully covered
                return False
    return True #else True

def closed_detect_row(board, col, y_start, x_start, length, d_y, d_x):
    marks = []
    marks_coord = []
    counter = 0
    prev_coord_index = -1
    closed_seq_count = 0
    key = False
    limit = limiter(board, y_start, x_start, d_y, d_x)

    for i in range(limit):
        marks_coord.append([y_start + d_y*i,x_start + d_x*i])
        marks.append(board[marks_coord[i][0]][marks_coord[i][1]])

        if marks[i] == col:
            counter += 1
            prev_coord_index = i
            if i == limit - 1 and counter == length:
                key = True

        elif counter == length:
            key = True

        else:
            counter = 0
            prev_coord_index = -1
            key = False

        if key:
            y_end = marks_coord[prev_coord_index][0]
            x_end = marks_coord[prev_coord_index][1]
            bound = is_bounded(board, y_end, x_end, counter, d_y, d_x)
            if bound == "CLOSED":
                closed_seq_count += 1
            counter = 0
            prev_coord_index = -1
            key = False

    return closed_seq_count



def closed_detect_rows(board, col, length):
    closed_seq_count = 0
    a,b,c,d,e,f,g,h,k,l,m,n = 0,0,0,0,0,0,0,0,0,0,0,0

    for i in range(len(board)):
        a = closed_detect_row(board, col, i, 0, length, 0, 1) #each row
        c = closed_detect_row(board, col, 0, i, length, 1, 0)
        #each column
        e = closed_detect_row(board, col, i, 0, length, 1, 1)
        #each right down diagonal from left edge

        if i != 0: #coz right down diagonal already considered
            g = closed_detect_row(board, col, 0, i, length, 1, 1)
            #each right down diagonal from top edge

        k = closed_detect_row(board, col, i, 0, length, -1, 1)
        #each right up diagonal from left edge
        if i != 0:
            m = closed_detect_row(board, col, len(board)-1, i, length, -1, 1)
            #each right up diagonal from left edge

        closed_seq_count += a + c + e + g + k + m
    return closed_seq_count


def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




if __name__ == '__main__':
    play_gomoku(8)

    """
             #0   #1   #2   #3   #4   #5   #6   #7
    board =[[' ', 'w', ' ', ' ', ' ', ' ', 'w', ' '], #0
            [' ', 'w', ' ', 'b', ' ', 'w', ' ', ' '], #1
            [' ', ' ', 'b', ' ', 'w', ' ', 'w', ' '], #2
            [' ', 'b', ' ', ' ', ' ', ' ', ' ', 'w'], #3
            [' ', 'b', 'w', ' ', ' ', ' ', ' ', ' '], #4
            [' ', 'w', ' ', ' ', ' ', 'b', ' ', ' '], #5
            ['w', 'w', ' ', ' ', ' ', ' ', 'b', ' '], #6
            ['w', ' ', 'b', 'b', ' ', ' ', 'b', 'b']] #7

    print(detect_row(board,"w",6,0,3,-1,1)) #Right up
    print(detect_row(board,"w",0,4,3,1,1)) #Right down
    print(detect_row(board,"w",3,7,3,-1,-1)) #left up
    print(detect_row(board,"w",0,6,3,1,-1)) #left down

    print(detect_row(board,"b",0,0,2,1,1)) #right down diag
    print(detect_row(board,"b",7,7,2,-1,-1)) #left up diag

    print(detect_row(board,"w",7,0,1,-1,1)) #right up diag
    print(detect_row(board,"w",0,7,1,1,-1)) #left down diag

    print(detect_row(board,"b",7,0,2,0,1)) #right
    print(detect_row(board,"w",0,1,2,1,0)) #down diag
    print(detect_row(board,"w",6,0,2,1,0)) #down diag

             #0    1    2    3    4    5    6    7
    board =[[' ', ' ', 'w', ' ', ' ', ' ', 'w', ' '], #0
            [' ', 'w', 'b', ' ', ' ', 'w', 'w', ' '], #1
            ['w', ' ', 'b', 'w', 'w', ' ', 'w', ' '], #2
            [' ', ' ', 'b', 'w', ' ', ' ', ' ', ' '], #3
            [' ', ' ', 'b', 'w', 'w', ' ', 'w', ' '], #4
            [' ', ' ', 'b', ' ', ' ', ' ', ' ', ' '], #5
            ['w', ' ', 'w', ' ', ' ', ' ', ' ', ' '], #6
            [' ', ' ', 'w', 'w', 'w', ' ', ' ', ' ']] #7

    board =[['w', 'w', 'w', 'w', 'b', 'b', 'b', 'b'],
            ['w', 'w', 'w', 'b', 'w', 'b', 'w', 'b'],
            ['w', 'w', 'w', 'w', 'b', 'b', 'b', 'b'],
            ['w', 'w', 'w', 'w', 'b', 'w', 'b', 'b'],
            ['b', 'b', 'b', 'w', 'b', 'w', 'w', 'w'],
            ['b', 'b', 'b', 'w', 'w', 'b', 'w', 'w'],
            ['b', 'b', 'b', 'b', 'w', 'w', 'w', 'w'],
            ['b', 'b', 'b', 'b', 'w', 'w', 'w', 'w']]
    #print(detect_rows(board, "w", 3))
    print(is_win(board))
    """

