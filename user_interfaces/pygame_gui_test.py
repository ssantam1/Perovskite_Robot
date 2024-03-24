import pygame
import sys
from pygame.locals import QUIT, KEYDOWN, K_RETURN, K_BACKSPACE, K_TAB

def handle_input_screen():
    # Initialize Pygame
    pygame.init()

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Screen dimensions
    SCREEN_WIDTH, SCREEN_HEIGHT = 400, 300

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("User Input")

    # Fonts
    font = pygame.font.Font(None, 32)

    # Text input boxes
    input_box1 = pygame.Rect(50, 100, 200, 32)
    input_box2 = pygame.Rect(50, 150, 200, 32)
    text1 = ''
    text2 = ''
    text_color = BLACK
    active1 = False
    active2 = False

    # Button
    button = pygame.Rect(270, 100, 80, 32)
    button_color = (0, 255, 0)
    button_text = font.render("Submit", True, WHITE)

    # Main loop
    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if active1:
                    if event.key == K_RETURN or event.key == K_TAB:
                        active1 = False
                        active2 = True
                    elif event.key == K_BACKSPACE:
                        text1 = text1[:-1]
                    elif len(text1) < 15:
                        text1 += event.unicode
                elif active2:
                    if event.key == K_RETURN or event.key == K_TAB:
                        active2 = False
                        # Submit button pressed
                        process_input(text1, text2)
                        text1 = ''
                        text2 = ''
                    elif event.key == K_BACKSPACE:
                        text2 = text2[:-1]
                    elif len(text2) < 15:
                        text2 += event.unicode

            # Check if mouse clicked on input boxes
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active1 = True
                    active2 = False
                elif input_box2.collidepoint(event.pos):
                    active1 = False
                    active2 = True
                else:
                    active1 = False
                    active2 = False
                text_color = BLACK if active1 or active2 else BLACK

        # Draw input boxes
        pygame.draw.rect(screen, text_color, input_box1, 2)
        input_surface1 = font.render(text1, True, BLACK)
        screen.blit(input_surface1, (input_box1.x + 5, input_box1.y + 5))

        pygame.draw.rect(screen, text_color, input_box2, 2)
        input_surface2 = font.render(text2, True, BLACK)
        screen.blit(input_surface2, (input_box2.x + 5, input_box2.y + 5))

        # Draw button
        pygame.draw.rect(screen, button_color, button)
        screen.blit(button_text, (275, 105))

        pygame.display.flip()

def process_input(text1, text2):
    # Your processing code here
    print("User input 1:", text1)
    print("User input 2:", text2)
    # For example, you can pass the text to another function or perform calculations

# Call the function to handle the input screen
handle_input_screen()
