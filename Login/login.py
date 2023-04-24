import pygame

pygame.init()

WINDOW_SIZE = (800, 600)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('User Login/Register')

font = pygame.font.SysFont(None, 32)

# Username input
username = ''
username_rect = pygame.Rect(300, 200, 200, 32)
username_active = False

# Password input
password = ''
password_rect = pygame.Rect(300, 300, 200, 32)
password_active = False

# Buttons
register_rect = pygame.Rect(300, 400, 200, 50)
login_rect = pygame.Rect(300, 500, 200, 50)

def draw_text_input(screen, text, rect, active):
    # Draw the input field rectangle
    pygame.draw.rect(screen, WHITE, rect, 2)

    # Render the input field text
    text_surface = font.render(text, True, WHITE)

    # Position the input field text
    text_rect = text_surface.get_rect()
    text_rect.x = rect.x + 5
    text_rect.y = rect.y + 5

    # Blit the input field text to the screen
    screen.blit(text_surface, text_rect)

    # If the input field is active, draw the cursor
    if active:
        cursor_rect = pygame.Rect(text_rect.x + text_rect.width, text_rect.y, 2, text_rect.height)
        pygame.draw.rect(screen, WHITE, cursor_rect)
    
def draw_buttons(screen):
    # Draw the register button
    pygame.draw.rect(screen, GRAY, register_rect)
    register_text = font.render('Register', True, BLACK)
    register_text_rect = register_text.get_rect()
    register_text_rect.center = register_rect.center
    screen.blit(register_text, register_text_rect)

    # Draw the login button
    pygame.draw.rect(screen, GRAY, login_rect)
    login_text = font.render('Login', True, BLACK)
    login_text_rect = login_text.get_rect()
    login_text_rect.center = login_rect.center
    screen.blit(login_text, login_text_rect)

import json

def save_user_data(username, password):
    # Load existing user data or create a new list
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
    except:
        users = []

    # Append the new user data
    user_data = {'username': username, 'password': password}
    users.append(user_data)

    # Save the user data to the file
    with open('users.json', 'w') as file:
        json.dump(users, file)

def handle_events():
    global username, password, username_active, password_active

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the username input field was clicked
            if username_rect.collidepoint(event.pos):
                username_active = True
            else:
                username_active = False

            # Check if the password input field was clicked
            if password_rect.collidepoint(event.pos):
                password_active = True
            else:
                password_active = False

            # Check if the register button was clicked
            if register_rect.collidepoint(event.pos):
                if username != '' and password != '':
                    save_user_data(username, password)
                    username = ''
                    password = ''
                else:
                    print('Please enter a username and password')

            # Check if the login button was clicked
            if login_rect.collidepoint(event.pos):
                print('Login not implemented yet')

        if event.type == pygame.KEYDOWN:
            # Handle input field typing
            if username_active:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
            elif password_active:
                if event.key == pygame.K_BACKSPACE:
                    password = password[:-1]
                else:
                    password += event.unicode

def draw_screen(screen):
    screen.fill(BLACK)

    # Draw the input fields
    draw_text_input(screen, username, username_rect, username_active)
    draw_text_input(screen, password, password_rect, password_active)

    # Draw the buttons
    draw_buttons(screen)

    pygame.display.update()

clock = pygame.time.Clock()

while True:
    handle_events()
    draw_screen(screen)
    clock.tick(60)
