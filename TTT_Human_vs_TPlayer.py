import copy
import pickle as pickle
from TTT_QLearning import Game,HumanPlayer_chance,T_HandPlayer
import numpy as np
import tkinter as tk
import graphplt


def main():
    policy = pickle.load(open("policy.p", "rb"))
    root_window = tk.Tk()
    player1 = HumanPlayer_chance(mark="X")
    player2 = T_HandPlayer(mark="O")
    game = Game(root_window, player1, player2, Q=policy)
    game.play_chance()
    root_window.mainloop()


if __name__ == '__main__':
    main()
