import math, random, sys
import pygame, time
from pygame.locals import*
from sys import exit
from pygame import mixer

#initialising python
pygame.init()
pygame.mixer.init()
pygame.mixer.pre_init()
#mixer.init()

#define display
W, H = 1600,900
HW, HH = (W/2), (H/2)
AREA = W * H

#Loading Background Music
MenuMusic = pygame.mixer.Sound("MainMenu.mp3")
MenuMusic = pygame.mixer.music.set_volume(0.45)


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

def event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            exit()


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


def main_menu():
    DS.blit(mainmenu, (0, 0))
    pygame.display.update()
    MenuMusic.play()

    
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
            
    main_menu()
#    redrawGameWindow()




    
    
