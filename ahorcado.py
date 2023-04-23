# Example file showing a circle moving on screen
import pygame
import random

words = ["locomotora", "limones", "computo", "muercielago", "familia", "escalera", "python", "vacuna", "artritis"];

word = words[random.randint(0,8)]

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

# pygame setup
pygame.init()
pygame.font.init()
lettersFont = pygame.font.SysFont("Arial", 20)
timerFont = pygame.font.SysFont("Arial", 20)
screen = pygame.display.set_mode((730, 500))
clock = pygame.time.Clock()
running = True

screen.fill("purple")

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
    
"""
drawHead()
drawBody()
drawLegs()
drawArms()
drawDead()
pygame.display.update()
"""

# Set up the timer
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000) # 1 second
# Set up the timer variables
time_elapsed = 0
start_ticks = pygame.time.get_ticks()

errors = 0
aciertos = 0
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
                                running = False
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
                                running = False
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

    # Update the screen
    pygame.display.flip()

running2 = True
while running2:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running2 = False

pygame.quit()