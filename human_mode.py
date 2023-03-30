from board import Board
from chess_piece import ChessPiece
from constants import PIECES_DIC
from position import Position


class HumanMode:
    def __init__(self, board : Board, chess_pieces):
        self.board = board
        self.chess_pieces = chess_pieces

    def play(self,pos):
        try:
            if pos != None and self.chess_pieces != []:
                print(self.chess_pieces)
                print(pos)
                chosen_pos = Position(int(pos[0]),int(pos[1]))
                strategy = PIECES_DIC[self.chess_pieces[0][0]]
                chess_piece_rep = self.chess_pieces[0]
                chess_piece = ChessPiece(chosen_pos,strategy,chess_piece_rep)
                self.board.add_piece(chess_piece)
                self.chess_pieces.remove(self.chess_pieces[0])
        except Exception as e:
            print(str(e))

    def check_input(self, input):
        if (len(input) != 3):
            raise Exception("User input error: Insufficient arguments, please retry")
        if input[1].isdigit() and input[2].isdigit():
                if (not self.board.valid_pos(Position(int(input[1]),int(input[2])))):
                    raise Exception("User input error: Position must be valid, please retry")
        else:
            raise Exception("User input error: Position must be integers, please retry")

        for piece in self.chess_pieces:
            if input[0] == piece:
                return
            
        raise Exception("User input error: Piece must exist, please retry")

    def render(self):
        print("\n--------GAME-------- \n")
        self.board.draw_board()
        print("\nOPTIONS: ")
        for piece in self.chess_pieces:
            print(" - " + piece)
    
