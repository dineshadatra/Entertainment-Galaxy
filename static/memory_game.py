import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Card Matching Game')

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Game variables
cards = []
card_values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] * 2  # Duplicated for pairs
card_size = 100
padding = 10
selected_cards = []
matched_pairs = 0
total_pairs = len(card_values) // 2

# Create card objects
class Card:
    def __init__(self, value, rect):
        self.value = value
        self.rect = rect
        self.face_down = True
        self.color = BLUE # Default color when face down

# Create grid of cards
def create_cards():
    global cards, card_values
    cards.clear()
    random.shuffle(card_values)
    num_cols = 4
    num_rows = 4
    card_width = card_size
    card_height = card_size

    for row in range(num_rows):
        for col in range(num_cols):
            x = col * (card_width + padding) + padding
            y = row * (card_height + padding) + padding
            rect = pygame.Rect(x, y, card_width, card_height)
            value = card_values.pop()
            card = Card(value, rect)
            cards.append(card)

# Draw cards on screen
def draw_cards():
    for card in cards:
        if card.face_down:
            pygame.draw.rect(screen, card.color, card.rect)
        else:
            pygame.draw.rect(screen, WHITE, card.rect)
            font = pygame.font.Font(None, 36)
            text = font.render(card.value, True, BLACK)
            text_rect = text.get_rect(center=card.rect.center)
            screen.blit(text, text_rect)

# Check for card clicks
def check_card_click(pos):
    for card in cards:
        if card.rect.collidepoint(pos) and card.face_down:
            card.face_down = False
            selected_cards.append(card)
            break

# Check if two selected cards match
def check_matching_cards():
    global selected_cards, matched_pairs
    if len(selected_cards) == 2:
        if selected_cards[0].value == selected_cards[1].value:
            selected_cards[0].color = GREEN
            selected_cards[1].color = GREEN
            matched_pairs += 1
        else:
            pygame.time.wait(50)  # Reduced wait time to 0.5 seconds
            selected_cards[0].face_down = True
            selected_cards[1].face_down = True
        selected_cards = []

# Display time taken to complete the game
def display_time_taken(time_taken):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 72)
    text = font.render(f'Time Taken: {time_taken:.2f} seconds', True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # Display time for 3 seconds

# Initialize game
create_cards()

# Main loop
running = True
clock = pygame.time.Clock()
start_time = time.time()  # Track start time

while running:
    dt = clock.tick(60) / 1000.0

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                check_card_click(event.pos)

    # Update game state
    check_matching_cards()

    # Draw
    screen.fill(WHITE)
    draw_cards()

    pygame.display.flip()

    # Check if all pairs are matched
    if matched_pairs == total_pairs:
        end_time = time.time()  # Track end time
        time_taken = end_time - start_time
        display_time_taken(time_taken)
        running = False

# Quit Pygame
pygame.quit()
