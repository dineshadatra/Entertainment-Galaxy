import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Paddle settings
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED = 6

# Ball settings
BALL_RADIUS = 10
BALL_SPEED_X = 4
BALL_SPEED_Y = -4

# Brick settings
BRICK_WIDTH = 75
BRICK_HEIGHT = 30
BRICK_COLS = 10
BRICK_ROWS = 6
BRICK_PADDING = 5

# Define Paddle class
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dx):
        self.rect.x += dx
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - PADDLE_WIDTH:
            self.rect.x = SCREEN_WIDTH - PADDLE_WIDTH

    def draw(self):
        pygame.draw.rect(SCREEN, BLUE, self.rect)

# Define Ball class
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y

    def draw(self):
        pygame.draw.circle(SCREEN, RED, (self.rect.x + BALL_RADIUS, self.rect.y + BALL_RADIUS), BALL_RADIUS)

# Define Brick class
class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = random.choice([GREEN, BLUE, RED])

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)
        pygame.draw.rect(SCREEN, BLACK, self.rect, 2)

# Create brick wall
def create_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
            y = row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_PADDING
            bricks.append(Brick(x, y))
    return bricks

# Main game function
def game():
    clock = pygame.time.Clock()
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()

    running = True
    while running:
        SCREEN.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-PADDLE_SPEED)
        if keys[pygame.K_RIGHT]:
            paddle.move(PADDLE_SPEED)

        ball.move()
        
        if ball.rect.colliderect(paddle.rect):
            ball.speed_y = -ball.speed_y
        
        for brick in bricks[:]:
            if ball.rect.colliderect(brick.rect):
                ball.speed_y = -ball.speed_y
                bricks.remove(brick)
                break

        if ball.rect.bottom >= SCREEN_HEIGHT:
            running = False
        
        paddle.draw()
        ball.draw()
        for brick in bricks:
            brick.draw()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Run the game
if __name__ == "__main__":
    game()
