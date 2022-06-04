
from strategy import BishopStrategy, KingStrategy, RookStrategy, QueenStrategy, KnightStrategy

# dictionary that connects chess piece representations to their attack strategy
PIECES_DIC = {"Q": QueenStrategy(),
            "R": RookStrategy(),
            "k": KnightStrategy(),
            "K": KingStrategy(),
            "B": BishopStrategy()}

# dictionary that connects chess piece representations to their sprite
PIECES_DIC_IMG = {"Q": "piece_sprites/queen_sprite.png",
            "R": "piece_sprites/rook_sprite.png",
            "k": "piece_sprites/knight_sprite.png",
            "K": "piece_sprites/king_sprite.png",
            "B": "piece_sprites/bishop_sprite.png"}


# value of the learning rate / step size
ALPHA = 0.1

# value of the discount factor
GAMA = 0.6

# chance of choosing a random action to explore
EPSILON = 0.1

# number of episodes
EPISODES = 20000

# every 1000 episodes register data for analysis
SHOW_EVERY = 500

# pygame window size
WIDTH, HEIGHT = 400, 400 

# colors
RED = (255,0,0,10)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

# variable for using pygame
USE_PYGAME = True