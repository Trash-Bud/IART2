from abc import ABC, abstractmethod
from chess_piece import ChessPiece
from position import Position
class Strategy(ABC):  # Strategy
    @abstractmethod
    def execute(self, position: Position, board_size, matrix):
        pass

    def adjacent_attacks(self,x,y,board_size,matrix):
        attackedPositions = []
        for i in range(x-1,x+2):
            if (i < board_size and i >= 0):
                for e in range(y-1,y+2):
                    if (e < board_size and e >= 0):
                        if type(matrix[e][i]) != ChessPiece:
                            attackedPositions.append(Position(i,e))

        return attackedPositions

    def line_attacks(self,x,y,board_size,matrix):
        attackedPositions = []
        for i in range(x+1,board_size):
            if type(matrix[y][i]) == ChessPiece:
                        break
            else:
                attackedPositions.append(Position(i,y))

        for i in range(x-1,-1,-1):
            if type(matrix[y][i]) == ChessPiece:
                        break
            else:
                attackedPositions.append(Position(i,y))

        for i in range(y+1,board_size):
            if type(matrix[i][x]) == ChessPiece:
                        break
            else:
                attackedPositions.append(Position(x,i))

        for i in range(y-1,-1,-1):
            if type(matrix[i][x]) == ChessPiece:
                        break
            else:
                attackedPositions.append(Position(x,i))

        return attackedPositions


    def diagonal_attacks(self, x, y, board_size, matrix):
        attackedPositions = []
        for i in range(x+1,board_size):
            for e in range(y+1,board_size):
                if abs(i - x) == abs(e - y):
                    if type(matrix[e][i]) == ChessPiece:
                        break
                    else:
                        attackedPositions.append(Position(i,e))
        
        for i in range(x-1,-1,-1):
            for e in range(y-1,-1,-1):
                if abs(i - x) == abs(e - y):
                    if type(matrix[e][i]) == ChessPiece:
                        break
                    else:
                        attackedPositions.append(Position(i,e))

        for i in range(x+1,board_size):
            for e in range(y-1,-1,-1):
                if abs(i - x) == abs(e - y):
                    if type(matrix[e][i]) == ChessPiece:
                        break
                    else:
                        attackedPositions.append(Position(i,e))
        
        for i in range(x-1,-1,-1):
            for e in range(y+1,board_size):
                if abs(i - x) == abs(e - y):
                    if type(matrix[e][i]) == ChessPiece:
                        break
                    else:
                        attackedPositions.append(Position(i,e))
        return attackedPositions


class KingStrategy(Strategy):
    def execute(self, position: Position, board_size, matrix):

        x = position.getX()
        y = position.getY()

        return self.adjacent_attacks(x,y,board_size,matrix)

class BishopStrategy(Strategy):
    def execute(self, position: Position, board_size, matrix):
        x = position.getX()
        y = position.getY()
        return self.diagonal_attacks(x,y,board_size,matrix)


class QueenStrategy(Strategy):
    def execute(self, position: Position, board_size, matrix):
        attackedPositions = []

        x = position.getX()
        y = position.getY()

        diagonal_attacks = self.diagonal_attacks(x,y,board_size,matrix)
        line_attacks = self.line_attacks(x,y,board_size,matrix)
        adjacent_attacks = self.adjacent_attacks(x,y,board_size,matrix)

        attackedPositions = diagonal_attacks + line_attacks + adjacent_attacks

        return attackedPositions

class RookStrategy(Strategy):
    def execute(self, position: Position, board_size, matrix):
        x = position.getX()
        y = position.getY()

        return self.line_attacks(x,y,board_size,matrix)


class KnightStrategy(Strategy):

    def check_in_board(self, x, y, board_size):
        return x >= 0 and x < board_size and y >= 0 and y < board_size

    def execute(self, position: Position, board_size, matrix):
        attackedPositions = []
        x = position.getX()
        y = position.getY()

        horse_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1)]

        for move in horse_moves:
            move_x = x + move[0]
            move_y = y + move[1]

            if self.check_in_board(move_x, move_y, board_size) and type(matrix[move_x][move_y]) != ChessPiece:
                attackedPositions.append(Position(move_x, move_y))
            move_x = x + move[1]
            move_y = y + move[0]
            if self.check_in_board(move_y, move_x, board_size) and type(matrix[move_y][move_x]) != ChessPiece:
                attackedPositions.append(Position(move_x, move_y))
        return attackedPositions
