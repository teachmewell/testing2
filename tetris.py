#unchanged code from chatgpt

import pygame
import random

pygame.init()

# Screen
WIDTH, HEIGHT = 300, 600
BLOCK = 30
COLS, ROWS = WIDTH // BLOCK, HEIGHT // BLOCK

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

COLORS = [
    (0, 255, 255),   # I
    (0, 0, 255),     # J
    (255, 165, 0),   # L
    (255, 255, 0),   # O
    (0, 255, 0),     # S
    (160, 32, 240),  # T
    (255, 0, 0),     # Z
]

SHAPES = [
    [[1, 1, 1, 1]],

    [[1, 0, 0],
     [1, 1, 1]],

    [[0, 0, 1],
     [1, 1, 1]],

    [[1, 1],
     [1, 1]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[0, 1, 0],
     [1, 1, 1]],

    [[1, 1, 0],
     [0, 1, 1]],
]


class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = COLORS[SHAPES.index(self.shape)]
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]


def valid(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                nx = piece.x + x
                ny = piece.y + y

                if nx < 0 or nx >= COLS or ny >= ROWS:
                    return False

                if ny >= 0 and grid[ny][nx] != BLACK:
                    return False
    return True


def merge(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[piece.y + y][piece.x + x] = piece.color


def clear_lines():
    global grid
    new_grid = [row for row in grid if BLACK in row]
    cleared = ROWS - len(new_grid)
    for _ in range(cleared):
        new_grid.insert(0, [BLACK] * COLS)
    grid = new_grid
    return cleared


piece = Piece()

fall_time = 0
fall_speed = 500

score = 0
font = pygame.font.SysFont(None, 30)

running = True

while running:
    dt = clock.tick(60)
    fall_time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                piece.x -= 1
                if not valid(piece):
                    piece.x += 1

            elif event.key == pygame.K_RIGHT:
                piece.x += 1
                if not valid(piece):
                    piece.x -= 1

            elif event.key == pygame.K_DOWN:
                piece.y += 1
                if not valid(piece):
                    piece.y -= 1

            elif event.key == pygame.K_UP:
                old = [r[:] for r in piece.shape]
                piece.rotate()
                if not valid(piece):
                    piece.shape = old

    if fall_time > fall_speed:
        fall_time = 0
        piece.y += 1

        if not valid(piece):
            piece.y -= 1
            merge(piece)
            score += clear_lines() * 100
            piece = Piece()

            if not valid(piece):
                running = False

    screen.fill(BLACK)

    # Draw grid
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(
                screen,
                grid[y][x],
                (x * BLOCK, y * BLOCK, BLOCK, BLOCK),
            )
            pygame.draw.rect(
                screen,
                GRAY,
                (x * BLOCK, y * BLOCK, BLOCK, BLOCK),
                1,
            )

    # Draw current piece
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    piece.color,
                    (
                        (piece.x + x) * BLOCK,
                        (piece.y + y) * BLOCK,
                        BLOCK,
                        BLOCK,
                    ),
                )
                pygame.draw.rect(
                    screen,
                    GRAY,
                    (
                        (piece.x + x) * BLOCK,
                        (piece.y + y) * BLOCK,
                        BLOCK,
                        BLOCK,
                    ),
                    1,
                )

    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
