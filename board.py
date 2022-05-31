from chess_piece import ChessPiece
from position import Position


class Board:
    def __init__(self, size: int)-> None:
        self.size = size
        board = []
        for i in range(0,size):
            arr = []
            for e in range(0,size):
                arr.append(" ")
            board.append(arr)
        self.board = board
        self.chess_pieces = []
    
    # snake is a list of positions
    def add_snake(self,snake):
        try:
            self.validate_snake(snake)
            for i in range(0,len(snake)):
                self.board[snake[i].getY()][snake[i].getX()] = "O" 
        except Exception as e:
            raise e
        
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

    def snake_eats_itself(self, x1,x2,y1,y2):
        if x1 == x2 and (y1 == y2 +1 or y1 == y2 -1):
            return True
        elif y1 == y2 and (x1 == x2 +1 or x1 == x2 -1):
            return True
        return False

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


    def add_piece(self, chess_piece: ChessPiece) -> None:
        if not self.valid_pos(chess_piece.position):
            raise Exception("Piece error: position chosen is invalid")

        x = chess_piece.position.getX()
        y = chess_piece.position.getY()

        if (self.board[y][x] != " "):
            raise Exception("Piece error: Square is occupied")

        self.chess_pieces.append(chess_piece)
        self.board[y][x] = chess_piece

    def remove_piece(self, position) -> None:
        if not self.valid_pos(position):
            raise Exception("Piece error: position chosen is invalid")
        for piece in self.chess_pieces:
            if piece.position == position:
                self.chess_pieces.remove(piece)
        raise Exception("Piece error: Square is occupied")

    def valid_pos(self, position):
        return position.getX() < self.size  or position.getY() < self.size or position.getX() >= 0 or position.getY() >= 0
    
    def check_win(self):
        nums = []
        for piece in self.chess_pieces:
            num = 0
            l = piece.implementStrategy(self.size,self.board)
            for pos in l:
                if self.board[pos.getY()][pos.getX()] == "O":
                    num += 1

            if(nums.count(num) != len(nums)):
                return False
        return True
