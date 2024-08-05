import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
ROWS, COLS = 10, 10
MINE_COUNT = 10
TILE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (192, 192, 192)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
NUM_COLORS = [BLACK, BLUE, GREEN, RED, (0, 0, 128), (128, 0, 0), (64, 224, 208), BLACK, GREY]

# Fonts
FONT = pygame.font.Font(None, 36)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Minesweeper')

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0

    def draw(self):
        if self.is_revealed:
            if self.is_mine:
                pygame.draw.rect(screen, RED, self.rect)
            else:
                pygame.draw.rect(screen, WHITE, self.rect)
                if self.neighbor_mines > 0:
                    text = FONT.render(str(self.neighbor_mines), True, NUM_COLORS[self.neighbor_mines])
                    screen.blit(text, (self.x * TILE_SIZE + TILE_SIZE // 3, self.y * TILE_SIZE + TILE_SIZE // 4))
        else:
            pygame.draw.rect(screen, GREY, self.rect)
            if self.is_flagged:
                pygame.draw.line(screen, RED, (self.x * TILE_SIZE, self.y * TILE_SIZE), 
                                 (self.x * TILE_SIZE + TILE_SIZE, self.y * TILE_SIZE + TILE_SIZE), 2)
                pygame.draw.line(screen, RED, (self.x * TILE_SIZE, self.y * TILE_SIZE + TILE_SIZE), 
                                 (self.x * TILE_SIZE + TILE_SIZE, self.y * TILE_SIZE), 2)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

def create_board():
    board = [[Tile(x, y) for y in range(ROWS)] for x in range(COLS)]
    mines_placed = 0
    while mines_placed < MINE_COUNT:
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)
        if not board[x][y].is_mine:
            board[x][y].is_mine = True
            mines_placed += 1
    for x in range(COLS):
        for y in range(ROWS):
            if not board[x][y].is_mine:
                board[x][y].neighbor_mines = sum(board[nx][ny].is_mine for nx in range(x-1, x+2) for ny in range(y-1, y+2)
                                                 if 0 <= nx < COLS and 0 <= ny < ROWS)
    return board

def reveal_tile(board, x, y):
    if board[x][y].is_revealed or board[x][y].is_flagged:
        return
    board[x][y].is_revealed = True
    if board[x][y].neighbor_mines == 0 and not board[x][y].is_mine:
        for nx in range(x-1, x+2):
            for ny in range(y-1, y+2):
                if 0 <= nx < COLS and 0 <= ny < ROWS:
                    reveal_tile(board, nx, ny)

def check_win(board):
    return all(tile.is_revealed or tile.is_mine for row in board for tile in row)

def main():
    board = create_board()
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                x //= TILE_SIZE
                y //= TILE_SIZE
                if event.button == 1:  # Left click
                    if board[x][y].is_mine:
                        game_over = True
                    else:
                        reveal_tile(board, x, y)
                elif event.button == 3:  # Right click
                    board[x][y].is_flagged = not board[x][y].is_flagged
        
        screen.fill(WHITE)
        for row in board:
            for tile in row:
                tile.draw()
        
        if check_win(board):
            game_over = True
            text = FONT.render("You Win!", True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        if game_over:
            text = FONT.render("Game Over", True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
