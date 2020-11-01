import random


class AI:
    LAST_ROW = 0
    LEN_COL = 7

    def __init__(self, game, player):
        """A constructor for an AI object"""
        self.game = game
        self.player = player

    def is_board_full(self):
        """
        This method will check if the board is full. return True if full, else return
        False
        """
        counter = self.LEN_COL
        for col in range(self.game.LEN_COL - 1):
            if self.game.get_board()[self.LAST_ROW][col] == self.game.EMPTY_CELL:
                counter -= 1
                break
        # if every last col is full, then the board is full
        if counter == self.LEN_COL:
            return True
        return False

    def find_legal_move(self, timeout=None):
        """
        This method find a legal move for the ai player and return a legal col(int)
        """
        if self.game.get_current_player() != self.player:
            raise Exception("Wrong player")
        if self.is_board_full():
            raise Exception("No possible AI moves")
        while True:
            col = random.randint(0, 6)
            if self.game.get_player_at(self.LAST_ROW,col) is None:
                return col

    def get_last_found_move(self):
        pass
