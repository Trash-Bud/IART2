
import string
from position import Position


class ChessPiece():
    def __init__(self, position: Position, move_strategy, representation: string) -> None:
        self.move_strategy = move_strategy
        self.position = position
        self.representation = representation

    @property
    def getMoveStrategy(self):
        return self.move_strategy

    @property
    def getPosition(self) -> Position:
        return self.position

    def setMoveStrategy(self, move_strategy) -> None:
        self.move_strategy = move_strategy

    def implementStrategy(self, board_size, board):
        return self.move_strategy.execute(self.position, board_size, board)