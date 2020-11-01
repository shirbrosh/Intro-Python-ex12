from .ai import *


class Game:
    EMPTY_CELL = '_'
    LEN_ROW = 6
    LEN_COL = 7
    PLAYER1_COLOR = 'R'
    PLAYER2_COLOR = 'B'
    PLAYER1 = 1
    PLAYER2 = 2
    WIN1 = 'RRRR'
    WIN2 = 'BBBB'
    TIE = 0
    FIRST_ROW = 0
    FOUR_IN_A_ROW = 4

    def __init__(self):
        """A constructor for a Game object"""

        self.board = self.create_empty_board()
        self.player_turn = self.PLAYER1
        self.winner = None
        self.player1_lst = []
        self.player2_lst = []
        self.ai1 = AI(self, self.PLAYER1)
        self.ai2 = AI(self, self.PLAYER2)

    def reset_winner(self):
        """
        This method resets the winner for a new game
        """
        self.winner = None

    def reset_players(self):
        """
        This method resets the players for a new game
        """
        self.player1_lst = []
        self.player2_lst = []
        self.player_turn = self.PLAYER1

    def create_empty_board(self):
        """
        This method creates an empty board
        """
        board = []
        for row in range(self.LEN_ROW):
            board_row = []
            for col in range(self.LEN_COL):
                board_row.append(self.EMPTY_CELL)
            board.append(board_row)
        return board

    def reset_board(self):
        """
        This method resets the board for a new game
        """
        self.board = self.create_empty_board()

    def __str__(self):
        """
        This method prints the game board.
        """
        board_str = ""
        board = self.board
        for i in range(self.LEN_ROW):
            for j in range(self.LEN_COL):
                if j == self.LEN_COL - 1:
                    board_str += board[i][j] + "\n"
                else:
                    board_str += board[i][j] + " "
        return board_str

    def get_board(self):
        """
        This method returns the board
        """
        return self.board

    def get_row_for_disc(self, col):
        """
        This method returns the lowest free row number in the given coulomb
        if coulomb is full, return False
        """
        for i in range(self.LEN_ROW - 1, -1, -1):
            if self.board[i][col] == self.EMPTY_CELL:
                return i
        return False

    def __illegal_move(self, column):
        """
        This method receives the column number and will raise a an exception if the
        move is illegal.
        """
        if self.winner is not None:
            raise Exception("Illegal move")
        if column not in range(self.LEN_COL):
            raise Exception("Illegal move")
        if self.get_row_for_disc(column) is False:
            raise Exception("Illegal move")

    def make_move(self, column):
        """
        This method receives a column number. if the column is 'legal' according to
        the exercise rules then the method will input the disc in to the game in
        the lowest free row in that column. the method is used for player vs player
        """
        # check if illegal move
        self.__illegal_move(column)
        # if clear, input the disc
        row = self.get_row_for_disc(column)
        if self.get_current_player() == self.PLAYER1:
            self.board[row][column] = self.PLAYER1_COLOR
            self.player1_lst.append((row, column))
            self.player_turn = self.PLAYER2
        else:
            self.board[row][column] = self.PLAYER2_COLOR
            self.player2_lst.append((row, column))
            self.player_turn = self.PLAYER1
            # check for winner
        self.get_winner()

    def make_move_pvc(self, col_player):
        """
        This method receives a column number. if the column is 'legal' according to
        the exercise rules then the method will input the disc in to the game in
        the lowest free row in that column. the method is used for player vs computer
        """
        row_player = self.get_row_for_disc(col_player)
        self.board[row_player][col_player] = self.PLAYER1_COLOR
        self.player1_lst.append((row_player, col_player))
        self.player_turn = self.PLAYER2
        # if the game has ended,then return nothing for the ai
        if self.get_winner():
            return None, None
        # find col,row for ai and return it
        col_ai = self.ai2.find_legal_move()
        row_ai = self.get_row_for_disc(col_ai)
        self.board[row_ai][col_ai] = self.PLAYER2_COLOR
        self.player2_lst.append((row_ai, col_ai))
        self.player_turn = self.PLAYER1
        # check if game has ended
        self.get_winner()
        return row_ai, col_ai

    def make_move_cvp(self, col_player=None):
        """
        This method receives a column number. if the column is 'legal' according to
        the exercise rules then the method will input the disc in to the game in
        the lowest free row in that column.the method is used for computer vs player
        """
        # if this is the first turn,then play only ai:
        if col_player is not None:
            row_player = self.get_row_for_disc(col_player)
            self.player2_lst.append((row_player, col_player))
            self.board[row_player][col_player] = self.PLAYER2_COLOR
            self.player_turn = self.PLAYER1
            # if the game has ended,then return nothing for the ai
            if self.get_winner():
                return None, None
        col_ai = self.ai1.find_legal_move()
        row_ai = self.get_row_for_disc(col_ai)
        self.board[row_ai][col_ai] = self.PLAYER1_COLOR
        self.player1_lst.append((row_ai, col_ai))
        self.player_turn = self.PLAYER2
        # check for winner
        self.get_winner()
        return row_ai, col_ai

    def make_move_cvc(self):
        """
        This method receives a column number.if the column is 'legal' according to
        the exercise rules then the method will input the disc in to the game in the
        lowest free row in that column.the method is used for computer vs computer
        """
        if self.get_current_player() == self.PLAYER1:
            col_ai = self.ai1.find_legal_move()
            row_ai = self.get_row_for_disc(col_ai)
            self.board[row_ai][col_ai] = self.PLAYER1_COLOR
            self.player1_lst.append((row_ai, col_ai))
            self.player_turn = self.PLAYER2
            self.get_winner()
        # player 2 turn
        else:
            col_ai = self.ai2.find_legal_move()
            row_ai = self.get_row_for_disc(col_ai)
            self.board[row_ai][col_ai] = self.PLAYER2_COLOR
            self.player2_lst.append((row_ai, col_ai))
            self.player_turn = self.PLAYER1
            self.get_winner()
        return col_ai, row_ai

    def __direction_is_horizontal(self, board):
        """
        This method checks if one of the players has won the game horizontally.
        """
        for row in range(len(board)):
            list_to_str = ''.join(board[row])
            if self.WIN1 in list_to_str:
                self.winner = self.PLAYER1
                return
            elif self.WIN2 in list_to_str:
                self.winner = self.PLAYER2
                return

    def __direction_is_vertical(self):
        """
        This method checks if one of the players has won the game vertically.
        """
        board_transpose = [list(i) for i in zip(*self.board)]
        self.__direction_is_horizontal(board_transpose)

    def __direction_is_diagonal_right(self, board):
        """
        This method checks if one of the players has won the game diagonal right.
        """
        board_transpose = self.__turn_board_diagonal(board)
        self.__direction_is_horizontal(board_transpose)

    def __direction_is_diagonal_left(self, board):
        """
        This method checks if one of the players has won the game diagonal left.
        """
        board_transpose = self.__turn_board_up_side_down(board)
        self.__direction_is_diagonal_right(board_transpose)

    def __turn_board_up_side_down(self, board):
        """
        This method receives a board and returns it upside down.
        """
        new_board = []
        for i in range(self.LEN_ROW - 1, -1, -1):
            new_board.append(board[i])
        return new_board

    def __turn_board_diagonal(self, board):
        """
        This method receives a board and returns it upside down.
        """
        diagonal_board = []
        # upper triangle
        i = 0
        while i < self.LEN_COL:
            j = 0
            diagonal_board_row = []
            for row in board:
                if j + i < self.LEN_COL:
                    diagonal_board_row.append(row[j + i])
                    j += 1
            i += 1
            diagonal_board.append(diagonal_board_row)
        # lower triangle
        j = 1
        while j < self.LEN_ROW:
            i = 0
            diagonal_board_row = []
            for row in range(j, self.LEN_ROW):
                if i < self.LEN_ROW - 1 and i < self.LEN_ROW:
                    diagonal_board_row.append(board[row][i])
                    i += 1
            j += 1
            diagonal_board.append(diagonal_board_row)
        return diagonal_board

    def get_winner(self):
        """
        This method will set the winner attribute to who won/tie or None, according
        to the game board.
        """
        # if the first row is full then the whole board is full.
        if self.EMPTY_CELL not in self.board[self.FIRST_ROW] and self.winner is None:
            self.winner = self.TIE
            return self.winner
        # else, then search for a winner in all directions
        self.__direction_is_horizontal(self.board)
        if self.winner is not None:
            return self.winner
        self.__direction_is_vertical()
        if self.winner is not None:
            return self.winner
        self.__direction_is_diagonal_right(self.board)
        if self.winner is not None:
            return self.winner
        self.__direction_is_diagonal_left(self.board)
        if self.winner is not None:
            return self.winner

    def get_player_at(self, row, col):
        """
        This method receives a cell coordinate and returns the player number
        that's in it. if the cell is empty, then return None
        """
        cell_content = self.board[row][col]
        if cell_content == self.EMPTY_CELL:
            return None
        elif cell_content == self.PLAYER1_COLOR:
            return self.PLAYER1
        else:
            return self.PLAYER2

    def get_current_player(self):
        """
        returns players turn to play.
        """
        return self.player_turn

    def get_winner_row_col_lst_color(self, player):
        """
        returns the winning player's last row(int),last col(int),
        move list(list of tuples) and color(string) in the the
        board. (R or B)
        """
        if player == self.PLAYER1:
            color = self.PLAYER1_COLOR
            last_row = self.player1_lst[-1][0]
            last_col = self.player1_lst[-1][1]
            move_lst = self.player1_lst
        else:
            color = self.PLAYER2_COLOR
            last_row = self.player2_lst[-1][0]
            last_col = self.player2_lst[-1][1]
            move_lst = self.player2_lst
        return last_row, last_col, move_lst, color

    def is_winner_vertical(self, last_col, last_row, move_lst):
        """
        this method is activated when a player has won,and will search for the
        winning discs. this method will return the coordinates of the winning discs
        in a list.
        """
        # filter for winning col only
        winning_col = list(filter(lambda x: x[1] == last_col, move_lst))
        # filter for rows going down from last winning disc (0 to 3).
        win_lst = list(
            filter(lambda x: x[0] in range(last_row, last_row + 4), winning_col))
        if len(win_lst) == self.FOUR_IN_A_ROW:
            return win_lst
        return None

    def is_winner_horizontal(self, last_row, color):
        """
        this method is activated when a player has won,and will search for the
        winning discs horizontally.
        this method will return the coordinates of the winning discs in a list.
        """
        list_to_str = ''.join(self.board[last_row])
        count = 0
        index = None
        win_lst = []
        # search 4 discs in a row and save last index of last letter.
        for i in range(len(list_to_str)):
            if list_to_str[i] == color:
                count += 1
            else:
                count = 0
            if count == self.FOUR_IN_A_ROW:
                index = i
                break
        if count == self.FOUR_IN_A_ROW:
            # if found 4 discs in a row then append coordinates to win_lst
            for i in range(self.FOUR_IN_A_ROW):
                win_lst.append((last_row, index - i))
            return win_lst
        return None

    def is_winner_diagonal_up_right(self, last_col, last_row, color):
        """
        this method is activated when a player has won,and will search for the
        winning discs diagonally (up right) and (down let).
        this method will return the coordinates of the winning discs in a list.
        """
        win_lst = []
        i = 0
        # count 3 to the right,stop if the disc changed color or out of board range.
        while i < 4 and last_row - i in range(
                self.LEN_ROW) and last_col + i in range(self.LEN_COL):
            if self.board[last_row - i][last_col + i] == color:
                win_lst.append((last_row - i, last_col + i))
                i += 1
            else:
                break
        count = len(win_lst)
        i = 1
        # search for rest of wining discs in the other direction
        while i < 5 - count and last_row + i in range(
                self.LEN_ROW) and last_col - i in range(self.LEN_COL):
            if self.board[last_row + i][last_col - i] == color:
                win_lst.append((last_row + i, last_col - i))
                i += 1
            else:
                break
        if len(win_lst) == self.FOUR_IN_A_ROW:
            return win_lst
        return None

    def is_winner_diagonal_up_left(self, last_col, last_row, color):
        """
        this method is activated when a player has won,and will search for the
        winning discs diagonally (up left) and (down right).
        this method will return the coordinates of the winning discs in a list.
        """
        win_lst = []
        i = 0
        # count 3 to the left,stop if the disc changed color or out of board range.
        while i < 4 and last_row - i in range(6) and last_col - i in range(7):
            if self.board[last_row - i][last_col - i] == color:
                win_lst.append((last_row - i, last_col - i))
                i += 1
            else:
                break
        count = len(win_lst)
        i = 1
        # search for rest of wining discs in the other direction
        while i < 5 - count and last_row + i in range(6) and last_col + i in range(
                7):
            if self.board[last_row + i][last_col + i] == color:
                win_lst.append((last_row + i, last_col + i))
                i += 1
            else:
                break
        if len(win_lst) == self.FOUR_IN_A_ROW:
            return win_lst
        return None

    def get_wining_discs(self, player):
        """
        this method is activated when a player has won,and will search for the
        winning discs in all directions. it will return a list of coordinated of
        the winning discs.
        """
        last_row, last_col, move_lst, color = self.get_winner_row_col_lst_color(
            player)
        # vertical check
        win_lst = self.is_winner_vertical(last_col, last_row, move_lst)
        if win_lst is not None:
            return win_lst
        # horizontal check
        win_lst = self.is_winner_horizontal(last_row, color)
        if win_lst is not None:
            return win_lst
        # diagonal right up check
        win_lst = self.is_winner_diagonal_up_right(last_col, last_row, color)
        if win_lst is not None:
            return win_lst
        # diagonal left up check
        win_lst = self.is_winner_diagonal_up_left(last_col, last_row, color)
        if win_lst is not None:
            return win_lst
