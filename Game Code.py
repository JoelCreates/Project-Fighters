import math, random, sys
import pygame, time
from pygame.locals import*

#define display
W, H = 1600,900
HW, HH = (W/2), (H/2)
AREA = W * H

#initialising display
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
FPS = 60
progress = 0
background = pygame.Surface(DS.get_size())
#smallfont = pygame.font.SysFont("comicsansms",25)



walkRight = [pygame.image.load('Moving1.png'), pygame.image.load('Moving2.png'), pygame.image.load('Moving3.png'), pygame.image.load('Moving4.png'), pygame.image.load('Moving5.png'), pygame.image.load('Moving6.png'), pygame.image.load('Moving7.png'), pygame.image.load('Moving8.png'), pygame.image.load('Moving9.png')]

walkLeft = []
for i in walkRight:
    walkLeft.append(pygame.transform.flip(i, True, False))
    
char = pygame.image.load('Testing1.png').convert_alpha()
char2 = pygame.image.load('Testing1.png').convert_alpha()
char2 = pygame.transform.flip(char2, True, False)


x = 0
y = 500
height = 64
width = 64
vel = 5
isJump = False
jumpCount = 10
left = False
right = False
walkCount = 0

#background image
bg = pygame.image.load("Daytime.jpg")
loading = pygame.image.load("LoadingScreen.png")



#define some colours
BLACK = (0,0,0,255)
WHITE = (255,255,255,255)
green = (0,255,0)


def redrawGameWindow():
    global walkCount
    #DS.blit(bg, (0,0))
    pygame.display.update()
    DS.blit(background, (0, 0))
    lastMoved = "left"
    if walkCount + 1 >= -27:
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
        text = smallfont/render("Loading: " + str(int(progress)) + "%", True, green)
    else:
        text = smallfont.render("Loading: " + str(100) + "%", True, green)

    DS.blit(text, [453, 273])

def message_to_screen(msh, color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = HW, HH + y_displace
    DS.blit(textSurf, textRect)

while (progress/2) < 100:
    time_count = (random.randint(1,1))
    increase = random.randint(1,20)
    progress += increase
    pygame.draw.rect(DS, green, [423, 223, 204, 49])
    pygame.draw.rect(DS, BLACK, [424, 224, 202, 47])
    if (progress/2) > 100:
        pygame.draw.rect(DS, green, [425, 225, 200, 45])
    else:
        pygame.draw.rect(DS, green, [425, 225, progress, 45])
        loading(progress/2)
        pygame.display.flip()

    time.sleep(time_count)
"""


class spritesheet:
    def __init__(self, filename, py, tw, th, tiles):
        self.sheet = pygame.image.load(filename).convert_alpha()

        self.py = py
        self.tw = tw
        self.th = th
        self.totalCellCount = tiles

        self.rect = self.sheet.get_rect()
        w, h = tw, th
        hw, hh = self.cellCenter = (w / 2, h / 2)

        self.cells = [(1+i*tw, self.py, tw-1, th-1) for i in range(tiles)]
        self.handle = list([
            (0,0), (-hw, 0), (-w, 0),
            (0, -hh), (-hw, -hh), (-w, -hh),
            (0, -h), (-hw, -h), (-w, -h),])

    def draw(self, surface, cellIndex, x, y, handle = 0):
        hdl = self.handle[handle]
        surface.blit(self.sheet, (x + hdl[0], y + hdl[1]), area=self.cells[cellIndex])

    
"""def game_intro():

    intro = True

    while intro:
        DS.blit(loading, (0,0))
        pygame.display.update()
        CLOCK.tick(15)"""


#s = spritesheet('Number18.png', 1085, 80, 134, 8)

CENTER_HANDLE = 6

Index = 0

#mainloop
run = True
px, py, speed = HW, HH, 10
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #s.draw(DS, Index % s.totalCellCount, HW, HH, CENTER_HANDLE)
    CLOCK.tick(FPS)


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < 1900 - width - vel:
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

    redrawGameWindow()

    #Index +=1

    #pygame.draw.circle(DS, WHITE, (HW, HW), 20, 10)


    
    
