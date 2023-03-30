
import pygame


from constants import BLACK, GREEN, HEIGHT, PIECES_DIC_IMG, RED, WHITE, WIDTH


def window_settings():
    pygame.init()
    window = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Chess Snake')
    return window

def draw_board(window, board,size):
    window.fill(WHITE)
    square_size = WIDTH//size
    l = []
    for row in range(size):
        for col in range(size):
            if (board[col][row] == "O"):
                pygame.draw.rect(
                    window, GREEN, (row*square_size, col * square_size, square_size, square_size), width=0)
            elif (board[col][row] != " "):
                image = pygame.image.load(
                    PIECES_DIC_IMG[board[col][row].representation[0]])
                scaled_sprite = pygame.transform.scale(
                    image, (square_size, square_size))

                window.blit(scaled_sprite,
                            (row*square_size, col * square_size))
                l += board[col][row].implementStrategy(
                    size, board)

            pygame.draw.rect(
                window, BLACK, (row*square_size, col * square_size, square_size, square_size), width=1)
    for i in l:
        if board[i.getY()][i.getX()] == "O":
            pygame.draw.rect(window, RED, (i.getX()*square_size, i.getY()
                                * square_size, square_size, square_size), width=0)
    pygame.display.update()

def process_mouse_press(mouse_pos, board_size):
        # find which square has been pressed
        if mouse_pos[1] > HEIGHT:
            return None
        square_size = int(WIDTH/ board_size)
        return ( mouse_pos[0] // square_size,mouse_pos[1] // square_size)