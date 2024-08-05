import pygame
import sys
import random

# Constants
GRID_SIZE = 4
TILE_SIZE = 100
TILE_MARGIN = 10
HEADER_HEIGHT = 120
WINDOW_WIDTH = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * TILE_MARGIN
WINDOW_HEIGHT = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * TILE_MARGIN + HEADER_HEIGHT
BACKGROUND_COLOR = (238, 228, 218)
HEADER_COLOR = (143, 122, 102)
SCORE_COLOR = (119, 110, 101)
TEXT_COLOR = (119, 110, 101)
HEADER_FONT_SIZE = 45
SCORE_FONT_SIZE = 36

# Tile colors based on the value
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (249, 246, 185),
    16: (170, 251, 186),
    32: (115, 209, 48),
    64: (0, 119, 0),
    128: (0, 93, 93),
    256: (0, 119, 119),
    512: (0, 85, 85),
    1024: (0, 60, 60),
    2048: (0, 35, 35),
}

def init_fonts():
    global TILE_FONT, HEADER_FONT, SCORE_FONT
    TILE_FONT = pygame.font.Font(None, 55)
    HEADER_FONT = pygame.font.Font(None, HEADER_FONT_SIZE)
    SCORE_FONT = pygame.font.Font(None, SCORE_FONT_SIZE)

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("2048 Game")
init_fonts()

class Game2048:
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.reset()

    def reset(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty_tiles = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if not empty_tiles:
            return
        row, col = random.choice(empty_tiles)
        self.grid[row][col] = 4 if random.random() < 0.1 else 2

    def can_move(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] == 0:
                    return True
                if col < GRID_SIZE - 1 and self.grid[row][col] == self.grid[row][col + 1]:
                    return True
                if row < GRID_SIZE - 1 and self.grid[row][col] == self.grid[row + 1][col]:
                    return True
        return False

    def move(self, direction):
        if direction == "LEFT":
            self.grid = self._move_left()
        elif direction == "RIGHT":
            self.grid = self._move_right()
        elif direction == "UP":
            self.grid = self._move_up()
        elif direction == "DOWN":
            self.grid = self._move_down()
        self.add_random_tile()

    def _move_left(self):
        new_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        for r in range(GRID_SIZE):
            fill_position = 0
            for c in range(GRID_SIZE):
                if self.grid[r][c] != 0:
                    new_grid[r][fill_position] = self.grid[r][c]
                    fill_position += 1
            for c in range(GRID_SIZE - 1):
                if new_grid[r][c] == new_grid[r][c + 1] and new_grid[r][c] != 0:
                    new_grid[r][c] *= 2
                    self.score += new_grid[r][c]
                    new_grid[r][c + 1] = 0
            new_grid[r] = [num for num in new_grid[r] if num != 0]
            new_grid[r] += [0] * (GRID_SIZE - len(new_grid[r]))
        return new_grid

    def _move_right(self):
        new_grid = [list(reversed(row)) for row in self.grid]
        new_grid = self._move_left()
        return [list(reversed(row)) for row in new_grid]

    def _move_up(self):
        new_grid = [list(row) for row in zip(*self.grid)]
        new_grid = self._move_left()
        return [list(row) for row in zip(*new_grid)]

    def _move_down(self):
        new_grid = [list(reversed(row)) for row in zip(*self.grid)]
        new_grid = self._move_left()
        new_grid = [list(reversed(row)) for row in zip(*new_grid)]
        return new_grid

    def draw(self, screen):
        screen.fill(BACKGROUND_COLOR)
        
        # Draw headers
        header_surface = HEADER_FONT.render("2048", True, TEXT_COLOR)
        header_rect = header_surface.get_rect(center=(WINDOW_WIDTH // 2, TILE_MARGIN + HEADER_HEIGHT // 4))
        screen.blit(header_surface, header_rect)

        guide_surface = HEADER_FONT.render("Game Guide", True, TEXT_COLOR)
        guide_rect = guide_surface.get_rect(center=(WINDOW_WIDTH // 2, TILE_MARGIN + HEADER_HEIGHT // 2))
        screen.blit(guide_surface, guide_rect)
        
        # Draw score
        score_surface = SCORE_FONT.render(f"Score: {self.score}", True, SCORE_COLOR)
        score_rect = score_surface.get_rect(topleft=(TILE_MARGIN, HEADER_HEIGHT - 40))
        screen.blit(score_surface, score_rect)

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                value = self.grid[row][col]
                color = TILE_COLORS.get(value, (60, 58, 50))
                rect = pygame.Rect(
                    col * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN,
                    row * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN + HEADER_HEIGHT,
                    TILE_SIZE,
                    TILE_SIZE,
                )
                pygame.draw.rect(screen, color, rect, border_radius=8)
                pygame.draw.rect(screen, HEADER_COLOR, rect, 1)  # 1-pixel border
                if value:
                    text_surface = TILE_FONT.render(str(value), True, TEXT_COLOR)
                    text_rect = text_surface.get_rect(center=rect.center)
                    screen.blit(text_surface, text_rect)

        pygame.display.flip()

def main():
    game = Game2048()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move("LEFT")
                elif event.key == pygame.K_RIGHT:
                    game.move("RIGHT")
                elif event.key == pygame.K_UP:
                    game.move("UP")
                elif event.key == pygame.K_DOWN:
                    game.move("DOWN")
                elif event.key == pygame.K_r:
                    game.reset()

        if not game.can_move():
            print("Game Over!")
            pygame.quit()
            sys.exit()

        game.draw(screen)
        clock.tick(30)

if __name__ == "__main__":
    main()
