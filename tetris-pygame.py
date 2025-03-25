import pygame
import random

# Pygame setup
pygame.init()
width, height = 300, 600
cell_size = 30
cols, rows = width // cell_size, height // cell_size
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Tetromino shapes
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

COLORS = {
    'I': (0, 255, 255), 'O': (255, 255, 0), 'T': (128, 0, 128),
    'S': (0, 255, 0), 'Z': (255, 0, 0), 'J': (0, 0, 255), 'L': (255, 165, 0)
}

# Piece class
class Piece:
    def __init__(self, shape):
        self.shape = SHAPES[shape]
        self.color = COLORS[shape]
        self.x = cols // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Game state
board = [[0] * cols for _ in range(rows)]
current = Piece(random.choice(list(SHAPES)))
def check_collision(piece, dx=0, dy=0):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                nx, ny = piece.x + x + dx, piece.y + y + dy
                if nx < 0 or nx >= cols or ny >= rows or (ny >= 0 and board[ny][nx]):
                    return True
    return False

def merge(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                board[piece.y + y][piece.x + x] = piece.color

def clear_lines():
    global board
    board = [row for row in board if any(cell == 0 for cell in row)]
    while len(board) < rows:
        board.insert(0, [0] * cols)

def draw_board():
    screen.fill((0, 0, 0))
    for y in range(rows):
        for x in range(cols):
            if board[y][x]:
                pygame.draw.rect(screen, board[y][x], (x*cell_size, y*cell_size, cell_size, cell_size))
    for y, row in enumerate(current.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, current.color, ((current.x+x)*cell_size, (current.y+y)*cell_size, cell_size, cell_size))
    pygame.display.flip()

# Game loop
fall_time = 0
running = True
while running:
    dt = clock.tick(60)
    fall_time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not check_collision(current, dx=-1):
                current.x -= 1
            elif event.key == pygame.K_RIGHT and not check_collision(current, dx=1):
                current.x += 1
            elif event.key == pygame.K_DOWN and not check_collision(current, dy=1):
                current.y += 1
            elif event.key == pygame.K_UP:
                old_shape = current.shape[:]
                current.rotate()
                if check_collision(current):
                    current.shape = old_shape

    if fall_time > 500:
        if not check_collision(current, dy=1):
            current.y += 1
        else:
            merge(current)
            clear_lines()
            current = Piece(random.choice(list(SHAPES)))
            if check_collision(current):
                print("Game Over")
                running = False
        fall_time = 0

    draw_board()

pygame.quit()