import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 10
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
WORDS = ["PYTHON", "PYGAME", "GAME", "WORD", "SEARCH"]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Setup display
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Word Search Game')
font = pygame.font.Font(None, CELL_SIZE)

# Create a blank grid
grid = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def place_word(word):
    direction = random.choice(['H', 'V'])
    if direction == 'H':
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - len(word))
        for i in range(len(word)):
            grid[row][col + i] = word[i]
    else:
        row = random.randint(0, GRID_SIZE - len(word))
        col = random.randint(0, GRID_SIZE - 1)
        for i in range(len(word)):
            grid[row + i][col] = word[i]

# Fill the grid with words
for word in WORDS:
    place_word(word)

# Fill the rest of the grid with random letters
for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        if grid[row][col] == '':
            grid[row][col] = chr(random.randint(65, 90))  # A-Z

# Selected cells
selected_cells = []

def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(window, WHITE, cell_rect)
            pygame.draw.rect(window, BLACK, cell_rect, 1)
            text = font.render(grid[row][col], True, BLACK)
            window.blit(text, (col * CELL_SIZE + 10, row * CELL_SIZE + 10))
            if (row, col) in selected_cells:
                pygame.draw.rect(window, GREEN, cell_rect, 3)

def check_word():
    selected_word = ''.join([grid[row][col] for row, col in selected_cells])
    return selected_word in WORDS

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            col = pos[0] // CELL_SIZE
            row = pos[1] // CELL_SIZE
            if (row, col) not in selected_cells:
                selected_cells.append((row, col))
            else:
                selected_cells.remove((row, col))
            
            if len(selected_cells) > 1 and check_word():
                selected_cells = []

    window.fill(BLACK)
    draw_grid()
    pygame.display.flip()

pygame.quit()

