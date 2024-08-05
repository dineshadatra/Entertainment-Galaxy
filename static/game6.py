import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 30

# Setup display
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Quiz Game')
font = pygame.font.Font(None, FONT_SIZE)

# Questions and answers
questions = [
    {
        "question": "What is the capital of France?",
        "answers": ["Paris", "London", "Berlin", "Rome"],
        "correct_answer": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "answers": ["Mars", "Jupiter", "Saturn", "Venus"],
        "correct_answer": "Mars"
    },
    {
        "question": "What is the largest mammal in the world?",
        "answers": ["Elephant", "Blue Whale", "Giraffe", "Hippo"],
        "correct_answer": "Blue Whale"
    }
]

# Selected cells
selected_cells = []

def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    window.blit(text_surface, text_rect)

def draw_buttons(answers):
    button_height = 50
    button_width = 400
    button_x = WINDOW_WIDTH // 2
    button_start_y = WINDOW_HEIGHT // 2

    for idx, answer in enumerate(answers):
        button_y = button_start_y + idx * (button_height + 20)
        pygame.draw.rect(window, WHITE, (button_x - button_width // 2, button_y, button_width, button_height))
        draw_text(answer, button_x, button_y + button_height // 2, BLACK)  # Changed text color to black

def display_question(question_data):
    window.fill(BLACK)
    draw_text(question_data["question"], WINDOW_WIDTH // 2, 100)
    draw_buttons(question_data["answers"])
    pygame.display.flip()

def check_answer(question_data, selected_answer):
    return question_data["correct_answer"] == selected_answer

def display_result(result):
    window.fill(BLACK)
    draw_text(result, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds before continuing to the next question

# Game loop
running = True
current_question = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(selected_cells) == 0:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                button_height = 50
                button_width = 400
                button_x = WINDOW_WIDTH // 2
                button_start_y = WINDOW_HEIGHT // 2
                for idx, _ in enumerate(questions[current_question]["answers"]):
                    button_y = button_start_y + idx * (button_height + 20)
                    if button_x - button_width // 2 <= mouse_x <= button_x + button_width // 2 and \
                            button_y <= mouse_y <= button_y + button_height:
                        selected_cells.append(questions[current_question]["answers"][idx])
                        if check_answer(questions[current_question], selected_cells[0]):
                            display_result("Correct!")
                        else:
                            display_result("Incorrect!")
                        break
            else:
                selected_cells.clear()
                current_question += 1
                if current_question >= len(questions):
                    running = False

    if current_question < len(questions):
        display_question(questions[current_question])
    else:
        running = False

pygame.quit()
sys.exit()
