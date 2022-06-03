from board import Board
from chess_piece import ChessPiece
from constants import PIECES_DIC
from gym import Env
from gym.spaces import MultiDiscrete
import numpy as np
import random

from position import Position

class SnakeChessEnv(Env):
  
    def __init__(self, board: Board, chess_pieces : list)-> None:
        # game board
        self.board = board
        # chess pieces to be played
        self.chess_pieces = chess_pieces
        # index of the piece that will be played next
        self.piece_num = 0
        # coordinates of all the pieces at the current moment
        # [-1,-1] means the piece has not been placed on the board yet
        self.state = [[-1,-1],[-1,-1]] # !!! only works for 2 chess pieces !!!
        # creates an array of all possible states
        self.generate_states_array() # !!! only works for 2 chess pieces !!!
        # creates an array of all possible actions
        self.actions_array = board.playable_squares()
        # length of the action space
        self.action_space_length = board.playable_squares_num()
        # length of the observation space
        self.observation_space_length = len(self.states_array) # !!! only works for 2 chess pieces !!!

    # creates the states' array
    def generate_states_array(self):
        self.states_array = []

        # appending initial state
        self.states_array.append([[-1,-1],[-1,-1]])

        playable_squares = self.board.playable_squares()
        for i in range(0,self.board.size):
            for e in range(0,self.board.size):
                if ([i,e] in playable_squares):

                    # appending all states where the first chess piece has been placed but the second one has not 
                    self.states_array.append([[i,e],[-1,-1]])

                for f in range(0,self.board.size):
                    for g in range(0,self.board.size):
                        if ([i,e] in playable_squares) and ([f,g] in playable_squares) and ([i,e] != [f,g]) :

                            # appending all states where both pieces have been placed in a valid way
                            self.states_array.append([[i,e],[f,g]])

    # get the index of a specific state (for the q_table) 
    def get_state(self, array):
        return self.states_array.index(array)

    # get a specific state from an index
    def get_state_from_index(self, index):
        return self.states_array[index]

    # get the index of a specific action (for the q_table) 
    def get_action(self, array):
        return self.actions_array.index(array)

    # get a specific action from an index
    def get_action_from_index(self, index):
        return self.actions_array[index]

    # update environment with an action
    def step(self, action):
        # get position chosen in action
        pos = self.actions_array[action]
        # create chess piece
        chess_piece = ChessPiece(Position(pos[0],pos[1]),PIECES_DIC[self.chess_pieces[0][0]],self.chess_pieces[0])
        # remove chess piece from chess pieces still not played 
        self.chess_pieces.remove(self.chess_pieces[0])
        # add chess piece to the board
        self.board.add_piece(chess_piece)
        # updating state
        self.state[self.piece_num] = pos

        # initializing reward
        reward = 0
        if self.board.end():
            # if the game is won the reward is 10
            done = True
            reward = 10
        else:
            if(len(self.board.chess_pieces) == self.board.piece_num):
                # if the game is won the reward is -10
                done = True
                reward = -10
            else:
                # if the game is not over we continue
                done = False

        # dummy because of the gym package needing it      
        info = {}
        # index for the next piece in the env state
        self.piece_num += 1

        return self.get_state(self.state), reward, done, info
        # ^ note: the state return needs to be the int and not the array

    # function for rendering the board
    def render(self):
        self.board.draw_board()
    
    # function for resetting the board so that it can be use again
    def reset(self):
        # re-adding the chess pieces to the array
        for i in range(0,len(self.board.chess_pieces)):
            self.chess_pieces.append(self.board.chess_pieces[i].representation)~
        # clearing the board
        self.board.clear()
        # resetting the index of the next chess piece to be played
        self.piece_num = 0
        # resetting state to initial state
        self.state = [[-1,-1],[-1,-1]] # !!! only works for 2 chess pieces !!!
        # returning initial state
        return self.get_state(self.state)
