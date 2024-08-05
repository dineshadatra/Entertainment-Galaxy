import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15
PADDLE_SPEED = 10
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

# Setup display
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Pong Game')
clock = pygame.time.Clock()

# Paddle positions
left_paddle_y = (WINDOW_HEIGHT - PADDLE_HEIGHT) // 2
right_paddle_y = (WINDOW_HEIGHT - PADDLE_HEIGHT) // 2

# Ball position and velocity
ball_x = WINDOW_WIDTH // 2
ball_y = WINDOW_HEIGHT // 2
ball_vel_x = BALL_SPEED_X
ball_vel_y = BALL_SPEED_Y

def draw_paddles():
    pygame.draw.rect(window, WHITE, (10, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(window, WHITE, (WINDOW_WIDTH - 20, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

def draw_ball():
    pygame.draw.ellipse(window, WHITE, (ball_x - BALL_SIZE // 2, ball_y - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE))

def handle_collisions():
    global ball_vel_x, ball_vel_y
    # Ball collision with top and bottom walls
    if ball_y - BALL_SIZE // 2 <= 0 or ball_y + BALL_SIZE // 2 >= WINDOW_HEIGHT:
        ball_vel_y = -ball_vel_y

    # Ball collision with paddles
    if (ball_x - BALL_SIZE // 2 <= 20 and left_paddle_y < ball_y < left_paddle_y + PADDLE_HEIGHT) or \
       (ball_x + BALL_SIZE // 2 >= WINDOW_WIDTH - 20 and right_paddle_y < ball_y < right_paddle_y + PADDLE_HEIGHT):
        ball_vel_x = -ball_vel_x

def reset_ball():
    global ball_x, ball_y, ball_vel_x, ball_vel_y
    ball_x = WINDOW_WIDTH // 2
    ball_y = WINDOW_HEIGHT // 2
    ball_vel_x = BALL_SPEED_X if ball_vel_x < 0 else -BALL_SPEED_X
    ball_vel_y = BALL_SPEED_Y

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys
    keys = pygame.key.get_pressed()
    
    # Left paddle movement
    if keys[pygame.K_w] and left_paddle_y > 0:
        left_paddle_y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
        left_paddle_y += PADDLE_SPEED
    
    # Right paddle movement
    if keys[pygame.K_UP] and right_paddle_y > 0:
        right_paddle_y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle_y < WINDOW_HEIGHT - PADDLE_HEIGHT:
        right_paddle_y += PADDLE_SPEED

    # Update ball position
    ball_x += ball_vel_x
    ball_y += ball_vel_y

    # Handle collisions
    handle_collisions()

    # Check if ball is out of bounds
    if ball_x - BALL_SIZE // 2 <= 0 or ball_x + BALL_SIZE // 2 >= WINDOW_WIDTH:
        reset_ball()

    # Draw everything
    window.fill(BLACK)
    draw_paddles()
    draw_ball()
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
