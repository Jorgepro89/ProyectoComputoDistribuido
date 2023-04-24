import math
import sys
import socket
import os
import pygame

os.environ["SDL_AUDIODRIVER"] = "dummy"

HOST = sys.argv[1]
PORT = 15000

# Define colors
RED = (255, 65, 54)
GREEN = (46, 204, 64)
BLUE = (0, 116, 217)
ORANGE = (255, 133, 27)
PURPLE = (177, 13, 201)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)
GRAY = (128, 128, 128)
LIGHT_GRAY = (211, 211, 211)
DARK_RED = (139, 0, 0)
DARK_GREEN = (0, 100, 0)
DARK_BLUE = (0, 0, 139)
ORANGE_LIGHT = (255, 179, 117)
LIGHT_PURPLE = (231, 67, 255)
LIGHT_GREEN = (86, 244, 104)


word = "locomotora"

class Letra:
    def __init__(self,x1,y1,width,height,text,textX,textY):
        self.x1 = x1
        self.y1 = y1
        self.width = width
        self.height = height
        self.rectangulo = pygame.Rect(x1,y1,width,height)
        self.text = text
        self.textX = textX
        self.textY = textY
        self.activo = True

class Button:
    def __init__(self, x, y, width, height, color, text_color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text_color = text_color
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.gradient_top = tuple([min(int(c * 1.2), 255) for c in self.color])
        self.gradient_bottom = tuple([min(int(c * 1.5), 255) for c in self.color])
        self.border_color = tuple([max(int(c * 0.8), 0) for c in self.color])
        self.clicked_color = tuple([max(int(c * 0.8), 0) for c in self.gradient_top])
        self.clicked = False

    def draw(self, surface):
        # Draw the button background with gradient
        surface.fill(self.gradient_top, self.rect)
        pygame.draw.rect(surface, self.gradient_bottom, self.rect.inflate(-5, -5),border_radius=10)
        pygame.draw.rect(surface, self.color, self.rect.inflate(-10, -10))

        # Draw the button border
        pygame.draw.rect(surface, self.border_color, self.rect, 5)

        # Render the button text
        text_surface = self.font.render(self.text, True, self.text_color)

        # Center the text on the button
        text_rect = text_surface.get_rect(center=self.rect.center)

        # Blit the text onto the surface
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                self.color = self.clicked_color
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.clicked:
                self.clicked = False
                self.color = self.gradient_top
                return True
        return False

class InputField:
    def __init__(self, x, y, width, height, label, max_chars):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.hiddenText = ""
        self.max_chars = max_chars
        self.name = label
        self.label = font.render(label, True, DARK_BLUE)
        self.label_rect = self.label.get_rect(topleft=(x, y - height//2))
        self.font = pygame.font.Font(None, 28)
        self.active = False  # added to keep track of focus

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.hiddenText = self.hiddenText[:-1]
            elif event.unicode.isalnum() and len(self.text) < self.max_chars:
                self.text += event.unicode
                self.hiddenText += '*'

    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, LIGHT_GRAY, self.rect, border_radius=10)
        else:
            pygame.draw.rect(surface, WHITE, self.rect, border_radius=10)
        if self.name == "Password":
            text = self.font.render(self.hiddenText, True, BLACK)
        else:
            text = self.font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(self.label, self.label_rect)
        surface.blit(text, text_rect)

class Alert:
    def __init__(self, text):
        self.font = pygame.font.Font(None, 40)
        self.text = self.font.render(text, True, (255, 255, 255))
        self.rect = self.text.get_rect(center=(screen_width // 2, screen_height // 4))
        self.rect.inflate_ip(0, 20)  # add 20 pixels of padding to top and bottom

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect, border_radius=10)
        screen.blit(self.text, self.rect)


def drawHead():
    pygame.draw.circle(screen, "blue", [424, 135], 15)

def drawBody():
    pygame.draw.line(screen, "blue", [424, 150], [424, 200], 5)
    
def drawLegs():
    pygame.draw.line(screen, "blue", [424, 200], [444, 220], 5)
    pygame.draw.line(screen, "blue", [424, 200], [404, 220], 5)

def drawArms():
    pygame.draw.line(screen, "blue", [424, 160], [444, 185], 5)
    pygame.draw.line(screen, "blue", [424, 160], [404, 185], 5)
    
def drawDead():
    pygame.draw.line(screen, "red", [415, 130], [421, 140], 1)
    pygame.draw.line(screen, "red", [415, 140], [421, 130], 1)
    pygame.draw.line(screen, "red", [433, 130], [427, 140], 1)
    pygame.draw.line(screen, "red", [433, 140], [427, 130], 1)

s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((HOST, PORT))
    print('Connected to', HOST, 'on port', PORT)
    
    # pygame setup
    pygame.init()
    pygame.font.init()
    lettersFont = pygame.font.SysFont("Arial", 20)
    timerFont = pygame.font.SysFont("Arial", 20)
    screen_width = 730
    screen_height = 500
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Ahorcado")
    clock = pygame.time.Clock()
    # 
    # pygame start screen
    start = True
    login = False
    register = False
    main = False
    screen.fill(BLUE)

    # Create the title text
    font = pygame.font.Font(None, 64)
    title_text = font.render("Ahorcado", True, WHITE)
    title_rect = title_text.get_rect(center=(screen_width//2, 100))

    # Create the buttons
    button_width = 200
    button_height = 50
    button_margin = 30
    button_x = (screen_width - button_width) // 2
    button_y = (screen_height - button_height - button_margin) // 2
    loginButton = Button(button_x, button_y, button_width, button_height, ORANGE, WHITE, "Login")
    button_y += button_height + button_margin
    registerButton = Button(button_x, button_y, button_width, button_height, PURPLE, WHITE, "Register")
    pygame.display.update()
    while start:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
            else:
                # Handle button events
                if loginButton.handle_event(event):
                    login = True
                if registerButton.handle_event(event):
                    register = True

        # Login Screen
        if login:
            # Set up the font
            font = pygame.font.Font(None, 32)
        
            input_width = 300
            input_height = 50
            input_margin = 50
            input_x = (screen_width - input_width) // 2
            input_y = (screen_height - 2 * input_height - input_margin) // 2
        
            usernameInput = InputField(input_x, input_y, input_width, input_height, "Username",10)
            passwordInput = InputField(input_x, input_y + input_height + input_margin, input_width, input_height, "Password",10)
        
            # Set up the button
            button_width = 200
            button_height = 50
            button_x = (screen_width - button_width) // 2
            button_y = passwordInput.rect.bottom + input_height
        
            button = Button(button_x, button_y, button_width, button_height, GREEN, WHITE, "LOGIN")
        
            #
            backButton = Button(10, 30, 100, 50, RED, BLACK, "atrás")
        
            # Set up the title
            font = pygame.font.Font(None, 48)
            title_label = font.render("Login", True, BLACK)
            title_label_rect = title_label.get_rect(center=(screen_width//2, 50))
            
            alert = Alert("Información Incorrecta")
            alert2 = Alert("Llena ambos campos")
            
        while login:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start = False
                    login = False
                else:
                    usernameInput.handle_event(event)
                    passwordInput.handle_event(event)
                    if backButton.handle_event(event):
                        login = False
                    if button.handle_event(event):
                        print(usernameInput.text, passwordInput.text)
                        if usernameInput.text != "" and passwordInput.text != "":
                            credentials = "L" + usernameInput.text + " " + passwordInput.text
                            enced = credentials.encode("utf-8")
                            s.sendall(enced)
                            data = s.recv(1024)
                            decoded_data = data.decode('utf-8')
                            if decoded_data[0] == "C":
                                login = False
                                start = False
                                main = True
                            else:
                                alert.draw(screen)
                                pygame.display.update()
                                pygame.time.delay(3000)
                        else:
                            alert2.draw(screen)
                            pygame.display.update()
                            pygame.time.delay(3000)
                            

            # Draw the background
            screen.fill(ORANGE_LIGHT)

            # Draw the title
            screen.blit(title_label, title_label_rect)

            # Draw the input fields
            usernameInput.draw(screen)
            passwordInput.draw(screen)

            # Draw the button
            button.draw(screen)
            backButton.draw(screen)

            pygame.display.flip()
        #
        # Register Screen
        if register:
            # Set up the font
            font = pygame.font.Font(None, 32)
        
            input_width = 300
            input_height = 50
            input_margin = 50
            input_x = (screen_width - input_width) // 2
            input_y = (screen_height - 2 * input_height - input_margin) // 2
        
            usernameInput = InputField(input_x, input_y, input_width, input_height, "Username",10)
            passwordInput = InputField(input_x, input_y + input_height + input_margin, input_width, input_height, "Password",10)
        
            # Set up the button
            button_width = 200
            button_height = 50
            button_x = (screen_width - button_width) // 2
            button_y = passwordInput.rect.bottom + input_height
        
            button = Button(button_x, button_y, button_width, button_height, GREEN, WHITE, "REGISTER")
        
            backButton = Button(10, 30, 100, 50, RED, BLACK, "atrás")
        
            # Set up the title
            font = pygame.font.Font(None, 48)
            title_label = font.render("Register", True, BLACK)
            title_label_rect = title_label.get_rect(center=(screen_width//2, 50))
        
            alert = Alert("Usuario ya Existe")
            alert2 = Alert("Llena ambos campos")
        
        while register:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start = False
                    register = False
                else:
                    usernameInput.handle_event(event)
                    passwordInput.handle_event(event)
                    if backButton.handle_event(event):
                        register = False
                    if button.handle_event(event):
                        print(usernameInput.text, passwordInput.text)
                        if usernameInput.text != "" and passwordInput.text != "":
                            credentials = "R" + usernameInput.text + " " + passwordInput.text
                            enced = credentials.encode("utf-8")
                            s.sendall(enced)
                            data = s.recv(1024)
                            decoded_data = data.decode('utf-8')
                            if decoded_data[0] == "C":
                                register = False
                                start = False
                                main = True
                            else:
                                alert.draw(screen)
                                pygame.display.update()
                                pygame.time.delay(3000)
                        else:
                            alert2.draw(screen)
                            pygame.display.update()
                            pygame.time.delay(3000)
                        

            # Draw the background
            screen.fill(LIGHT_PURPLE)

            # Draw the title
            screen.blit(title_label, title_label_rect)

            # Draw the input fields
            usernameInput.draw(screen)
            passwordInput.draw(screen)

            # Draw the button
            button.draw(screen)
            backButton.draw(screen)

            pygame.display.flip()


        #

        # Draw the background
        screen.fill(BLUE)

        # Draw the title
        screen.blit(title_text, title_rect)

        # Draw the buttons
        loginButton.draw(screen)
        registerButton.draw(screen)

        # Update the display
        pygame.display.flip()

        # Set the frame rate
        #clock.tick(60)
       
    #

    # Main Screen
    jugar = False
    buscando = False
    info = False
    esperar = False
    resultado = False
    comoJugar= False
    puntajes = False

    if main:
        # Define title properties
        title_font = pygame.font.SysFont(None, 64)
        title_text = title_font.render('Ahorcado', True, BLACK)
        title_x = (screen_width - title_text.get_width()) / 2
        title_y = 70
    
        # Define button properties
        button_width = 150
        button_height = 50
        button_padding = 20
        button_x = (screen_width - button_width) / 2
        button_y = 150
        button_color = YELLOW
        button_text_color = BLACK
    
        # Create buttons
        jugarButton = Button(button_x, button_y, button_width, button_height, button_color, button_text_color, "Jugar")
        comojugarButton = Button(button_x, button_y + button_height + button_padding, button_width, button_height, button_color, button_text_color, "Como Jugar")
        puntajesButton = Button(button_x, button_y + 2 * (button_height + button_padding), button_width, button_height, button_color, button_text_color, "Puntajes")
        button_color = RED
        salirButton = Button(button_x, button_y + 3 * (button_height + button_padding), button_width, button_height, button_color, button_text_color, "Salir")

    # Game loop
    while main:
        mainActiveMsg = "Main"
        enmam = mainActiveMsg.encode("utf-8")
        s.sendall(enmam)
        
        data = s.recv(1024)
        decoded_data = data.decode('utf-8')
        if decoded_data[0] != 'e':
            numButton = Button(10, 30, 100, 30, PINK, BLACK, decoded_data)
            #numButton.draw(screen)
            pygame.display.update()
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
            # Handle button clicks
            if jugarButton.handle_event(event):
                buscando = True
                info = False
                jugar = False
            if comojugarButton.handle_event(event):
                comoJugar = True
            if puntajesButton.handle_event(event):
                puntajes = True
            if salirButton.handle_event(event) :
                main = False
        if buscando:
            font = pygame.font.Font(None, 40)

            title_surface = font.render("Buscando Oponente...", True, BLACK)
            title_rect = title_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 75))

            button_width = 100
            button_height = 50
            button_x = (screen.get_width() - button_width) // 2
            button_y = screen.get_height() // 2 + 75
            
            cancelButton = Button(button_x, button_y, button_width, button_height, RED, BLACK, "Cancel")
            cancelButton.draw(screen)

            # Loading variables
            loading_percent = 0
            loading_speed = 0.7  # Increase this number to make the loading faster
            while buscando:
                mainActiveMsg = "Buscando"
                enmam = mainActiveMsg.encode("utf-8")
                s.sendall(enmam)
                
                data = s.recv(1024)
                decoded_data = data.decode('utf-8')
                if decoded_data[0] == '!':
                    word = decoded_data[1:]
                    buscando = False
                    info = False
                    jugar = True
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        buscando = False
                        jugar = False
                        main = False
                    else:
                        if cancelButton.handle_event(event):
                            mainActiveMsg = "Cancel"
                            enmam = mainActiveMsg.encode("utf-8")
                            s.sendall(enmam)
                            
                            data = s.recv(1024)
                            decoded_data = data.decode('utf-8')
                            buscando = False

                screen.fill(DARK_GREEN)
                cancelButton.draw(screen)
                screen.blit(title_surface, title_rect)
                # Draw the loading circle
                circle_center = (screen_width // 2, screen_height // 2)
                circle_radius = 50
                circle_width = 5
                loading_angle = loading_percent * 3.6  # Convert percent to degrees
                pygame.draw.circle(screen, WHITE, circle_center, circle_radius, circle_width)
                pygame.draw.arc(screen, BLUE, (circle_center[0]-circle_radius, circle_center[1]-circle_radius, circle_radius*2, circle_radius*2), math.radians(-90), math.radians(loading_angle - 90), circle_width)
            
                # Update the loading percent
                loading_percent += loading_speed
                if loading_percent > 100:
                    loading_percent = 0
                
                pygame.display.update()
        if info:
            screen.fill(BLUE)
            # set up fonts and colors
            font = pygame.font.Font(None, 30)
            font_bold = pygame.font.Font(None, 40)
            white = (255, 255, 255)
            
            # draw the title at the top
            title = font_bold.render("Match Found", True, BLACK)
            title_rect = title.get_rect(center=(365, 50))
            screen.blit(title, title_rect)
            
            
            # set up the table data
            player1Name = "player1"
            player1Record = "0-0"
            player2Name = "player2"
            player2Record = "0-0"
            
            table_data = [
                [player1Name, "vs", player2Name],
                [player1Record, "", player2Record],
            ]
            
            # draw the table
            table_width = 500
            table_height = 200
            table_x = (730 - table_width) // 2
            table_y = 100
            cell_width = table_width // 3
            cell_height = table_height // 2
            for i in range(len(table_data)):
                for j in range(len(table_data[i])):
                    cell_x = table_x + j * cell_width
                    cell_y = table_y + i * cell_height
                    cell_rect = pygame.Rect(cell_x, cell_y, cell_width, cell_height)
                    cell_text = font.render(table_data[i][j], True, white)
                    cell_text_rect = cell_text.get_rect(center=cell_rect.center)
                    if j == 1 and i == 1:
                        screen.blit(font.render(table_data[i][j], True, white), cell_text_rect)
                    else:
                        screen.blit(cell_text, cell_text_rect)
            
            # draw the text below the table
            bottom_text = font_bold.render("10", True, white)
            bottom_rect = bottom_text.get_rect(center=(365, 400))
            screen.blit(bottom_text, bottom_rect)
            
            # update the screen
            pygame.display.flip()
            
            # run the game loop
            startTime = 0
            startSpeed = 0.001
            look = 0
            while info:
                mainActiveMsg = "Buscando"
                enmam = mainActiveMsg.encode("utf-8")
                s.sendall(enmam)
                
                data = s.recv(1024)
                decoded_data = data.decode('utf-8')
                if look==0:
                    if decoded_data[0] == '!':
                        look = 1
                        playersInfo = decoded_data.split()
                        player1Name = playersInfo[0][1:]
                        player1Win = playersInfo[2]
                        player1Lose = playersInfo[3]
                        player2Name = playersInfo[4]
                        player2Win = playersInfo[6]
                        player2Lose = playersInfo[7]
                        # set up the table data
                        player1Record = player1Win+"-"+player1Lose
                        player1Record = player2Win+"-"+player2Lose
                    elif decoded_data[0] == 'p':
                        info = False
                        jugar = True
                        break
                        
                table_data = [
                    [player1Name, "vs", player2Name],
                    [player1Record, "", player2Record],
                ]
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        info = False
                        jugar = False
                        main = False
                screen.fill(BLUE)
                screen.blit(title_text, title_rect)
                for i in range(len(table_data)):
                    for j in range(len(table_data[i])):
                        cell_x = table_x + j * cell_width
                        cell_y = table_y + i * cell_height
                        cell_rect = pygame.Rect(cell_x, cell_y, cell_width, cell_height)
                        cell_text = font.render(table_data[i][j], True, white)
                        cell_text_rect = cell_text.get_rect(center=cell_rect.center)
                        if j == 1 and i == 1:
                            screen.blit(font.render(table_data[i][j], True, white), cell_text_rect)
                        else:
                            screen.blit(cell_text, cell_text_rect)
                # draw the text below the table
                text = str(3- int(startTime))
                font_bold = pygame.font.Font(None, 48)
                bottom_text = font_bold.render(text, True, BLACK)
                bottom_rect = bottom_text.get_rect(center=(365, 350))
                screen.blit(bottom_text, bottom_rect)
                startTime += startSpeed
                
                if startTime>3:
                    info = False
                    jugar = True
                else:
                    # update the screen
                    pygame.display.flip()
        if jugar:
            #Active Game
            pygame.draw.rect(screen, (255,0,0), (0, 0, 730, 75))
            pygame.draw.rect(screen, (255,255,0), (10, 10, 710, 55))
        
        
            pygame.draw.rect(screen, (0,255,0), (0, 75, 730, 175))
            pygame.draw.rect(screen, (255,255,0), (182, 85, 365, 155))
        
        
            pygame.draw.rect(screen, (0,0,255), (0, 250, 730, 125))
            pygame.draw.rect(screen, (255,255,0), (10, 260, 710, 105))
        
            pygame.draw.rect(screen, (50,50,50), (0, 375, 730, 125))
            pygame.draw.rect(screen, (255,255,50), (10, 385, 710, 50))
            pygame.draw.rect(screen, (255,255,50), (10, 440, 710, 50))
        
            pygame.display.update()
        
            letras = {}
        
            xPrimerLetra = 10
            yPrimerLetra = 385
        
            x = xPrimerLetra
            y = yPrimerLetra
        
            width = 50
            height = 50
            for i in range(97, 123):
                lerta = chr(i)
                pygame.draw.rect(screen,(0,255,255),(x,y,50,50))
                
                text_surface = lettersFont.render(chr(i), True, (0, 0, 0))
                # Get the dimensions of the text surface
                text_width = text_surface.get_width()
                text_height = text_surface.get_height()
                # Calculate the x and y coordinates to center the text in the rectangle
                text_x = (width - text_width) // 2 + x
                text_y = (height - text_height) // 2 + y
                # Blit the text surface onto the window surface at the correct coordinates
                screen.blit(text_surface, (text_x, text_y))
                letras[chr(i)] = Letra(x,y,50,50,text_surface,text_x,text_y)
        
                x += 55
                if i == 109:
                    x = xPrimerLetra
                    y = 440
                pygame.display.update()
        
            espacios = {}   
            letrasEspacios = [] 
            spaceWidth = (710-(len(word)-1)*5) // len(word)
            spaceHeight = spaceWidth
            if spaceHeight > 105:
                spaceHeight = 105
            x = 10 + (710-(spaceWidth*len(word)+(len(word)-1)*5))/2
            y = 260 + (105-spaceHeight)/2
        
            for i in range(0,len(word)):
                if word[i] in espacios:
                    espacios[word[i]].append(i)
                else:
                    espacios[word[i]] = [i]
                text_surface = lettersFont.render(word[i].upper(), True, (255, 255, 255))
                text_width = text_surface.get_width()
                text_height = text_surface.get_height()
                text_x = (spaceWidth - text_width) // 2 + x
                text_y = (spaceHeight - text_height) // 2 + y
                letrasEspacios.append((text_surface,(text_x,text_y)))
                pygame.draw.rect(screen,(10,20,30),(x,y,spaceWidth,spaceHeight))
                x += spaceWidth+5
                pygame.display.update()
            """
            for letra in espacios:
                for espacio in espacios[letra]:
                    screen.blit(letrasEspacios[espacio][0],(letrasEspacios[espacio][1][0],letrasEspacios[espacio][1][1]))
            """
        
            pygame.draw.line(screen, (60, 179, 113), [244, 240], [364, 240], 5)
            pygame.draw.line(screen, (60, 179, 113), [304, 240], [304, 85], 5)
            pygame.draw.line(screen, (60, 179, 113), [304, 85], [424, 85], 5)
            pygame.draw.line(screen, (60, 179, 113), [424, 85], [424, 120], 5)
            pygame.display.update()
                
            # Set up the timer
            timer_event = pygame.USEREVENT + 1
            pygame.time.set_timer(timer_event, 1000) # 1 second
            # Set up the timer variables
            time_elapsed = 0
            start_ticks = pygame.time.get_ticks()
        
            errors = 0
            aciertos = 0     
        while jugar:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main = False
                    jugar = False
                elif event.type == timer_event:
                    # Update the timer variables
                    time_elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for letra in letras:
                        if letras[letra].rectangulo.collidepoint(event.pos):
                            pygame.draw.rect(screen,(0,0,0),letras[letra].rectangulo)
                            text = lettersFont.render(letra, True, (50, 50, 50))
                            screen.blit(text,(letras[letra].textX,letras[letra].textY))
                            if letras[letra].activo==True:
                                if letra in espacios:
                                    for espacio in espacios[letra]:
                                        aciertos +=1
                                        screen.blit(letrasEspacios[espacio][0],(letrasEspacios[espacio][1][0],letrasEspacios[espacio][1][1]))
                                    if aciertos == len(word):
                                        resultado = True
                                        esperar = False
                                        jugar = False
                                else:
                                    errors +=1
                                    if errors == 1:
                                        drawHead()
                                    elif errors == 2:
                                        drawBody()
                                    elif errors == 3:
                                        drawLegs()
                                    elif errors == 4:
                                        drawArms()
                                    elif errors == 5:
                                        drawDead()
                                    elif errors == 6:
                                        resultado = True
                                        esperar = False
                                        jugar = False
                                    letras[letra].activo = False
                                    pygame.display.update()
                                letras[letra].activo = False
                            pygame.display.update()
                        
            # Draw the timer
            hours, remainder = divmod(time_elapsed, 3600)
            minutes, seconds = divmod(remainder, 60)
            timer_text = timerFont.render("{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), True, (0, 0, 0))
            pygame.draw.rect(screen, (255,255,0), (10, 10, 710, 55))
            timeText = timerFont.render("Time", True, (0, 0, 0))
            screen.blit(timeText, (355, 10))
            screen.blit(timer_text, (345, 30))
            score_text = timerFont.render(str(aciertos*100), True, (0, 0, 0))
            scoreText = timerFont.render("Puntuación", True, (0, 0, 0))
            screen.blit(scoreText, (50, 10))
            screen.blit(score_text, (80, 30))
            errors_text = timerFont.render(str(errors), True, (0, 0, 0))
            errorsText = timerFont.render("Errores", True, (0, 0, 0))
            screen.blit(errorsText, (620, 10))
            screen.blit(errors_text, (645, 30))

            # Update the screen
            pygame.display.flip()
        ##Game Active Ends
        # Wait Oponent
        if esperar:
            # Create the alert box
            ALERT_WIDTH = 500
            ALERT_HEIGHT = 300 # increased height to fit the table and button
            alert_rect = pygame.Rect((screen_width - ALERT_WIDTH) / 2, (screen_height - ALERT_HEIGHT) / 2, ALERT_WIDTH, ALERT_HEIGHT)
            pygame.draw.rect(screen, LIGHT_PURPLE, alert_rect, border_radius=10)
            # Add message to center of alert box
            message_font = pygame.font.SysFont(None, 56)
            message_text = message_font.render("Waiting for oponent...", True, BLACK)
            message_rect = message_text.get_rect(center=alert_rect.center)
            screen.blit(message_text, message_rect)
            #
            pygame.display.update()
        while esperar:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperar = False
                    resultado = False
                    main = False
            
        #Score
        if resultado:
            # Create the alert box
            ALERT_WIDTH = 500
            ALERT_HEIGHT = 300 # increased height to fit the table and button
            alert_rect = pygame.Rect((screen_width - ALERT_WIDTH) / 2, (screen_height - ALERT_HEIGHT) / 2, ALERT_WIDTH, ALERT_HEIGHT)
            pygame.draw.rect(screen, LIGHT_PURPLE, alert_rect, border_radius=10)
            
            # Create the title
            title_font = pygame.font.SysFont(None, 48, bold=True)
            title = title_font.render("Resultado!", True, BLACK)
            title_rect = title.get_rect(center=(alert_rect.centerx, alert_rect.top + 50))
            screen.blit(title, title_rect)
            
            # Create the table
            table_font = pygame.font.SysFont(None, 24)
            table_data = [("Palabra: "+word, ""),
                          ("{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds), ""),
                          (str(aciertos*100), "")]
            
            # Calculate table dimensions and position
            table_width = alert_rect.width - 40  # subtract 40 for the left and right margins
            table_height = table_font.get_height() * len(table_data)
            table_x = alert_rect.left + (alert_rect.width - table_width) / 2
            table_y = title_rect.bottom + 20 + ((alert_rect.height - title_rect.bottom - 20 - table_height - 30) / 2) # subtract 30 for the space between the table and the button
            
            # Draw the table data
            table_data_x = table_x
            table_data_y = table_y
            for j, row in enumerate(table_data):
                for i, cell in enumerate(row):
                    cell_text = table_font.render(cell, True, BLACK)
                    cell_rect = cell_text.get_rect(midtop=(table_data_x + table_width * (i + 0.5) / 2, table_data_y + table_font.get_height() * (j + 0.5)))
                    screen.blit(cell_text, cell_rect)
                table_data_y += 10

            
            # Create the button
            button_width = 100
            button_height = 40
            button_x = alert_rect.left + (alert_rect.width - button_width) / 2
            button_y = alert_rect.bottom - 20 - button_height
            button = Button(button_x, button_y, button_width, button_height, RED, BLACK, "Close")
            
            # Draw the button
            button.draw(screen)
            
            # Update display
            pygame.display.update()
        while resultado:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    resultado = False
                    main = False
                else:
                    if button.handle_event(event):
                        resultado = False
                        main = True
                        mainActiveMsg = "Final"
                        enmam = mainActiveMsg.encode("utf-8")
                        s.sendall(enmam)
                        data = s.recv(1024)
                        decoded_data = data.decode('utf-8')
                        break
            button.draw(screen)
            pygame.display.flip()
        #
        #Como Jugar
        if comoJugar:
            screen.fill(LIGHT_GRAY)
            # Set up the font and font size for the text
            font = pygame.font.Font(None, 48)
            
            # Define the text to be displayed
            title = font.render("Como Jugar", True, BLACK)
            font = pygame.font.Font(None, 28)
            line1_text = font.render("1. Presiona jugar para buscar oponente.", True, BLACK)
            line2_text = font.render("2. Adivina la palabra antes que tu oponente.", True, BLACK)
            line3_text = font.render("3. Si te equivocas 6 veces, pierdes.", True, BLACK)
            line4_text = font.render("4. Cada letra que adivines te dará 100 puntos.", True, BLACK)
            line5_text = font.render("5. En caso de empate en puntos ganará el menor tiempo.", True, BLACK)
            
            # Get the dimensions of the text to be displayed
            title_rect = title.get_rect()
            line1_rect = line1_text.get_rect()
            line2_rect = line2_text.get_rect()
            line3_rect = line3_text.get_rect()
            line4_rect = line4_text.get_rect()
            line5_rect = line5_text.get_rect()
            
            # Set the position of the text to be displayed
            title_rect.centerx = screen.get_rect().centerx
            title_rect.top = 50
            
            # Calculate the total height of the lines
            total_height = line1_rect.height + line2_rect.height + line3_rect.height + line4_rect.height + line5_rect.height
            
            # Calculate the vertical spacing between the lines
            vertical_spacing = (screen_height - title_rect.bottom - total_height) / 8
            
            # Set the positions of the lines of text
            line1_rect.centerx = screen.get_rect().centerx
            line1_rect.top = title_rect.bottom + vertical_spacing
            line2_rect.centerx = screen.get_rect().centerx
            line2_rect.top = line1_rect.bottom + vertical_spacing
            line3_rect.centerx = screen.get_rect().centerx
            line3_rect.top = line2_rect.bottom + vertical_spacing
            line4_rect.centerx = screen.get_rect().centerx
            line4_rect.top = line3_rect.bottom + vertical_spacing
            line5_rect.centerx = screen.get_rect().centerx
            line5_rect.top = line4_rect.bottom + vertical_spacing
            
            # Draw the text on the screen
            screen.blit(title, title_rect)
            screen.blit(line1_text, line1_rect)
            screen.blit(line2_text, line2_rect)
            screen.blit(line3_text, line3_rect)
            screen.blit(line4_text, line4_rect)
            screen.blit(line5_text, line5_rect)
            button = Button(10, 30, 100, 30, RED, BLACK, "atrás")
            button.draw(screen)
            pygame.display.update()
            
        while comoJugar:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    comoJugar = False
                    main = False
                else:
                    if button.handle_event(event):
                        comoJugar = False
            button.draw(screen)
            pygame.display.update()
        #
        #Puntajes
        if puntajes:
            screen.fill(DARK_BLUE)
            
            # set the positions for the title and table
            title_position = (screen_width // 2, 50)
            
            # set the size of each cell in the table
            cell_size = (150, 50)
            
            # create the table data
            table_data = [
            ]
            
            # set the number of rows and columns in the table
            num_rows = len(table_data)
            if num_rows>7:
                num_rows = 7
            num_cols = 2
            
            # calculate the size of the table
            table_width = num_cols * cell_size[0]
            table_height = num_rows * cell_size[1]
            
            # calculate the position of the top-left cell of the table
            table_position = ((screen_width - table_width) // 2 + 80, (screen_height - table_height) // 2 + 50)

            # set the font for the text
            font = pygame.font.Font(None, 48)
            # draw the title text
            title = font.render("Mejores Jugadores", True, WHITE)
            title_rect = title.get_rect(center=title_position)
            screen.blit(title, title_rect)
            
            # set the font for the text
            font = pygame.font.Font(None, 24)
            # draw the table data
            for i in range(num_rows):
                for j in range(num_cols):
                    cell_position = (table_position[0] + j * cell_size[0], table_position[1] + i * cell_size[1])
                    cell_text = font.render(table_data[i][j], True, WHITE)
                    cell_rect = cell_text.get_rect(center=cell_position)
                    # draw the cell border
                    cell_rect_outer = pygame.Rect(cell_position[0] - cell_size[0] // 2, cell_position[1] - cell_size[1] // 2, cell_size[0], cell_size[1])
                    pygame.draw.rect(screen, PURPLE, cell_rect_outer, 2)
                    screen.blit(cell_text, cell_rect)
            
            # update the screen
            button = Button(10, 30, 100, 30, RED, BLACK, "atrás")
            button.draw(screen)
            pygame.display.update()
            
            # run the Pygame loop
            while puntajes:
                ptsActiveMsg = "Puntajes"
                enpts = ptsActiveMsg.encode("utf-8")
                s.sendall(enpts)
                
                data = s.recv(1024)
                decoded_data = data.decode('utf-8')
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        puntajes = False
                        main = False
                    else:
                        if button.handle_event(event):
                            puntajes = False
                button.draw(screen)
                pygame.display.update()
        #
        
        # Fill the screen with white
        screen.fill(LIGHT_GREEN)
        
        # Draw title
        screen.blit(title_text, (title_x, title_y))

        # Draw buttons
        jugarButton.draw(screen)
        comojugarButton.draw(screen)
        puntajesButton.draw(screen)
        salirButton.draw(screen)
        #numButton.draw(screen)

        # Update the screen
        pygame.display.update()
    #




    running2 = False
    while running2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running2 = False

    pygame.quit()
except socket.error as err:
    print('Error connecting to', HOST, 'on port', PORT, ':', err)
finally:
    s.close()