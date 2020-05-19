import copy
import pickle
from TTT_QLearning import Game, QPlayer
import numpy as np
import tkinter as tk
import graphplt


def main():
    root_window = tk.Tk()
    epsilon = 0.9
    player1 = QPlayer(mark="X",epsilon = epsilon)
    player2 = QPlayer(mark="O",epsilon = epsilon)
    game = Game(root_window, player1, player2)
    N_episodes = 20000
    reward_XX = []
    reward_OO = []
    for episodes in range(N_episodes):
        episodes = episodes +1
        game.play_chance()
        game.reset()
        reward_XX.append(game.reward_X/episodes)
        reward_OO.append(game.reward_O/episodes)
    policy = game.QValue
    filename = "policy.p".format(N_episodes)
    pickle.dump(policy, open(filename, "wb"))
    graphplt.graphplt(reward_XX, reward_OO, "QTraining","Episodes","Average Reward")


if __name__ == '__main__':
    main()
