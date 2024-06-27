import pygame
import sys
import math
import random

# Initialize pygame
pygame.init()

# Constants for the game
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# Colors
WHITE = (255, 255, 255)
LINE_COLOR = (23, 145, 135)
BG_COLOR = (28, 170, 156)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

# Board
board = [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Fonts
FONT = pygame.font.SysFont('comicsans', 80)


def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)

    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + 20),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + SQUARE_SIZE - 20),
                                 LINE_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + 20),
                                 (col * SQUARE_SIZE + 20, row * SQUARE_SIZE + SQUARE_SIZE - 20), LINE_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                   int(SQUARE_SIZE / 2) - 20, LINE_WIDTH)


def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] == ' '


def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == ' ':
                return False
    return True


def check_win(player):
    # Check rows and columns
    for row in range(BOARD_ROWS):
        if all([board[row][col] == player for col in range(BOARD_COLS)]) or \
                all([board[col][row] == player for col in range(BOARD_COLS)]):
            return True

    # Check diagonals
    if all([board[i][i] == player for i in range(BOARD_COLS)]) or \
            all([board[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_COLS)]):
        return True

    return False


def draw_winner(winner):
    if winner == 'X':
        text = FONT.render('X Wins!', True, CROSS_COLOR)
    else:
        text = FONT.render('O Wins!', True, CIRCLE_COLOR)

    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(1500)


def reset_game():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = ' '


def minimax(board, depth, is_maximizing):
    if check_win('O'):
        return 10 - depth
    elif check_win('X'):
        return depth - 10
    elif is_board_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[row][col] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[row][col] = ' '
                    best_score = min(score, best_score)
        return best_score


def find_best_move():
    best_score = -math.inf
    best_move = (-1, -1)

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == ' ':
                board[row][col] = 'O'
                score = minimax(board, 0, False)
                board[row][col] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    return best_move


def main():
    screen.fill(BG_COLOR)
    draw_lines()

    player = 'X'
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if player == 'X' and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)

                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    if check_win(player):
                        draw_winner(player)
                        reset_game()
                    elif is_board_full():
                        reset_game()
                    else:
                        player = 'O'

            elif player == 'O':
                row, col = find_best_move()
                mark_square(row, col, player)
                if check_win(player):
                    draw_winner(player)
                    reset_game()
                elif is_board_full():
                    reset_game()
                else:
                    player = 'X'

        draw_figures()

        pygame.display.update()

main()
