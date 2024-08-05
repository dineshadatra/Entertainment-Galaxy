import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 400
HEIGHT = 400
FPS = 70
FONT_SIZE = 40
WHITE = (0, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Guess")
clock = pygame.time.Clock()

# List of words to guess
word_list1 = ["apple", "banana", "guava", "grapes", "pineapple", "pomegranate", "mango", "custardapple", "orange"]
word_list2=["potato","tomato","cabbage","onion","carrot","beetroot","raddish","banana"]
word_list3=["dhoni","kohli","rohit","klrahul","bumrah","pandya","raina","jadeja","umeshyadav","jaiswal"]


# Function to display text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Function to draw the hangman
def draw_hangman(stage):
    if stage == 1:
        pygame.draw.circle(screen, BLACK, (400, 200), 40, 3)
    elif stage == 2:
        pygame.draw.line(screen, BLACK, (400, 240), (400, 400), 3)
    elif stage == 3:
        pygame.draw.line(screen, BLACK, (400, 280), (350, 350), 3)
    elif stage == 4:
        pygame.draw.line(screen, BLACK, (400, 280), (450, 350), 3)
    elif stage == 5:
        pygame.draw.line(screen, BLACK, (400, 400), (350, 500), 3)
    elif stage == 6:
        pygame.draw.line(screen, BLACK, (400, 400), (450, 500), 3)
    elif stage == 7:
        pygame.draw.line(screen, BLACK, (400, 320), (350, 370), 3)
    elif stage == 8:
        pygame.draw.line(screen, BLACK, (400, 320), (450, 370), 3)

# Main loop
def main():
    running = True

    # Select a random word
    word_list = random.choice([word_list1,word_list2,word_list3])
    
        
    target_word=random.choice(word_list)
    
    guessed_letters = set()
    incorrect_guesses = 0

    while running:
        screen.fill(WHITE)
        if word_list==word_list1:
            draw_text("HINT:Name of a fruit", pygame.font.Font(None, 40), BLACK, WIDTH // 2, 50)
        elif word_list==word_list2:
            draw_text("HINT:Name of a vegetable", pygame.font.Font(None, 40), BLACK, WIDTH // 2, 50)
        elif word_list==word_list3:
            draw_text("HINT:Name of a cricketer", pygame.font.Font(None, 40), BLACK, WIDTH // 2, 50)
            
       

        # Display the word with blanks for missing letters
        display_word = ""
        for letter in target_word:
            if letter in guessed_letters:
                display_word += letter + " "
            else:
                display_word += "_ "
        draw_text(display_word, pygame.font.Font(None, FONT_SIZE), BLACK, WIDTH // 2, HEIGHT // 2)

        # Draw the hangman
        draw_hangman(incorrect_guesses)

        # Check if player won
        if all(letter in guessed_letters for letter in target_word):
            draw_text("Congratulations! You guessed the word!", pygame.font.Font(None, 40), RED, WIDTH // 3, HEIGHT - 100)
            pygame.display.update()
            pygame.time.wait(3000)
            break

        # Check if player lost
        if incorrect_guesses == 8:
            draw_text("Sorry, you lost. The word was: " + target_word, pygame.font.Font(None, 40), RED, WIDTH // 3, HEIGHT - 100)
            pygame.display.update()
            pygame.time.wait(3000)
            break

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.key >= pygame.K_a and event.key <= pygame.K_z:
                    letter = chr(event.key)
                    if letter not in guessed_letters:
                        guessed_letters.add(letter)
                        if letter not in target_word:
                            incorrect_guesses += 1

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()