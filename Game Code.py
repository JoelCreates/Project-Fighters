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
pygame.display.set_caption('Ultimate Fighters')


#define display
W, H = 1600,900
HW, HH = (W/2), (H/2)
AREA = W * H

#Music
Menu1 = "MainMenu.mp3"
Menumusic = pygame.mixer.music.load(Menu1)


#bsound effects
buttonsound1 = pygame.mixer.Sound("ButtonSound1.wav") 
mouseclick1 = pygame.mixer.Sound("MouseClick.wav")

#initialising display
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
FPS = 54
progress = 0

background = pygame.Surface(DS.get_size())
smallfont = pygame.font.SysFont("century gothic",25)
largefont = pygame.font.SysFont("century gothic",40)


#background image
bg = pygame.image.load("Daytime.jpg").convert()
canyon = pygame.image.load('canyon.png').convert()
arcadescreen = pygame.image.load("Arcade Screen.png").convert()
loadingimg = pygame.image.load("LoadingScreen.png").convert()
pause = pygame.image.load("Pause screen.png").convert()
instructions = pygame.image.load("Instructions Screen.png").convert()
gameover = pygame.image.load("Game Over.png").convert()
mainmenu = pygame.image.load("Main_Menu.png").convert()
leaderboardimg = pygame.image.load('Leaderboard Image.png').convert()
loadingimg = pygame.transform.smoothscale(loadingimg, (W, H))
canyon = pygame.transform.smoothscale(canyon, (W, H))
instructions = pygame.transform.smoothscale(instructions, (W, H))
images = [bg, instructions,pause, gameover, mainmenu]


#Image Load
exit1 = pygame.image.load("exitbutton.png")
exit1 = pygame.transform.smoothscale(exit1, (165, 72))
leaderboard1 = pygame.image.load('leaderboard.png')
leaderboard1 = pygame.transform.smoothscale(leaderboard1,(529, 114))
fight = pygame.image.load('Fight.png')
fight = pygame.transform.smoothscale(fight,(256, 117))
loadgif = pygame.image.load('loading.gif').convert_alpha()

#define some colours
BLACK = (0,0,0,255)
WHITE = (255,255,255,255)
green = (0,140,0)
grey = (180,180,180)


#Sprite Image Load
#18
walkLeft = [pygame.image.load('Moving1.png'), pygame.image.load('Moving2.png'), pygame.image.load('Moving3.png'), pygame.image.load('Moving4.png'), pygame.image.load('Moving5.png'), pygame.image.load('Moving6.png'), pygame.image.load('Moving7.png'), pygame.image.load('Moving8.png'), pygame.image.load('Moving9.png')]
walkRight = []

for i in walkLeft:
    walkRight.append(pygame.transform.flip(i, True, False))
   
for x in range(len(walkLeft)):
    walkLeft[x] = pygame.transform.smoothscale(walkLeft[x], (372, 493))

for x in range(len(walkRight)):
    walkRight[x] = pygame.transform.smoothscale(walkRight[x], (372, 493))


char = pygame.image.load('Moving1.png').convert_alpha()
char = pygame.transform.smoothscale(char, (372, 493))
char2 = pygame.image.load('Moving1.png').convert_alpha()
char2 = pygame.transform.smoothscale(char2, (372, 493))
char2 = pygame.transform.flip(char2, True, False)


x = 0
y = 407
height = 40
width = 87
vel = 5
isJump = False
jumpCount = 10
left = False
right = False
walkCount = 0
walkCount1 = 0
run = True

# === CLASSES === (CamelCase names)

class Enemy(object):
    walkLeft1 = [ pygame.image.load("GB1.png"), pygame.image.load("GB2.png"), pygame.image.load("GB3.png"), pygame.image.load("GB4.png") ]
    walkRight1= []
    global vel
    global walkCount1
    
    for i in walkLeft1:
        walkRight1.append(pygame.transform.flip(i, True, False))

    

    for x in range(len(walkLeft1)):
        walkLeft1[x] = pygame.transform.smoothscale(walkLeft1[x], (372, 493))

    for x in range(len(walkRight1)):
        walkRight1[x] = pygame.transform.smoothscale(walkRight1[x], (372, 493))

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount1 = 0
        self.vel = 3

    def draw(self, DS):
        self.move()
        if self.walkCount1 + 1 <= 33:
            self.walkCount1 = 0

        if self.vel > 0:
            DS.blit(self.walkRight1[self.walkCount1 //4], (self.x, self.y))
            self.walkCount1 += 1
        else: 
            DS.blit(self.walkLeft1[self.walkCount1 //4], (self.x, self.y))
            self.walkCount1 += 1


    def move(self):
        global walkCount1
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount1 = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount1 = 0



class Button():

    def __init__(self, text, x=0, y=0, width=100, height=50, command=None):

        self.text = text
        self.command = command
        self.image_normal = pygame.Surface((width, height))
        self.image_normal.fill(green)
        self.image_hovered = pygame.Surface((width, height))
        self.image_hovered.fill(grey)
        self.image  = self.image_normal
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.hovered= False  # is the mouse over this button?

    def update(self):
        pass

    def handleMouseOver( self, mouse_position ):
        """ If the given co-ordinate inside our rect,
            Do all the mouse-hovering work             """
        # Check button position against mouse
        # Change the state *once* on entry/exit
        if ( self.mouseIsOver( mouse_position ) ):
            if ( self.hovered == False ):
                self.image = self.image_hovered
                self.hovered = True   # edge-triggered, not level triggered
                # Do we want to check pygame.mixer.get_busy() ?
                if ( pygame.mixer.get_busy() == False ):
                    buttonsound1.play()
                    print("Hovering above")
        else:
            if ( self.hovered == True ):
                self.image = self.image_normal
                self.hovered = False

    def mouseIsOver( self, mouse_position ):
        """ Is the given co-ordinate inside our rect """
        return self.rect.collidepoint( mouse_position )

    def draw(self, surface):

        surface.blit(self.image, self.rect)




class GameState( enum.Enum ):
    Loading = 0
    Menu = 1
    Settings = 2
    Playing = 3
    GameOver = 4



# FUNCTIONS
def EventHandler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            exit()

                    

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
    EventHandler()
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

    time.sleep(0.01)





def MainMenu():
    #Menumusic = pygame.mixer.music.play(-1, 0.0)
    game_state = GameState.Menu
    DS.blit(mainmenu, (0, 0))
    pygame.display.update()
    run = True
    btn1 = Button('Arcade Mode', 545,  231, 525, 113)
    btn2 = Button('Vs Mode',  240, 371, 1121, 115)
    btn3 = Button('Instructions', 542, 488, 531, 109)
    btn4 = Button('Options', 605, 606, 342, 116)
    btn5 = Button('Exit game', 579, 726, 395, 111)
    # Put the buttons into a list so we can loop over them, simply
    buttons = [ btn1, btn2, btn3, btn4, btn5 ]

    if (pygame.mixer.get_busy() == False) or (pygame.mixer.get_busy() == True) :
            pygame.mixer.music.stop()
            pygame.mixer.music.load("MainMenu.mp3")
            print("Music playing")
            pygame.mixer.music.play(-1, 0.0)

    while run:
        EventHandler()
        # draw the buttons
        #for b in buttons:
            #b.draw( DS ) # --- draws ---

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEMOTION:
                mouse_position = event.pos
                for b in buttons:
                    b.handleMouseOver( mouse_position )
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = event.pos
                for b in buttons:
                    if ( b.mouseIsOver( mouse_position ) ):
                        print('Clicked:', b.text)
                        
                        if b.text == "Arcade Mode":
                            mouseclick1.play()
                            print("Arcade mode has been clicked")
                            ArcadeMode()
                            
                        elif b.text == "Vs Mode":
                            mouseclick1.play()
                            print("Vs mode has been clicked")

                            
                        elif b.text == "Instructions":
                            mouseclick1.play()
                            print("Instructions mode has been clicked")
                            InstructionsMode()
                            
                        elif b.text == "Options":
                            mouseclick1.play()
                            print("options has been clicked")

                            
                        elif b.text == "Exit game":
                            mouseclick1.play()
                            run = False
                            pygame.quit()
                            print("Exit button pressed")
                        print('Sound Effect')
                if game_state != 1:
                    run = False
                            
                        



        pygame.display.update()
        


def InstructionsMode():
    DS.blit(instructions, (0,0))
    pygame.display.update()
    run = False
    instructions1 = True
    counter = 0
    exitbutton = Button('Exit', 719, 737, 165, 72)
    arrow = Button('Arrow', 1108, 732, 120, 68)
    
    arrow1 = pygame.image.load("arrow.png")
    arrow1 = pygame.transform.smoothscale(arrow1, (120, 68))
    
    box1 = pygame.image.load("Box1.png").convert_alpha()
    box1 = pygame.transform.smoothscale(box1, (1222,706))
    
    box2 = pygame.image.load("Box2.png").convert_alpha()
    box2 = pygame.transform.smoothscale(box2, (1222,706))
    
    box3 = pygame.image.load("Box3.png").convert_alpha()
    box3 = pygame.transform.smoothscale(box3, (1222,706))
    
    box4 = pygame.image.load("Box4.png").convert_alpha()
    box4 = pygame.transform.smoothscale(box4, (1222,706))
    
    box5 = pygame.image.load("Box5.png").convert_alpha()
    box5 = pygame.transform.smoothscale(box5, (1222,706))
    

    
    
    while instructions1:
        EventHandler()
        if (pygame.mixer.get_busy() == True):
            pygame.mixer.music.set_volume(0.2)
        if counter == 0:
            DS.blit(box1, (182,88))
            DS.blit(arrow1,(1108, 710))
            DS.blit(exit1, (719, 737))
            pygame.display.update()
 
        elif counter == 1:
            DS.blit(box2, (182,88))
            pygame.display.update()
     
        elif counter == 2:
            DS.blit(box3, (182,88))
            pygame.display.update()
 
        elif counter == 3:
            DS.blit(box4, (182,88))
            pygame.display.update()

        elif counter == 4:
            DS.blit(box5, (182,88))
            pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                instructions1 = False
            if event.type == pygame.MOUSEMOTION:
                mouse_position = event.pos
                arrow.handleMouseOver( mouse_position )
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = event.pos
                if ( arrow.mouseIsOver( mouse_position ) ):
                        print('Clicked:', arrow.text)
                        print('Sound Effect')
                        counter +=1
                        mouseclick1.play()
                if ( exitbutton.mouseIsOver( mouse_position ) ):
                    print("Instructiona Exited")
                    mouseclick1.play()
                    instructions1 = False
                    MainMenu()


def ArcadeMode():
    DS.blit(arcadescreen, (0, 0))
    pygame.display.update()
    run = False
    arcade = True
    
    char1 = Button('Goku Black', 125,  144, 261, 189)
    char2 = Button('Gohan',  500, 152, 165, 178)
    char3 = Button('Vegeta', 758, 146, 340, 189)
    char4 = Button('Goku', 1148, 146, 337, 193)
    char5 = Button('Android 18', 129, 393, 257, 261)

    exitbutton = Button('Exit', 134, 800, 267, 75)
    leaderboard = Button('Leaderboard',557, 786, 529, 114)
    

    fightbutton = Button('Fight', 1320, 785, 256, 117)

    characters = [ char1, char2, char3, char4, char5 ]
    limiter = 0

    cx, cy = 669,746
 

    if (pygame.mixer.get_busy() == True):
            pygame.mixer.music.stop()
            pygame.mixer.music.load("ArcadeMode.mp3")
            print("Music playing")
            pygame.mixer.music.play(-1, 0.0)

    while arcade:
        EventHandler()
        DS.blit(exit1, (134, 800))
        DS.blit(leaderboard1, (557, 786))
        DS.blit(fight, (1320, 785))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                arcade = False
            if event.type == pygame.MOUSEMOTION:
                mouse_position = event.pos
                for b in characters:
                    b.handleMouseOver( mouse_position )
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = event.pos
                for b in characters:
                    if ( b.mouseIsOver( mouse_position ) ):
                        print('Clicked:', b.text)
       
                        if b.text == "Goku Black" and limiter == 0:
                            mouseclick1.play()
                            print("Goku Black: Selected")
                            limiter += 1
                            text1 = largefont.render(b.text + ': Selected', True, WHITE, None)
                            DS.blit(text1,(cx,cy))
                            
                        elif b.text == "Gohan" and limiter == 0:
                            mouseclick1.play()
                            print("Gohan: Selected")
                            limiter += 1
                            text1 = largefont.render(b.text + ': Selected', True, WHITE, None)
                            DS.blit(text1,(cx,cy))
                         
                        elif b.text == "Vegeta" and limiter == 0:
                            mouseclick1.play()
                            print("Vegeta: Selected")
                            limiter += 1
                            text1 = largefont.render(b.text + ': Selected', True, WHITE, None)
                            DS.blit(text1,(cx,cy))
                                       
                        elif b.text == "Goku" and limiter == 0:
                            mouseclick1.play()
                            print("Goku Selected")
                            limiter += 1
                            text1 = largefont.render(b.text + ': Selected', True, WHITE, None)
                            DS.blit(text1,(cx,cy))
                        
                        elif b.text == "Android 18" and limiter == 0:
                            mouseclick1.play()
                            print("Android 18: Selected")
                            limiter += 1
                            text1 = largefont.render(b.text + ': Selected', True, WHITE, None)
                            DS.blit(text1,(cx,cy))

                        pygame.display.update()

                    if ( exitbutton.mouseIsOver( mouse_position ) ):
                        print("Arcade Exited")
                        mouseclick1.play()
                        arcade = False
                        MainMenu()

                    if ( leaderboard.mouseIsOver( mouse_position ) ):
                        print("Leaderboard Clicked")
                        mouseclick1.play()
                        LeaderBoard()

                    if ( fightbutton.mouseIsOver( mouse_position ) ):
                        print("Fight Clicked")
                        mouseclick1.play()

                        FightMode()
                        
man = Enemy(1400, 407, 96, 136, 22)
def redrawGameWindow():
    global walkCount
    pygame.display.update()
    DS.blit(canyon,(0,0))
    lastMoved = "left"
    man.draw(DS)
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



def FightMode():
    fight = True
    arcade = False
    progress = 0
    global isJump, jumpCount
    global x,y, vel
    global width, height
    global left, right
    px, py, speed = HW, HH, 10
    if (pygame.mixer.get_busy() == True):
            pygame.mixer.music.stop()
        
    while fight:
        while(progress/4) < 100:
            EventHandler()
            DS.fill(BLACK)
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

            time.sleep(0.2)
        pygame.display.update()
   
       
        CLOCK.tick(FPS)
        redrawGameWindow()
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

        pygame.display.update()
        

        
      
                        
            
                        
def LeaderBoard():
    DS.blit(leaderboardimg, (0,0))
    pygame.display.update()
    arcade = False
    leader = True
    text1 = largefont.render('Player Names', True, WHITE, None)
    text2 = largefont.render('Time Taken', True, WHITE, None)
    exitbutton = Button('Exit', 134, 800, 267, 75)
 
    while leader:
        EventHandler()
        DS.blit(text1, (256, 110))
        DS.blit(text2, (986, 110))
        DS.blit(exit1, (134, 800))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                leader = False
            if event.type == pygame.MOUSEMOTION:
                mouse_position = event.pos               
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = event.pos            
                if ( exitbutton.mouseIsOver( mouse_position ) ):
                    print("Leaderboard Exited")
                    mouseclick1.play()
                    leader = False
                    ArcadeMode()
                    


                        
                        
            
          
  
    # Put the buttons into a list so we can loop over them, simply










    
MainMenu()


    












  

           

    #redrawGameWindow()


    
    
