
from strategy import BishopStrategy, KingStrategy, RookStrategy, QueenStrategy, KnightStrategy

PIECES_DIC = {"Q": QueenStrategy(),
            "R": RookStrategy(),
            "k": KnightStrategy(),
            "K": KingStrategy(),
            "B": BishopStrategy()}