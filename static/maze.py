import pygame
import random
import time

pygame.init()

# All fonts used
font1 = pygame.font.SysFont("comicsansms", 49, True)
font2 = pygame.font.SysFont("comicsansms", 150, True)
font3 = pygame.font.SysFont("comicsansms", 28, True)

# Creates the string that displays time
def get_time(hours, minutes, seconds):
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Creates the time counter
def draw_time(start_time, pause_time):
    elapsed_time = int(time.time() - pause_time - start_time)
    hours, elapsed_time = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(elapsed_time, 60)
    time_str = get_time(hours, minutes, seconds)
    return [font1.render(time_str, True, (0, 0, 0), (255, 255, 255)), time_str]

class Cell:
    def __init__(self, up, down, left, right):
        self.visited = False
        self.walls = [up, down, left, right]

class Labyrinth:
    # Generates the maze
    def __init__(self, id):
        self.id = id
        self.walls = []
        self.maze_walls = []
        self.cells = []

        x = 0
        t = 0

        # Creates all cell within the maze
        for f in range(22):
            for s in range(28):
                # If command makes sure no cells are created where the clock is supposed to be
                if not (f in (0, 1, 2) and s > 20):
                    self.cells.append(Cell((x + 8, t, 25, 8), (x + 8, t + 33, 25, 8), (x, t + 8, 8, 25), (x + 33, t + 8, 8, 25)))
                x += 33
            x = 0
            t += 33

        # Generates maze using Prim's algorithm
        for v in self.cells[0].walls:
            self.maze_walls.append(v)
            self.walls.append(v)

        self.cells[0].visited = True

        while self.walls:
            wall = random.choice(self.walls)
            divided_cells = [u for u in self.cells if wall in u.walls]

            if len(divided_cells) > 1 and (divided_cells[0].visited != divided_cells[1].visited):
                for k in divided_cells:
                    k.walls.remove(wall)
                    if not k.visited:
                        k.visited = True
                        for q in k.walls:
                            if q not in self.walls:
                                self.walls.append(q)
                            if q not in self.maze_walls:
                                self.maze_walls.append(q)
                        if wall in self.maze_walls:
                            self.maze_walls.remove(wall)
            self.walls.remove(wall)

        for j in range(0, 736, 33):
            for i in range(0, 951, 33):
                self.maze_walls.append((i, j, 8, 8))

    # Draws the maze
    def draw(self, screen, color, goal):
        screen.fill((0, 0, 0))
        for k in self.maze_walls:
            pygame.draw.rect(screen, color, pygame.Rect(k[0], k[1], k[2], k[3]))

        pygame.draw.rect(screen, color, pygame.Rect(695, 0, 300, 105))  # Clock background
        pygame.draw.rect(screen, (0, 255, 0), goal)  # Finish

def main():
    screen = pygame.display.set_mode((930, 733))
    id = 0
    running = True
    color = (0, 128, 255)  # Color of the walls
    clock = pygame.time.Clock()

    while running:
        done = False
        x, y = 16, 16
        start = time.time()
        id += 1
        maze = Labyrinth(id)
        goal = pygame.Rect(899, 701, 25, 25)
        victory = False
        speed = 4  # Movement speed
        pause = False
        pause_time = 0  # Time spent in pause menu

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_p):
                        if pause:
                            pause = False
                            pause_time += time.time() - pause_time_start
                        else:
                            pause = True
                            pause_time_start = time.time()

                    if event.key == pygame.K_RETURN:
                        done = True

            if pause:
                screen.fill((0, 0, 0))
                pause_text = font2.render("PAUSE", True, (255, 255, 255))
                screen.blit(pause_text, (468 - (pause_text.get_width() // 2), 368 - (pause_text.get_height() // 2)))
            else:
                move_up = move_down = move_left = move_right = True
                pressed = pygame.key.get_pressed()

                # Movement
                if pressed[pygame.K_w] or pressed[pygame.K_UP]:
                    player = pygame.Rect(x, y - speed, 10, 10)
                    move_up = not any(player.colliderect(pygame.Rect(m[0], m[1], m[2], m[3])) for m in maze.maze_walls)
                    if move_up:
                        y -= speed

                if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
                    player = pygame.Rect(x, y + speed, 10, 10)
                    move_down = not any(player.colliderect(pygame.Rect(m[0], m[1], m[2], m[3])) for m in maze.maze_walls)
                    if move_down:
                        y += speed

                if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
                    player = pygame.Rect(x - speed, y, 10, 10)
                    move_left = not any(player.colliderect(pygame.Rect(m[0], m[1], m[2], m[3])) for m in maze.maze_walls)
                    if move_left:
                        x -= speed

                if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
                    player = pygame.Rect(x + speed, y, 10, 10)
                    move_right = not any(player.colliderect(pygame.Rect(m[0], m[1], m[2], m[3])) for m in maze.maze_walls)
                    if move_right:
                        x += speed

                # Check if player has reached the goal
                if goal.colliderect((x, y, 10, 10)):
                    victory = True

                # Draw the screen
                maze.draw(screen, color, goal)
                text = draw_time(start, pause_time)
                pygame.draw.rect(screen, (255, 100, 0), pygame.Rect(x, y, 10, 10))
                screen.blit(text[0], (700, 15))

            if victory:
                screen.fill((0, 0, 0))
                time_text = font1.render("Time Taken: " + text[1], True, (255, 255, 255))
                victory_text = font2.render("VICTORY!", True, (255, 255, 255))
                reset = font3.render("(Press Enter to Start New Game)", True, (255, 255, 255))
                screen.blit(victory_text, (468 - (victory_text.get_width() // 2), 328 - (victory_text.get_height() // 2)))
                screen.blit(time_text, (468 - (time_text.get_width() // 2), 248 + victory_text.get_height()))
                screen.blit(reset, (468 - (reset.get_width() // 2), 248 + victory_text.get_height() + time_text.get_height()))

            clock.tick(60)
            pygame.display.flip()

if __name__ == "__main__":
    main()
