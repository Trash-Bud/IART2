import random
import time
import numpy as np
from board import Board
from constants import ALPHA, EPISODES, EPSILON, GAMA, SHOW_EVERY, WHITE, USE_PYGAME
from human_mode import HumanMode
from position import Position
from environment import SnakeChessEnv
import matplotlib.pyplot as plt
import pygame

from pygame_utils import close_pygame, pygame_render


class Game:

    def __init__(self):
        self.choose_difficulty()

    def choose_game_mode(self, board, chess_pieces):
        while True:
            print("\nChoose Game Mode!")

            inp = input("A - player   B - Q-learning  C - SARSA: ")

            if (str(inp) == 'B'):
                self.play_q_learning(board, chess_pieces)
                break
            elif (str(inp) == 'C'):
                self.sarsa_algorithm(board, chess_pieces)
                break
            elif (str(inp) == 'A'):
                self.human_mode(board, chess_pieces)
                break
            else:
                print("Choose a valid option")

    def choose_difficulty(self):
        while True:
            print("\nChoose a game")

            inp = input("1, 2 or 3: ")

            if (str(inp) == '1'):
                self.game_1()
                break
            elif (str(inp) == '2'):
                self.game_2()
                break
            elif (str(inp) == '3'):
                self.game_3()
                break
            else:
                print("Choose a valid option")

    def game_3(self):
        try:
            board = Board(5, 2)
            snake = [
                Position(0, 4),
                Position(0, 3),
                Position(1, 3),
                Position(1, 2),
                Position(1, 1),
                Position(2, 1),
                Position(3, 1),
                Position(4, 1),
                Position(4, 0)
            ]

            board.add_snake(snake)
            chess_pieces = ["K1", "Q1"]

        except Exception as e:
            print(str(e))
        board.draw_board()
        self.choose_game_mode(board, chess_pieces)

    def game_2(self):
        try:
            board = Board(5, 2)
            snake = [
                Position(0, 4),
                Position(0, 3),
                Position(0, 2),
                Position(0, 1),
                Position(0, 0),
                Position(1, 0),
                Position(2, 0),
                Position(2, 1),
                Position(2, 2),
                Position(3, 2),
                Position(4, 2),
                Position(4, 1),
                Position(4, 0)
            ]

            board.add_snake(snake)
            chess_pieces = ["R1", "K1"]

        except Exception as e:
            print(str(e))
        board.draw_board()
        self.choose_game_mode(board, chess_pieces)

    def game_1(self):
        try:
            board = Board(5, 2)
            snake = [
                Position(0, 4),
                Position(0, 3),
                Position(0, 2),
                Position(1, 2),
                Position(2, 2),
                Position(2, 3),
                Position(3, 3),
                Position(4, 3),
                Position(4, 2),
                Position(4, 1),
                Position(4, 0)
            ]

            board.add_snake(snake)
            chess_pieces = ["K1", "Q1"]

        except Exception as e:
            print(str(e))
        board.draw_board()
        self.choose_game_mode(board, chess_pieces)

    def human_mode(self, board, chess_pieces):
        human_game = HumanMode(board, chess_pieces)
        human_game.render()
        while not human_game.board.end():
            human_game.play()
        human_game.render()

    def play_q_learning(self, board, chess_pieces):
        # initializing the environment
        env = SnakeChessEnv(board, chess_pieces)

        # creating q_table full of zeroes
        q_table = np.zeros(
            [env.observation_space_length, env.action_space_length])

        # list to keep episode rewards
        ep_rewards = []
        # dictionary for average max and min rewards
        ag_ep_rewards = {'ep': [], 'avg': [], 'min': [], 'max': []}

        # amount of games lost
        lost = 0

        for episode in range(1, EPISODES + 1):
            episode_reward = 0
            # env reset so we start fresh each episode
            state = env.reset()

            if USE_PYGAME:
                pygame_render(env)

            #print("Episode:{} -> ".format(episode), end = "")
            done = False

            while not done:

                if random.uniform(0, 1) < EPSILON:  # if choice is random
                    # choosing an existing valid position for our chess piece
                    num = random.randint(
                        0, env.board.playable_squares_num() - 1)
                    action_b = env.board.playable_squares()[num]
                    # seeing what number in our environment corresponds to this action
                    action = env.get_action(action_b)
                else:  # if choice is not random
                    # choosing greedily the next action
                    action = np.argmax(q_table[state])

                # applying the action to the environment
                next_state, reward, done, info = env.step(action)
                #
                episode_reward += reward
                # getting the old value of the action on the old state
                old_value = q_table[state, action]
                # getting the old value of the best action of our new state
                next_max = np.max(q_table[next_state])

                # calculating the new value with q-learning
                new_value = (1-ALPHA) * old_value + ALPHA * \
                    (reward + GAMA * next_max)

                # saving the new value for this state and action
                q_table[state, action] = new_value

                # if the reward is less than zero then we lost the game
                if reward < 0:
                    lost += 1

                # setting the state for our next iteration
                state = next_state

                # appending episode reward
                ep_rewards.append(episode_reward)
                # SHOW_EVERY episodes we save data
                if not episode % SHOW_EVERY:
                    # get average
                    average_reward = sum(
                        ep_rewards[-SHOW_EVERY:])/len(ep_rewards[-SHOW_EVERY:])
                    # get min
                    min_v = min(ep_rewards[-SHOW_EVERY:])
                    # get max
                    max_v = max(ep_rewards[-SHOW_EVERY:])
                    # adding dictionary
                    ag_ep_rewards['ep'].append(episode)
                    ag_ep_rewards['avg'].append(average_reward)
                    ag_ep_rewards['min'].append(min_v)
                    ag_ep_rewards['max'].append(max_v)

                if USE_PYGAME:
                    pygame_render(env)
                    close_pygame()

        print("lost ", end="")
        print(lost, end="")
        print(" times in ", end="")
        print(EPISODES, end="")
        print(" tries")

        # resetting the state of the environment
        state = env.reset()
        done = False

        # for the last iteration we always get the best state
        while not done:
            env.render()
            action = np.argmax(q_table[state])
            state, reward, done, info = env.step(action)
        env.render()

        plt.plot(ag_ep_rewards['ep'], ag_ep_rewards['avg'], label="avg")
        plt.plot(ag_ep_rewards['ep'], ag_ep_rewards['min'], label="min")
        plt.plot(ag_ep_rewards['ep'], ag_ep_rewards['max'], label="max")
        plt.legend(loc=4)
        plt.show()

    def sarsa_algorithm(self, board, chess_pieces):
        # initializing the environment
        env = SnakeChessEnv(board, chess_pieces)

        # creating q_table full of zeroes
        q_table = np.zeros(
            [env.observation_space_length, env.action_space_length])

        # list to keep episode rewards
        ep_rewards = []
        # dictionary for average max and min rewards
        ag_ep_rewards = {'ep': [], 'avg': [], 'min': [], 'max': []}

        # amount of games lost
        lost = 0
        for episode in range(1, EPISODES + 1):
            episode_reward = 0
            # env reset so we start fresh each episode
            state = env.reset()
            if USE_PYGAME:
                pygame_render(env)
            #print("Episode:{} -> ".format(episode), end = "")
            done = False

            # calculating the first action before the episode really starts
            if random.uniform(0, 1) < EPSILON:
                num = random.randint(0, env.board.playable_squares_num() - 1)
                action_b = env.board.playable_squares()[num]
                action = env.get_action(action_b)
            else:
                action = np.argmax(q_table[state])

            while not done:
                # applying the action to the environment
                next_state, reward, done, info = env.step(action)
                # getting the old value of the action on the old state

                # choosing next action
                if random.uniform(0, 1) < EPSILON:
                    num = random.randint(
                        0, env.board.playable_squares_num() - 1)
                    action_b = env.board.playable_squares()[num]
                    next_action = env.get_action(action_b)
                else:
                    next_action = np.argmax(q_table[next_state])

                # getting the value of our old state
                old_value = q_table[state, action]
                # getting the value of the next state with the next action calculated
                next_max = q_table[next_state, next_action]

                # calculating the new value with SARSA
                new_value = old_value + ALPHA * \
                    ((reward + GAMA * next_max) - old_value)

                # saving the new value for this state and action
                q_table[state, action] = new_value

                # if the reward is less than zero then we lost the game
                if reward < 0:
                    lost += 1

                episode_reward += reward

                # setting the state for our next iteration
                state = next_state
                # setting the action for our next iteration
                action = next_action

                # appending episode reward
                ep_rewards.append(episode_reward)
                # SHOW_EVERY episodes we save data
                if not episode % SHOW_EVERY:
                    # get average
                    average_reward = sum(
                        ep_rewards[-SHOW_EVERY:])/len(ep_rewards[-SHOW_EVERY:])
                    # get min
                    min_v = min(ep_rewards[-SHOW_EVERY:])
                    # get max
                    max_v = max(ep_rewards[-SHOW_EVERY:])
                    # adding dictionary
                    ag_ep_rewards['ep'].append(episode)
                    ag_ep_rewards['avg'].append(average_reward)
                    ag_ep_rewards['min'].append(min_v)
                    ag_ep_rewards['max'].append(max_v)
                    #print("Episode: {} Average: {} Min: {} Max: {}".format(episode,average_reward,min_v,max_v))

                if USE_PYGAME:
                    pygame_render(env)
                    close_pygame()

        print("lost ", end="")
        print(lost, end="")
        print(" times in ", end="")
        print(EPISODES, end="")
        print(" tries")

        # resetting the state of the environment
        state = env.reset()
        done = False

        # for the last iteration we always get the best state
        while not done:
            env.render()
            action = np.argmax(q_table[state])
            state, reward, done, info = env.step(action)
        env.render()

        plt.plot(ag_ep_rewards['ep'], ag_ep_rewards['avg'], label="avg")
        plt.plot(ag_ep_rewards['ep'], ag_ep_rewards['min'], label="min")
        plt.plot(ag_ep_rewards['ep'], ag_ep_rewards['max'], label="max")
        plt.legend(loc=4)
        plt.show()
