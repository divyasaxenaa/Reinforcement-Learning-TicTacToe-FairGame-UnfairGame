import copy
import pickle as pickle
import numpy as np
import tkinter as tk


class Board:
    def __init__(self, TTT_board=np.ones((3,3))*np.nan):
        self.TTT_board = TTT_board

    def winner_selected(self):
        rows = [self.TTT_board[i,:] for i in range(3)]
        columns = [self.TTT_board[:,j] for j in range(3)]
        diag = [np.array([self.TTT_board[i,i] for i in range(3)])]
        cross_diagonal = [np.array([self.TTT_board[2-i,i] for i in range(3)])]
        # A "lane" is defined as a row, column, diagonal, or cross-diagonal
        lanes = np.concatenate((rows, columns, diag, cross_diagonal))
        # Returns true if any lane is equal to the input argument "x"
        any_lane = lambda x: any([np.array_equal(lane, x) for lane in lanes])
        if any_lane(np.ones(3)):
            return "X"
        elif any_lane(np.zeros(3)):
            return "O"

    def gameover(self):
        return (not np.any(np.isnan(self.TTT_board))) or (self.winner_selected() is not None)

    # Place a mark on the board
    def place_mark(self, move, mark):
        num = Board.mark_no(mark)
        self.TTT_board[tuple(move)] = num

    @staticmethod
    def mark_no(mark):
        d = {"X": 1, "O": 0}
        return d[mark]

    def moves_available(self):
        return [(i,j) for i in range(3) for j in range(3) if np.isnan(self.TTT_board[i][j])]

    def refresh_board(self, move, mark):
        next_board = copy.deepcopy(self)
        next_board.place_mark(move, mark)
        return next_board

    # For Q-learning, returns a 10-character string representing the state of the board and the player whose turn it is
    def str_to_represent_state(self, mark):
        fill_value = 9
        filled_TTT_board = copy.deepcopy(self.TTT_board)
        np.place(filled_TTT_board, np.isnan(filled_TTT_board), fill_value)
        return "".join(map(str, (list(map(int, filled_TTT_board.flatten()))))) + mark

    def reward_earned(self):
        if self.gameover():
            if self.winner_selected() is not None:
                if self.winner_selected() == "X":
                    return 1.0
                elif self.winner_selected() == "O":
                    return -1.0
            else:
                return 0.5
        else:
            return 0.0
