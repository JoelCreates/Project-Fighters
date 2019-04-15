import math, random, sys
import enum
import pygame, time
from pygame.locals import*
from sys import exit
from pygame import mixer

#initialising python
pygame.init()
#pygame.mixer.init()
pygame.mixer.pre_init(44100,16,2,4096)
mixer.init()

#define display
W, H = 1600,900
HW, HH = (W/2), (H/2)
AREA = W * H


#bsound effects
buttonsound1 = pygame.mixer.Sound("ButtonSound1.wav") 


#initialising display
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
FPS = 54
progress = 0
background = pygame.Surface(DS.get_size())
smallfont = pygame.font.SysFont("century gothic",25)


#background image
bg = pygame.image.load("Daytime.jpg").convert()
loadingimg = pygame.image.load("LoadingScreen.png").convert()
pause = pygame.image.load("Pause screen.png").convert()
gameover = pygame.image.load("Game Over.png").convert()
mainmenu = pygame.image.load("Main_Menu4.png").convert()
#mainmenu = pygame.transform.smoothscale(mainmenu, (W,H))
loadingimg = pygame.transform.smoothscale(loadingimg, (W,H))

#define some colours
BLACK = (0,0,0,255)
WHITE = (255,255,255,255)
green = (0,140,0)
grey = (180,180,180)

walkLeft = [pygame.image.load('Moving1.png'), pygame.image.load('Moving2.png'), pygame.image.load('Moving3.png'), pygame.image.load('Moving4.png'), pygame.image.load('Moving5.png'), pygame.image.load('Moving6.png'), pygame.image.load('Moving7.png'), pygame.image.load('Moving8.png'), pygame.image.load('Moving9.png')]
walkRight = []
for i in walkLeft:
    walkRight.append(pygame.transform.flip(i, True, False))


char = pygame.image.load('Moving1.png').convert_alpha()
char2 = pygame.image.load('Moving1.png').convert_alpha()
char2 = pygame.transform.flip(char2, True, False)

x = 0
y = 500
height = 40
width = 87
vel = 5
isJump = False
jumpCount = 10
left = False
right = False
walkCount = 0
run = True


# FUNCTIONS
def event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            exit()

# === CLASSES === (CamelCase names)

class Button():

    def __init__(self, text, x=0, y=0, width=100, height=50, command=None):

        self.text = text
        self.command = command

        self.image_normal = pygame.Surface((width, height))
        self.image_normal.fill(green)

        self.image_hovered = pygame.Surface((width, height))
        buttonsound1.play()

        self.image = self.image_normal
        self.rect = self.image.get_rect()

        font = pygame.font.Font('freesansbold.ttf', 15)


        text_image = font.render(text, True, WHITE)
        text_rect = text_image.get_rect(center = self.rect.center)

        self.image_normal.blit(text_image, text_rect)
        self.image_hovered.blit(text_image, text_rect)

        # you can't use it before `blit` 
        self.rect.topleft = (x, y)

        self.hovered = False
        #self.clicked = False

    def update(self):

        if self.hovered:
            self.image = self.image_hovered
        else:
            self.image = self.image_normal

    def draw(self, surface):

        surface.blit(self.image, self.rect)

    def handle_event(self, event):

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                print('Clicked:', self.text)
                if self.command:
                    self.command()

                    
class GameState( enum.Enum ):
    Loading = 0
    Menu = 1
    Settings = 2
    Playing = 3
    GameOver = 4
    
#set the game state initially.
game_state = GameState.Loading


#LOADING
def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)

    return textSurface, textSurface.get_rect()

def loading(progress):
    if progress < 100:
        text = smallfont.render("Loading: " + str(int(progress)) + "%", True, WHITE)
    else:
        text = smallfont.render("Loading: " + str(100) + "%", True, WHITE)

    DS.blit(text, [50, 660])

def message_to_screen(msh, color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = HW, HH + y_displace
    DS.blit(textSurf, textRect)

while (progress/4) < 100:
    event_handler()
    DS.blit(loadingimg, (0,0))
    time_count = (random.randint(1,1))
    increase = random.randint(1,20)
    progress += increase
    pygame.draw.rect(DS, green, [50, 700, 402, 29])
    pygame.draw.rect(DS, grey, [50, 701, 401, 27])
    if (progress/4) > 100:
        pygame.draw.rect(DS, green, [50, 700, 401, 28])
    else:
        pygame.draw.rect(DS, green, [50, 700, progress, 28])
    loading(progress/4)
    pygame.display.flip()

    time.sleep(time_count)

#changing to menu
game_state = GameState.Menu


Menumusic = pygame.mixer.music.load("MainMenu.mp3")
Menumusic = pygame.mixer.music.play(-1, 0.0)

def main_menu():
    DS.blit(mainmenu, (0, 0))
    pygame.display.update()
    
    btn1 = Button('Hello', 200, 50, 100, 50)
    btn2 = Button('World', 200, 150, 100, 50)

    while run:
        event_handler()
        btn1.update()
        btn2.update()

        # --- draws ---

        btn1.draw(DS)
        btn2.draw(DS)

    pygame.display.update()
    
main_menu()


    


"""
def redrawGameWindow():
    global walkCount
    DS.blit(mainmenu, (0,0))
    pygame.display.update()
    
    DS.blit(background, (0, 0))
    lastMoved = "left"
    if walkCount + 1 >= 27:
        walkCount = 0
    if left:
        DS.blit(walkLeft[walkCount//3],(x,y))
        walkCount +=1
        lastMoved = "left"
    elif right:
        DS.blit(walkRight[walkCount//3], (x,y))
        walkCount +=1
        lastMoved = "right"
    else: #this is when its moving neither left or right
        if lastMoved == "left":
            DS.blit(char2, (x, y))
        else:
            DS.blit(char, (x, y))
"""





  
#mainloop
px, py, speed = HW, HH, 10
while run:
    CLOCK.tick(FPS)
    event_handler()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < W - width - vel:
        x+= vel
        right = True
        left = False
    else:
        right = False
        left = False
        walkCount = 0

    if not(isJump):
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y-= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10

           

#    redrawGameWindow()




    
    
