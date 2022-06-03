
from strategy import BishopStrategy, KingStrategy, RookStrategy, QueenStrategy, KnightStrategy

# dictionary that connects chess piece representations to their attack strategy
PIECES_DIC = {"Q": QueenStrategy(),
            "R": RookStrategy(),
            "k": KnightStrategy(),
            "K": KingStrategy(),
            "B": BishopStrategy()}

# value of the learning rate / step size
ALPHA = 0.1

# value of the discount factor
GAMA = 0.6

# chance of choosing a random action to explore
EPSILON = 0.1

# number of episodes
EPISODES = 10000