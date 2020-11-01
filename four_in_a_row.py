import tkinter as tk
from PIL import ImageTk, Image
from ex12.game import *


class MyApp:
    LEN_COL = 7
    ZERO = 0
    ONE = 1
    HUNDRED = 100
    ADJUST_LOCATION = 0.0015
    PLAYER_1_COLOR = "red"
    PLAYER_2_COLOR = "yellow"
    PLAYER_1 = 1
    PLAYER_2 = 2
    TIE = 0
    PVP = "pvp"
    PVC = "pvc"
    CVP = "cvp"
    CVC = "cvc"

    def __init__(self, root):
        """A constructor for a MyApp object"""
        self.root = root
        self.root.resizable(False, False)
        root.geometry("800x600")
        self.create_main_menu()
        self.game = Game()
        self.board_canvas = None
        self.back_canvas = None
        self.which_player = tk.Label(self.root, font=("Courier", 30))
        self.which_player.pack(side=tk.RIGHT)
        self.game_mode = None

    def create_main_menu(self):
        """A method that builds the main menu- canvas and buttons"""
        # create the background canvas:
        wood_photo = Image.open("ex12/wood2.png").resize((1000, 1000),
                                                    Image.ANTIALIAS)
        wood_photo = ImageTk.PhotoImage(wood_photo)
        back_canvas = tk.Canvas(self.root, width=1000, height=1000)
        back_canvas.pack(expand=tk.YES, fill=tk.BOTH)
        back_canvas.create_image(0, 0, image=wood_photo, anchor="nw")
        back_canvas.photo = wood_photo

        # create the game logo canvas:
        logo_photo = Image.open("ex12/game_logo_bg1.png").resize((500, 200),
                                                            Image.ANTIALIAS)
        logo_photo = ImageTk.PhotoImage(logo_photo)
        logo_canvas = tk.Canvas(self.root, width=500, height=200)
        logo_canvas.place(relx=0.2, rely=0.02)
        logo_canvas.create_image(0, 0, image=logo_photo, anchor="nw")
        logo_canvas.photo = logo_photo

        # call for the function that creates the buttons:
        self.create_main_menu_buttons()

    def create_main_menu_buttons(self):
        """A method that creates the main menu buttons"""
        # player vs player button:
        pvp_photo = Image.open("ex12/pvp.png").resize((140, 130), Image.ANTIALIAS)
        pvp_photo = ImageTk.PhotoImage(pvp_photo)
        pvp_button = tk.Button(self.root, image=pvp_photo, command=self.pvp)
        pvp_button.photo = pvp_photo
        pvp_button.place(relx=0.3, rely=0.40)

        # player vs computer button:
        pvc_photo = Image.open("ex12/pvc.png").resize((140, 130), Image.ANTIALIAS)
        pvc_photo = ImageTk.PhotoImage(pvc_photo)
        pvc_button = tk.Button(self.root, image=pvc_photo,
                               command=self.pvc)
        pvc_button.photo = pvc_photo
        pvc_button.place(relx=0.5, rely=0.40)

        # computer vs player button:
        cvp_photo = Image.open("ex12/cvp.png").resize((140, 130), Image.ANTIALIAS)
        cvp_photo = ImageTk.PhotoImage(cvp_photo)
        cvp_button = tk.Button(self.root, image=cvp_photo,
                               command=self.cvp)
        cvp_button.photo = cvp_photo
        cvp_button.place(relx=0.3, rely=0.65)

        # computer vs computer button:
        cvc_photo = Image.open("ex12/cvc.png").resize((140, 130), Image.ANTIALIAS)
        cvc_photo = ImageTk.PhotoImage(cvc_photo)
        cvc_button = tk.Button(self.root, image=cvc_photo,
                               command=self.cvc)
        cvc_button.photo = cvc_photo
        cvc_button.place(relx=0.5, rely=0.65)

    def create_board_canvas(self):
        """A method that creates the board canvas"""
        empty_board = tk.PhotoImage(file='ex12/wood2.png')
        back_canvas = tk.Canvas(self.root, width=1000, height=1000)
        back_canvas.create_image(0, 0, image=empty_board, anchor=tk.NW)
        back_canvas.photo = empty_board
        board_canvas = tk.Canvas(self.root, width=570, height=500, bg='blue')
        # placing the oval objects by
        for row in range(10, 560, 80):
            for col in range(10, 480, 80):
                board_canvas.create_oval(row, col, row + 70, col + 70,
                                         fill="white")
        board_canvas.place(relx=0.05, rely=0.1)
        back_canvas.place(relx=0, rely=0)
        self.board_canvas = board_canvas
        self.back_canvas = back_canvas

        # create player labels:
        player1_photo = Image.open("ex12/player1.png").resize((100, 50),
                                                         Image.ANTIALIAS)
        player1_photo = ImageTk.PhotoImage(player1_photo)
        player1_canvas = tk.Canvas(self.root, width=100, height=50)
        player1_canvas.place(relx=0.82, rely=0.02)
        player1_canvas.create_image(0, 0, image=player1_photo, anchor="nw")
        player1_canvas.photo = player1_photo

        player2_photo = Image.open("ex12/player2.png").resize((100, 50),
                                                         Image.ANTIALIAS)
        player2_photo = ImageTk.PhotoImage(player2_photo)
        player2_canvas = tk.Canvas(self.root, width=100, height=50)
        player2_canvas.place(relx=0.82, rely=0.12)
        player2_canvas.create_image(0, 0, image=player2_photo, anchor="nw")
        player2_canvas.photo = player2_photo

    def create_arrow_button(self):
        """A method that creates the arrow buttons which operates the game. each
        button will insert a disc to the column it refers to"""
        arrow_photo = Image.open("ex12/arrow.png").resize((40, 40), Image.ANTIALIAS)
        arrow_photo = ImageTk.PhotoImage(arrow_photo)
        adjust_location = self.ZERO
        col_counter = self.ZERO
        for col in range(7, 77, 10):
            col_float = col / self.HUNDRED
            col_loc = col_float + adjust_location
            arrow_button = tk.Button(self.root, image=arrow_photo,
                                     command=self.insert_disc(col_counter))
            arrow_button.photo = arrow_photo
            arrow_button.place(relx=col_loc, rely=0.01)
            adjust_location += self.ADJUST_LOCATION
            col_counter += self.ONE

    def mark_winning_ovals(self, winner_lst):
        """A method that marks the winning four discs using hollow ovals objects"""
        for disc_cor in winner_lst:
            row_win = disc_cor[0]
            col_win = disc_cor[1]
            self.board_canvas.create_oval(10 + col_win * 80, 10 + row_win * 80,
                                          col_win * 80 + 80, row_win * 80 + 80,
                                          outline="white", width="4")

    def check_winner(self):
        """A method that checks if someone has won the game and updates the game
        accordingly"""
        if self.game.get_winner() == self.PLAYER_1:
            winner_lst = self.game.get_wining_discs(self.PLAYER_1)
            self.mark_winning_ovals(winner_lst)
            color = "red"
            self.win_msg(color)
            self.game.reset_board()
            return True
        elif self.game.get_winner() == self.PLAYER_2:
            winner_lst = self.game.get_wining_discs(self.PLAYER_2)
            self.mark_winning_ovals(winner_lst)
            color = "yellow"
            self.win_msg(color)
            self.game.reset_board()
            return True
        elif self.game.get_winner() == self.TIE:
            color = "cyan2"
            self.win_msg(color)
            self.game.reset_board()
            return True

    def press_pvp(self, col):
        """A method that operates the insert of the discs in the player
        vs player version of the game"""
        player = self.game.get_current_player()
        # self.which_player.configure(text=player)
        row = self.game.get_row_for_disc(col)
        # creating the oval objects that plays the rule of a disc
        if row is not False:
            self.game.make_move(col)
            if player == self.game.PLAYER1:
                self.create_yellow_polygon()
                self.board_canvas.create_oval(10 + col * 80, 10 + row * 80,
                                              col * 80 + 80, row * 80 + 80,
                                              fill="red")
            else:
                self.board_canvas.create_oval(10 + col * 80, 10 + row * 80,
                                              col * 80 + 80, row * 80 + 80,
                                              fill="yellow")
                self.create_red_polygon()
                # check if a player won, if yes, add a winning message and mark
                # winning discs
            self.check_winner()

    def press_pvc(self, col):
        """A method that operates the insert of the discs in the player
        vs computer version of the game"""
        # self.which_player.configure(text=player)
        row = self.game.get_row_for_disc(col)
        # creating the oval objects that plays the rule of a disc
        if row is not False:

            row_ai, col_ai = self.game.make_move_pvc(col)
            self.create_red_polygon()
            self.create_yellow_polygon()
            self.board_canvas.create_oval(10 + col * 80, 10 + row * 80,
                                          col * 80 + 80, row * 80 + 80,
                                          fill="red")
            self.root.after(500, self.create_oval_yellow_ai(row_ai, col_ai))
        self.check_winner()

    def press_cvp(self, col):
        """A method that operates the insert of the discs in the computer
        vs player version of the game"""
        # self.which_player.configure(text=player)
        row = self.game.get_row_for_disc(col)
        # creating the oval objects that plays the rule of a disc
        if row is not False:
            row_ai, col_ai = self.game.make_move_cvp(col)

            self.board_canvas.create_oval(10 + col * 80, 10 + row * 80,
                                          col * 80 + 80, row * 80 + 80,
                                          fill="yellow")
            self.create_red_polygon()

            self.root.after(500, self.create_oval_red_ai(row_ai, col_ai))
        self.check_winner()

    def create_red_polygon(self):
        """A method that creates a red polygon object which marks that it's the first
        player's turn to play"""

        def create_red_polygon_helper():
            self.back_canvas.create_polygon(
                [762, 70, 762, 128, 655, 128, 655, 70],
                outline="gray90", width="4")
            self.back_canvas.create_polygon(
                [762, 10, 762, 68, 655, 68, 655, 10],
                outline="red", width="4")

        return create_red_polygon_helper()

    def create_yellow_polygon(self):
        """A method that creates a yellow polygon object which marks that its the
        second player's turn to play"""

        def create_yellow_polygon_helper():
            self.back_canvas.create_polygon(
                [762, 10, 762, 68, 655, 68, 655, 10],
                outline="gray90", width="4")
            self.back_canvas.create_polygon(
                [762, 70, 762, 128, 655, 128, 655, 70],
                outline="yellow", width="4")

        return create_yellow_polygon_helper()

    def create_oval_yellow_ai(self, row_ai, col_ai):
        """A method that creates a yellow oval object which represents the computers
        disc"""

        def create_helper():
            if self.game.get_winner() is None:
                self.board_canvas.create_oval(10 + col_ai * 80, 10 + row_ai * 80,
                                              col_ai * 80 + 80, row_ai * 80 + 80,
                                              fill="yellow")
            self.create_red_polygon()

        return create_helper

    def create_oval_red_ai(self, row_ai, col_ai):
        """A method that creates a red oval object which represents the computers
        disc"""

        def create_helper():
            if self.game.get_winner() is None:
                self.board_canvas.create_oval(10 + col_ai * 80, 10 + row_ai * 80,
                                              col_ai * 80 + 80, row_ai * 80 + 80,
                                              fill="red")
                self.create_yellow_polygon()

        return create_helper

    def insert_disc(self, col):
        """A method that operates the press methods which operates the game itself"""
        if self.game_mode == self.PVP:
            def press():
                self.press_pvp(col)
        elif self.game_mode == self.PVC:
            def press():
                self.press_pvc(col)
        elif self.game_mode == self.CVP:
            def press():
                self.press_cvp(col)
        return press

    def play_again_button(self):
        """A method that operates the 'play again' button that appears whenever the
        game has ended"""
        if self.game_mode == self.PVP:
            play_again_button = tk.Button(self.root, text="Play Again",
                                          font=("Courier", 14),
                                          command=self.pvp)
        elif self.game_mode == self.PVC:
            play_again_button = tk.Button(self.root, text="Play Again",
                                          font=("Courier", 14),
                                          command=self.pvc)
        elif self.game_mode == self.CVP:
            play_again_button = tk.Button(self.root, text="Play Again",
                                          font=("Courier", 14),
                                          command=self.cvp)
        else:
            play_again_button = tk.Button(self.root, text="Play Again",
                                          font=("Courier", 14),
                                          command=self.cvc)
        play_again_button.place(relx=0.37, rely=0.1)

    def win_msg(self, color):
        """A method that creates the win message canvas"""
        win_p_1_canvas = tk.Canvas(self.root, width=1000, height=100, bg=color)
        win_p_1_canvas.place(relx=0, rely=0.00)
        if self.game.get_winner() == self.TIE:
            label = tk.Label(self.root, text="IT'S A TIE!", font=("Courier", 30),
                             bg=color)
        else:
            label = tk.Label(self.root, text="YOU WIN!", font=("Courier", 30),
                             bg=color)
        label.place(relx=0.38, rely=0.01)
        # play again button:
        self.play_again_button()
        # exit
        exit_button = tk.Button(self.root, text="Exit",
                                font=("Courier", 14),
                                command=self.root.destroy)
        exit_button.place(relx=0.55, rely=0.1)

    def pvp(self):
        """A method that operates the player vs player version of the game"""
        self.game_mode = self.PVP
        self.create_board_canvas()
        self.create_red_polygon()
        self.create_arrow_button()
        self.game.reset_winner()
        self.game.reset_players()

    def pvc(self):
        """A method that operates the player vs computer version of the game"""
        self.game_mode = self.PVC
        self.create_board_canvas()
        self.create_red_polygon()
        self.create_arrow_button()
        self.game.reset_winner()
        self.game.reset_players()

    def cvp(self):
        """A method that operates the computer vs player version of the game"""
        self.game_mode = self.CVP
        self.create_board_canvas()
        self.create_yellow_polygon()
        self.game.reset_players()
        self.game.reset_winner()
        row_ai, col_ai = self.game.make_move_cvp()
        self.board_canvas.create_oval(10 + col_ai * 80, 10 + row_ai * 80,
                                      col_ai * 80 + 80, row_ai * 80 + 80,
                                      fill="red")
        self.create_arrow_button()
        self.game.reset_winner()

    def cvc(self):
        """A method that operates the computer vs computer version of the game"""
        self.game_mode = self.CVC
        self.create_board_canvas()
        self.game.reset_winner()
        self.game.reset_players()

        def play_cvc():
            """
            This function will insert the discs for both ai
            """
            if not self.check_winner():
                col_ai, row_ai = self.game.make_move_cvc()
                if self.game.player_turn == self.PLAYER_1:
                    self.board_canvas.create_oval(10 + col_ai * 80,
                                                  10 + row_ai * 80,
                                                  col_ai * 80 + 80,
                                                  row_ai * 80 + 80,
                                                  fill="yellow")
                    self.create_yellow_polygon()

                    self.root.after(500, play_cvc)
                    self.root.update()
                elif self.game.player_turn == self.PLAYER_2:
                    self.board_canvas.create_oval(10 + col_ai * 80,
                                                  10 + row_ai * 80,
                                                  col_ai * 80 + 80,
                                                  row_ai * 80 + 80,
                                                  fill="red")
                    self.create_red_polygon()
                    self.root.after(500, play_cvc)
                    self.root.update()

        return play_cvc()


if __name__ == '__main__':
    root = tk.Tk()
    MyApp(root)
    root.mainloop()
