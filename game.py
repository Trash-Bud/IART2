
from cmath import pi
import random

import numpy as np
from board import Board
from chess_piece import ChessPiece
from constants import PIECES_DIC
from human_mode import HumanMode
from position import Position
from environment import SnakeChessEnv

class Game:

    def __init__(self):
        print("Choose Game Mode!")
        print("You chose easy mode!")
        self.easy_mode()
        

    def easy_mode(self):
        try:
            board = Board(5,2)
            snake = [
                Position(0,4),
                Position(0,3),
                Position(0,2),
                Position(1,2),
                Position(2,2),
                Position(2,3),
                Position(3,3),
                Position(4,3),
                Position(4,2),
                Position(4,1),
                Position(4,0)
                ]

            board.add_snake(snake)
            chess_pieces = ["k1","B1"]

        except Exception as e:
            print(str(e))

        self.play_q_learning(board,chess_pieces)

    def human_mode(self, board, chess_pieces):
        human_game = HumanMode(board, chess_pieces)
        human_game.render()
        while not human_game.board.end():
            human_game.play()
        human_game.render()
            

    def play_q_learning(self, board, chess_pieces):
        env = SnakeChessEnv(board, chess_pieces)
        q_table = np.zeros([env.observation_space_length,env.action_space_length])
        alpha = 0.1
        gama = 0.6
        epsilon = 0.1

        epochs, penalties = 0,0

        episode = 1000
        for episode in range(1, episode + 1):
            state = env.reset()
            print("Episode:{}".format(episode))
            done = False
       
            while not done:
                if random.uniform(0,1) < epsilon:
                    num = random.randint(0, env.board.playable_squares_num() - 1)
                    action_b = env.board.playable_squares()[num]
                    action = env.get_action(action_b)
                else:
                    num = np.argmax(q_table[state])
                    action_b = env.board.playable_squares()[num]
                    action = env.get_action(action_b)

                next_state, reward, done, info = env.step(action)
                old_value = q_table[state, action]
                next_max = np.max(q_table[next_state])

                new_value = (1-alpha)*old_value + alpha*(reward + gama *next_max)
                q_table[state,action] = new_value
                
                if reward < 0:
                    penalties += 1
                state = next_state
                epochs += 1
            
        
        state = env.reset()
        done = False
        
        while not done:
            env.render()
            action = np.argmax(q_table[state])
            state,reward,done,info = env.step(action)
        env.render()
            

        
    

        



