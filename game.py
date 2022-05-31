
from cmath import pi
from board import Board
from chess_piece import ChessPiece
from position import Position
from strategy import BishopStrategy, KingStrategy, RookStrategy, QueenStrategy, KnightStrategy




class Game:
    pieces_dict = {"Q": QueenStrategy(),
               "R": RookStrategy(),
               "k": KnightStrategy(),
               "K": KingStrategy(),
               "B": BishopStrategy()}

    def __init__(self,size)-> None:
        self.board = Board(size)

    def draw_self(self):
        print("\n--------GAME-------- \n")
        self.board.draw_board()
        print("\nOPTIONS: ")
        for piece in self.options:
            print(" - " + piece)

    
    def easy_mode(self):
        try:
            snake = [Position(0,4),Position(0,3),Position(0,2),Position(1,2),Position(2,2),Position(2,3),Position(3,3),Position(4,3),Position(4,2),Position(4,1),Position(4,0)]
            self.board.add_snake(snake)
        except Exception as e:
            print(str(e))
        self.options = ["k1","B1"]
        self.play()

    def check_input(self, input):
        if (len(input) != 3):
            raise Exception("User input error: Insufficient arguments, please retry")
        if input[1].isdigit() and input[2].isdigit():
                if (not self.board.valid_pos(Position(int(input[1]),int(input[2])))):
                    raise Exception("User input error: Position must be valid, please retry")
        else:
            raise Exception("User input error: Position must be integers, please retry")

        for piece in self.options:
            if input[0] == piece:
                return
            
        raise Exception("User input error: Piece must exist, please retry")

    def end(self):
        if self.options == []:
            if self.board.check_win():
                print("Game Won!")
            else:
                print("Game Lost!")
            self.draw_self()
            return True
        

    def play(self):
        self.draw_self()
        while not self.end():
            move = input('Insert the piece to play and the position to play it in. Format: <ChessPiece> <X> <Y> (Ex.: K 1 2) \n')
            try:
                moveS = move.split(" ")
                self.check_input(moveS)
                self.board.add_piece(ChessPiece(Position(int(moveS[1]),int(moveS[2])),self.pieces_dict[moveS[0][0]],moveS[0]))
                self.options.remove(moveS[0])
                self.draw_self()
            except Exception as e:
                print(str(e))
