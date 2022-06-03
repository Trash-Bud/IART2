from chess_piece import ChessPiece
from position import Position

class Board:
    def __init__(self, size: int, piece_num: int)-> None:
        # number of pieces that are going to be placed in the board
        self.piece_num = piece_num
        # size of the board
        self.size = size
        # creating empty board
        board = []
        for i in range(0,size):
            arr = []
            for e in range(0,size):
                arr.append(" ")
            board.append(arr)
        # saving board as a local variable
        self.board = board
        #array of chess pieces placed in the board
        self.chess_pieces = []

    # gets the coordinates of all playable squares
    def playable_squares(self):
        num = []
        for i in range(0,self.size):
            for e in range(0,self.size):
                if self.board[i][e] == " ":
                    num.append([e,i])
        return num

    # gets the number of playable squares in the board
    def playable_squares_num(self):
        return len(self.playable_squares())

    # gets the number of squares that the snake occupies
    def snake_size(self):
        num = 0
        for i in range(0,self.size):
            for e in range(0,self.size):
                if self.board[i][e] == "O":
                    num += 1
        return num

    
    # adds a snake to the board
    # note: snake is a list nof positions
    def add_snake(self,snake: list):
        try:
            self.validate_snake(snake)
            for i in range(0,len(snake)):
                self.board[snake[i].getY()][snake[i].getX()] = "O" 
        except Exception as e:
            raise e

    # makes sure snake is valid 
    def validate_snake(self,snake: list):
        if snake[0].getX() != 0 or snake[0].getY() != self.size - 1:
            raise Exception("Board Error: Snake must start in position 0,"+ str(self.size - 1))
        if snake[len(snake)-1].getX() != self.size - 1 or snake[len(snake)-1].getY() != 0:
            raise Exception("Board Error: Snake must start in position" + str(self.size - 1) + ",0")
        for i in range(0,len(snake)):
            if not self.valid_pos(snake[i]):
                raise Exception("Board Error: The snake's body must be within the board's limits")
            arr = 0
            for e in range(0,len(snake)):
                if self.snake_eats_itself(snake[i].getX(),snake[e].getX(),snake[i].getY(),snake[e].getY()):
                    arr += 1
                if arr > 2:
                    raise Exception("Board Error: The snake eats itself (at least one part of its body touches more than one other part of it")

    # checks if the snake eats itself making it invalid
    def snake_eats_itself(self, x1,x2,y1,y2):
        if x1 == x2 and (y1 == y2 +1 or y1 == y2 -1):
            return True
        elif y1 == y2 and (x1 == x2 +1 or x1 == x2 -1):
            return True
        return False

    # draws board to console
    def draw_board(self):
        for i in range(0,self.size):
            print(str(i) + " [",end = ' ')
            for e in range(0, self.size):
                if(type(self.board[i][e]) == ChessPiece):
                    print(self.board[i][e].representation, end = '')
                else:
                    print(self.board[i][e], end = ' ')
            print("]")
        print("   ",end = " ")
        for i in range(0,self.size):
            print(str(i),end = " ")
        print("\n")

    # checks if chess piece can be placed in position
    def check_if_pos_is_valid(self, position: Position) -> None:
        if not self.valid_pos(position):
            raise Exception("Piece error: position chosen is invalid")

        x = position.getX()
        y = position.getY()

        if (self.board[y][x] != " "):
            raise Exception("Piece error: Square is occupied")
        return True

    # adds a chess piece to the board
    def add_piece(self, chess_piece: ChessPiece) -> None:
        x = chess_piece.position.getX()
        y = chess_piece.position.getY()
        try:
            if self.check_if_pos_is_valid(chess_piece.position):
                self.chess_pieces.append(chess_piece)
                self.board[y][x] = chess_piece
        except Exception as e:
            raise e

    # removes a chess piece from the board
    def remove_piece(self, position) -> None:
        if not self.valid_pos(position):
            raise Exception("Piece error: position chosen is invalid")
        for piece in self.chess_pieces:
            if piece.position == position:
                self.chess_pieces.remove(piece)
        raise Exception("Piece error: Square is occupied")

    # checks if a position is within board bounds
    def valid_pos(self, position):
        return position.getX() < self.size  or position.getY() < self.size or position.getX() >= 0 or position.getY() >= 0
    
    # gets the number of attacks of each chess piece placed in the board
    def get_attacks(self):
        nums = []
        for piece in self.chess_pieces:
            num = 0
            l = piece.implementStrategy(self.size,self.board)
            for pos in l:
                if self.board[pos.getY()][pos.getX()] == "O":
                    num += 1
            nums.append(num)
        return nums

    # checks if the game was won
    def check_win(self):
        nums = self.get_attacks()
        if(nums.count(nums[0]) != len(nums)):
            return False
        return True
    
    # checks if the game ended and if it was won
    def end(self):
        if self.piece_num == len(self.chess_pieces):
            if self.check_win():
                print("Game Won!")
                return True
            else:
                print("Game Lost!")
                return False

    # clears board but without removing the snake
    def clear(self):
        for i in range(0,len(self.chess_pieces)):
            self.chess_pieces.remove(self.chess_pieces[0])
        for i in range(0,self.size):
            for e in range(0, self.size):
                if(self.board[i][e] != "O"):
                    self.board[i][e] = " "



