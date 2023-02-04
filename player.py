BOARD_START = 0
BOARD_END = 7
EMPTY_SQUARE = -1

def is_outside_of_board(row, col):
    if row < BOARD_START or row > BOARD_END or col < BOARD_START or col > BOARD_END:
        return True

class MyPlayer:
    ''' A reverse game player who analyzes the position where to play '''
    def __init__(self, my_color, opponent_color):
        self.name = 'gavulsim'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.my_discs_array = []
        self.array_of_moves = []
        self.number_of_empty_pos = 0
        self.player_move = None
        self.dir1 = [-1, -1, -1, 0, 0, 1, 1, 1]
        self.dir2 = [-1, 0, 1, -1, 1, -1, 0, 1]
        self.value_of_move = 0
    
    #Go through every position on the board and return its position (row, column)
    def check_all_pos(self, board):
        for r in range(len(board)):
            for c in range(len(board[r])):
                yield r, c

    #Find all my discs on the board and append their position (row, column) to an array
    def find_discs(self, board):
        for pos in self.check_all_pos(board):
            pos_value = board[pos[0]][pos[1]]
            if pos_value == self.my_color:
                self.my_discs_array.append(pos)
            if(pos_value == EMPTY_SQUARE):
                self.number_of_empty_pos += 1

    #Evaluate value of discs, that can be flipped
    def evaluate_flipped_discs(self, new_row, new_col):
        if self.number_of_empty_pos > 20:
            #Increase value of border discs
            if new_row == BOARD_START or new_row == BOARD_END or new_col == BOARD_START or new_col == BOARD_END:
                self.value_of_move += 2
            #Increase the value of the discs, that are in the middle 2x2 square
            elif (new_row, new_col) in ((3, 3), (3, 4), (4, 3), (4, 4)):
                self.value_of_move  += 4
            #Increase the value of the discs, that are in the middle 4x4 square
            elif new_row >= 2 and new_row <= 5 and new_col >= 2 and new_col <= 5:
                self.value_of_move  += 3
            #Value of normal discs
            else:
                self.value_of_move  += 1
        else:
            self.value_of_move  += 1

    def evaluate_corner_move(self, new_row, new_col):
        if (new_row, new_col) in ((BOARD_END, BOARD_END), (BOARD_START, BOARD_START), (BOARD_START, BOARD_END), (BOARD_END, BOARD_START)):
            self.value_of_move  *= 100

    def evaluate_border_move(self, new_row, new_col):
        if new_row == BOARD_START or new_row == BOARD_END or new_col == BOARD_START or new_col == BOARD_END:
            self.value_of_move *= 10

    #Dicrease value of discs on unsatisfactory position - second border and discs around corner discs
    def evaluate_unsatisfactory_move(self, new_row, new_col):
        if new_row == 1 or new_row == 6 or new_col == 1 or new_col == 6:
            self.value_of_move /= 20
        if (new_row, new_col) in ((1, 1), (1, 6), (6, 1), (6, 6)):
            self.value_of_move  /= 30

    #Check if the player can place the disc on the position
    def check_valid_position(self, board, new_row, new_col):
        if(board[new_row][new_col] == EMPTY_SQUARE):
            self.evaluate_position_of_move(new_row, new_col)

    def evaluate_position_of_move(self, new_row, new_col):
        self.evaluate_corner_move(new_row, new_col)
        self.evaluate_border_move(new_row, new_col)
        if self.number_of_empty_pos > 20:
            self.evaluate_unsatisfactory_move(new_row, new_col)
        self.array_of_moves.append([new_row, new_col, self.value_of_move])

    def find_move(self, row, col, board, i):
        while True:
            #increase row and column by direction
            row += self.dir1[i]
            col += self.dir2[i]

            #validate if row and column is in the board range 
            if is_outside_of_board(row, col):
                break
            
            #check if opponent disc is on the position, if not break the cycle
            if board[row][col] != self.opponent_color:
                break
            
            new_row = row + self.dir1[i]
            new_col = col + self.dir2[i]

            #validate if a new row and a new column is in the board range
            if is_outside_of_board(new_row, new_col):
                break
            
            self.evaluate_flipped_discs(new_row, new_col)
            #check if the position is empty, if so evaluate the position and add coordinates of the position to the array
            self.check_valid_position(board, new_row, new_col)

    def find_all_moves(self, board, r, c):
        #cycle every directions
        for i in range(len(self.dir1)):
            self.value_of_move = 0
            #add to variables row and column coordinates of my disc in my_disc_array
            row = r
            col = c
            self.find_move(row, col, board, i)

    def go_through_every_element_in_discs_array(self, board):
        for i in range(len(self.my_discs_array)):
            row = self.my_discs_array[i][0]
            col = self.my_discs_array[i][1]
            self.find_all_moves(board, row, col)
    
    def compare_values_of_moves(self, best_value_of_move):
        #Find the move with the highest move value
        for i in range(len(self.array_of_moves)):
            if best_value_of_move < self.array_of_moves[i][2]:
                best_value_of_move = self.array_of_moves[i][2]
                row = self.array_of_moves[i][0]
                col = self.array_of_moves[i][1]
                self.player_move = (row, col)

    def choose_best_move(self):
        #Add first move as the best move and then compare it with other moves
        best_value_of_move = self.array_of_moves[0][2]
        row = self.array_of_moves[0][0]
        col = self.array_of_moves[0][1]
        self.player_move = (row, col)
        self.compare_values_of_moves(best_value_of_move)

    def move(self, board):
        #set arrays to empty
        self.my_discs_array = []
        self.array_of_moves = []
        self.number_of_empty_pos = 0

        self.find_discs(board)
        #go through every element (my disc) in my_disc_array and find all moves
        self.go_through_every_element_in_discs_array(board)
        #check if exists any valid move, if not return error
        if len(self.array_of_moves) == 0:
            return None
        #Choose and return move
        self.choose_best_move()
        return self.player_move