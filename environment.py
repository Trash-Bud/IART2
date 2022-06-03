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
        self.board = board
        self.chess_pieces = chess_pieces
        self.piece_num = 0
        self.state = [[-1,-1],[-1,-1]] #only works for 2 chess pieces
        self.generate_states_array() #only works for 2 chess pieces
        self.actions_array = board.playable_squares()
        self.action_space_length = board.playable_squares_num()
        self.observation_space_length = len(self.states_array) #only works for 2 chess pieces

    
    def generate_states_array(self):
        self.states_array = []
        self.states_array.append([[-1,-1],[-1,-1]])
        playable_squares = self.board.playable_squares()
        for i in range(0,self.board.size):
            for e in range(0,self.board.size):
                if ([i,e] in playable_squares):
                    self.states_array.append([[i,e],[-1,-1]])
                for f in range(0,self.board.size):
                    for g in range(0,self.board.size):
                        if ([i,e] in playable_squares) and ([f,g] in playable_squares) and ([i,e] != [f,g]) :
                            self.states_array.append([[i,e],[f,g]])

    def get_state(self, array):
        return self.states_array.index(array)

    def get_action(self, array):
        return self.actions_array.index(array)

    def step(self, action):
        possible_moves_list = self.actions_array
        pos = possible_moves_list[action]
        chess_piece = ChessPiece(Position(pos[0],pos[1]),PIECES_DIC[self.chess_pieces[0][0]],self.chess_pieces[0])
        self.chess_pieces.remove(self.chess_pieces[0])
        self.board.add_piece(chess_piece)
        self.state[self.piece_num] = pos
        reward = 0
        if self.board.end():
            done = True
            reward = 10
        else:
            if(len(self.board.chess_pieces) == self.board.piece_num):
                done = True
                reward = -10
            else:
                done = False
        info = {}
        self.piece_num += 1
        return self.get_state(self.state), reward, done, info

    def render(self):
        self.board.draw_board()
    
    def reset(self):
        print("resetting..")

        for i in range(0,len(self.board.chess_pieces)):
            self.chess_pieces.append(self.board.chess_pieces[i].representation)
        self.board.clear()
        self.board.draw_board
        self.piece_num = 0
        self.state = [[-1,-1],[-1,-1]] #only works for 2 chess pieces
        return self.get_state(self.state)
