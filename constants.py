
from strategy import BishopStrategy, KingStrategy, RookStrategy, QueenStrategy, KnightStrategy

# dictionary that connects chess piece representations to their attack strategy
PIECES_DIC = {"Q": QueenStrategy(),
            "R": RookStrategy(),
            "k": KnightStrategy(),
            "K": KingStrategy(),
            "B": BishopStrategy()}