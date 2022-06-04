from game import Game
from constants import USE_PYGAME
from pygame_utils import window_settings

def main():
    if USE_PYGAME:
        window_settings()
    game = Game()


main()
