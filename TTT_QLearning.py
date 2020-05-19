import Board
import Player
import numpy as np
import tkinter as tk
import copy
import pickle as pickle
import matplotlib.pyplot as plt


class HumanPlayer_chance(Player.Player):
    pass


class ComputerPlayer_chance(Player.Player):
    pass


class RandomPlayer(ComputerPlayer_chance):
    @staticmethod
    def next_move(board):
        moves = board.moves_available()
        if moves:
            return moves[np.random.choice(len(moves))]    # Apply random selection to the index


class T_HandPlayer(ComputerPlayer_chance):
    def __init__(self, mark):
        super(T_HandPlayer, self).__init__(mark=mark)

    def next_move(self, board):
        moves = board.moves_available()
        if moves:
            for move in moves:
                if T_HandPlayer.next_move_winner(board, move, self.mark):
                    return move
                elif T_HandPlayer.next_move_winner(board, move, self.opponent_mark):
                    return move
            else:
                return RandomPlayer.next_move(board)

    @staticmethod
    def next_move_winner(board, move, mark):
        return board.refresh_board(move, mark).winner_selected() == mark


class QPlayer(ComputerPlayer_chance):
    def __init__(self, mark, Q={}, epsilon=0.2):
        super(QPlayer, self).__init__(mark=mark)
        self.QValue = Q
        self.epsilon = epsilon

    #epsilon-greedy exploration
    def next_move(self, board):
        if np.random.uniform() < self.epsilon:
            return RandomPlayer.next_move(board)
        else:
            state_key = QPlayer.board_player_turn(board, self.mark, self.QValue)
            Qs = self.QValue[state_key]
            if self.mark == "X":
                return QPlayer.argminmax(Qs, max)
            elif self.mark == "O":
                return QPlayer.argminmax(Qs, min)

    @staticmethod
    def board_player_turn(board, mark, Q):     # Make a dictionary key for the current state (board + player turn) and if Q does not yet have it, add it to Q
        default_Qvalue = 1.0       # Encourages exploration
        state_key = board.str_to_represent_state(mark)
        if Q.get(state_key) is None:
            moves = board.moves_available()
            Q[state_key] = {move: default_Qvalue for move in moves}    # The available moves in each state are initially given a default value of zero
        return state_key

    @staticmethod
    def argminmax(Qs, min_or_max):       # Determines either the argmin or argmax of the array Qs such that if there are 'ties', one is chosen at random
        min_or_maxQ = min_or_max(list(Qs.values()))
        if list(Qs.values()).count(min_or_maxQ) > 1:      # If there is more than one move corresponding to the maximum Q-value, choose one at random
            best_options = [move for move in list(Qs.keys()) if Qs[move] == min_or_maxQ]
            move = best_options[np.random.choice(len(best_options))]
        else:
            move = min_or_max(Qs, key=Qs.get)
        return move

class Game:
    def __init__(self, master, player1, player2, learnQ=None, Q={}, alpha=0.3, gamma=0.9):
        frame = tk.Frame()
        frame.grid()
        self.master = master
        master.title("Tic-Tac-Toe")
        self.reward_X = 0
        self.reward_O = 0
        self.rew_X = []
        self.rew_O = []
        self.player1 = player1
        self.player2 = player2
        self.curr_player = player1
        self.other_player = player2
        self.empty_movetext = ""
        self.TTT_board = Board.Board()
        self.board_buttons = [[None for _ in range(3)] for _ in range(3)]
        self.learnQ = learnQ
        for i in range(3):
            for j in range(3):
                self.board_buttons[i][j] = tk.Button(frame, height=3, width=3, text=self.empty_movetext, command=lambda i=i, j=j: self.calling_actions(self.board_buttons[i][j]))
                self.board_buttons[i][j].grid(row=i, column=j)
        if self.learnQ:
            self.QValue = Q
            self.alpha = alpha          # Learning rate
            self.gamma = gamma          # Discount rate
        self.reset_button = tk.Button(text="Reset", command=self.reset)
        self.reset_button.grid(row=3)
        self.win_draw = []

    @property
    def learnQ(self):
        if self._learnQ is not None:
            return self._learnQ
        if isinstance(self.player1, QPlayer) or isinstance(self.player2, QPlayer):
            return True

    @learnQ.setter
    def learnQ(self, _learnQ):
        self._learnQ = _learnQ

    def calling_actions(self, button):
        if self.TTT_board.gameover():
            pass
        else:
            if isinstance(self.curr_player, HumanPlayer_chance) and isinstance(self.other_player, HumanPlayer_chance):
                if self.empty_move(button):
                    move = self.next_move(button)
                    self.handle_move(move)
            elif isinstance(self.curr_player, HumanPlayer_chance) and isinstance(self.other_player, ComputerPlayer_chance):
                computer_player = self.other_player
                if self.empty_move(button):
                    human_move = self.next_move(button)
                    self.handle_move(human_move)
                    if not self.TTT_board.gameover() and self.chance != 0.1:
                        computer_move = computer_player.next_move(self.TTT_board)
                        self.handle_move(computer_move)
            elif isinstance(self.curr_player, ComputerPlayer_chance):
                computer_player = self.curr_player
                if not self.TTT_board.gameover():
                    computer_move = computer_player.next_move(self.TTT_board)
                    self.handle_move(computer_move)

    def empty_move(self, button):
        return button["text"] == self.empty_movetext

    def next_move(self, button):
        info = button.grid_info()
        move = (int(info["row"]), int(info["column"]))
        return move

    def handle_move(self, move):
        if self.learnQ:
            self.learn_Q(move)
        # Get row and column number of the corresponding button
        i, j = move
        # Change the label on the button to the current player's mark
        self.board_buttons[i][j].configure(text=self.curr_player.mark)
        # Update the board
        self.TTT_board.place_mark(move, self.curr_player.mark)
        if self.TTT_board.gameover():
            self.result()
        else:
            self.next_players_turn()

    def result(self):
        if self.TTT_board.winner_selected() is None:
            print("Cat's game(DRAW).")
        else:
            print(("The game is over. The player with mark {mark} won!".format(mark=self.curr_player.mark)))

    def reset(self):
        print("Resetting...")
        for i in range(3):
            for j in range(3):
                self.board_buttons[i][j].configure(text=self.empty_movetext)
        self.TTT_board = Board.Board(TTT_board=np.ones((3,3))*np.nan)
        self.curr_player = self.player1
        self.other_player = self.player2
        self.play_chance()

    def next_players_turn(self):
        #10% chance ,player skips his chance
        self.chance = round(np.random.random_sample(), 1)
        if self.chance != 0.1:
            if self.curr_player == self.player1:
                self.curr_player = self.player2
                self.other_player = self.player1
            else:
                self.curr_player = self.player1
                self.other_player = self.player2
        else:
            print("Current Player chance skipped...")
            if self.curr_player == self.player1:
                self.curr_player = self.player1
                self.other_player = self.player2
            else:
                self.curr_player = self.player2
                self.other_player = self.player1

    def play_chance(self):
        if isinstance(self.player1, HumanPlayer_chance) and isinstance(self.player2, HumanPlayer_chance):
            pass        # For human vs. human, play relies on the calling_actions from button presses
        elif isinstance(self.player1, HumanPlayer_chance) and isinstance(self.player2, ComputerPlayer_chance):
            pass
        elif isinstance(self.player1, ComputerPlayer_chance) and isinstance(self.player2, HumanPlayer_chance):
            first_computer_move = player1.next_move(self.TTT_board)
            self.handle_move(first_computer_move)
        elif isinstance(self.player1, ComputerPlayer_chance) and isinstance(self.player2, ComputerPlayer_chance):
            while not self.TTT_board.gameover():
                self.play_turn()

    def play_turn(self):
        move = self.curr_player.next_move(self.TTT_board)
        self.handle_move(move)

    # If Q-learning is toggled on, "learn_Q" should be called after receiving a move
    # from an instance of Player and before implementing the move (using Board's "place_mark" staticmethod)
    def learn_Q(self, move):
        state_key = QPlayer.board_player_turn(self.TTT_board, self.curr_player.mark, self.QValue)
        next_board = self.TTT_board.refresh_board(move, self.curr_player.mark)
        reward = next_board.reward_earned()
        if self.curr_player.mark == 'X':
            self.reward_X=reward + self.reward_X
            self.rew_X.append(reward)
        else:
            self.reward_O=reward + self.reward_O
            self.rew_O.append(reward)
        next_state_key = QPlayer.board_player_turn(next_board, self.other_player.mark, self.QValue)
        if next_board.gameover():
            expected = reward
        else:
            next_Qs = self.QValue[next_state_key]
            if self.curr_player.mark == "X":
                # current player is X, the next player is O, move with the minimum Q value should be chosen
                expected = reward + (self.gamma * min(next_Qs.values()))
            elif self.curr_player.mark == "O":
                # Current player is O, the next player is X, move with the maximum Q vlue should be chosen
                expected = reward + (self.gamma * max(next_Qs.values()))
        change = self.alpha * (expected - self.QValue[state_key][move])
        self.QValue[state_key][move] += change



