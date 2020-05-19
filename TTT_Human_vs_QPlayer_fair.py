import copy
import pickle as pickle
from TTT_QLearning_fair import Game,HumanPlayer_chance, QPlayer
import numpy as np
import tkinter as tk
import graphplt


def main():
    policy = pickle.load(open("policy.p", "rb"))
    root_window = tk.Tk()
    player1 = HumanPlayer_chance(mark="X")
    player2 = QPlayer(mark="O", epsilon=0)
    game = Game(root_window, player1, player2, Q=policy)
    game.play_chance()
    root_window.mainloop()
    reward_X = game.rew_X
    reward_O = game.rew_O
    graphplt.graphplt(reward_X,reward_O, "Human_vs_QPlayer_fair","Episodes","Reward")


if __name__ == '__main__':
    main()