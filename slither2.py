# SLITHER
#  Note that in this version, the apple does not spawn in multiples of x hence we ca have a snake larger than the apple and also allow freedom of spawns (less grid like)


import pygame
import time
import random
import sys
sys.setrecursionlimit(10000)

pygame.init()

#Colours RGB
white = (255, 255, 255)
black = (0, 0, 0)
StartScreenGreen = (105, 196, 166)
blue = (21,78, 210)


red = (255, 0, 0)
light_red = (255,51, 51)
green  = (34,177,76)
light_green = (0, 255, 0)

yellow = (255,255,0)
light_yellow = (255,255,102)



display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Slither')

image = pygame.image.load('SnakeHead.png')
clock = pygame.time.Clock() #return pygame clock object, used to set FPS
AppleThickness = 30 
block_size = 20
FPS = 30
#direc = 2 #Used in rotating SnakeHead.png, 0=right

smallfont = pygame.font.SysFont("futura", 25)
mediumfont = pygame.font.SysFont("futura", 50)
largefont = pygame.font.SysFont("futura", 80)



def StartScreen():
    Start = True
    while Start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    Start = False
                if event.key ==pygame.QUIT:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        message_to_screen("Welcome to Snake!", StartScreenGreen, -200, "large")
        message_to_screen("The objective of the game is to eat the red apples.", black, -130)
        message_to_screen("More apples = longer snake!", black, -100)
        message_to_screen("DO NOT RUN INTO YOURSELF OR THE EDGE OF THE WINDOW.", red, -70)

        #Draw buttons (x,y,width,height)
        
        button("Play", 150, 500, 100, 50, green, light_green, action="play")
        button("Controls", 350, 500, 100, 50, yellow, light_yellow, action="controls")
        button("Quit", 550, 500, 100, 50, red, light_red, action = "quit")






                         
        #message_to_screen("Press C to play, Q to quit or P to pause.", red, 100)

        pygame.display.update()
        clock.tick(30)

def StartControls():
    
    Scont = True
    while Scont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message_to_screen("Controls", StartScreenGreen, -200, "large")
        message_to_screen("The objective of the game is to eat the red apples.", black, -130)
        message_to_screen("More apples = longer snake!", black, -100)
        message_to_screen("DO NOT RUN INTO YOURSELF OR THE EDGE OF THE WINDOW.", red, -70)

        #Draw buttons (x,y,width,height)
        
        button("Play", 150, 500, 100, 50, green, light_green, action="play")
        button("Main Menu", 350, 500, 100, 50, yellow, light_yellow, action="Main Menu")
        button("Quit", 550, 500, 100, 50, red, light_red, action = "quit")






                         
        #message_to_screen("Press C to play, Q to quit or P to pause.", red, 100)

        pygame.display.update()
        clock.tick(30)

def snake(block_size, snakeList): # Creates snake.
    if direc == 0: #right
        head = pygame.transform.rotate(image, 270)
    if direc == 1: #left
        head = pygame.transform.rotate(image, 90)
    if direc == 2: #up
        head = image
    if direc == 3: #down
        head = pygame.transform.rotate(image, 180)
        
    #Note: when snake grows, blocks get added to the front of the list [0]
    #Therefore, the snakes head will be in [-1] (last position)   
    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))

    for XnY in snakeList[:-1]: #[:-1]perform for loop UPTO the last element.
        ## draw rectangle (snake) (where, colour, [x,y,width,height])
        # pygame.draw.rect(gameDisplay, green, [lead_x,lead_y, block_size, block_size])
        
        pygame.draw.rect(gameDisplay, blue, [XnY[0],XnY[1], block_size, block_size])


def AppleGen(): #Created this function to deal with the overuse of the below 2 lines
    randAppleX= round(random.randrange(0, display_width-AppleThickness)) # The round function is used to align
    randAppleY= round(random.randrange(0, display_height-AppleThickness))

    return randAppleX, randAppleY

def score(score):
    score = score*100
    text = smallfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, [0,0])

def text_objects(text, color, size): #ep 27
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = mediumfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    
    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))#Finds centre of button based on given parameters.
    gameDisplay.blit(textSurf, textRect)

#LEGACY MESSAGE TO SCREEN
#def message_to_screen(msg, color):
##    screen_text = font.render(msg, True, color) #RENDER FONT
##    gameDisplay.blit(screen_text, [display_width/2, display_height/2])

##    textSurf, textRect = text_objects(msg, color)
##    textRect.center = (display_width / 2), (display_height / 2)
##    gameDisplay.blit(textSurf, textRect)

#defining a variable name inside the parameter list is called a parameter default.
def message_to_screen(msg,color, y_displace=0, size = "small"):
    #y_displace used to move text from the centre
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)

def button(text, x, y, width, height, initial_color, active_color, action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #cur[0] is the x position of the mouse.
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x,y,width,height))
        #click[0] is LMB.
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            if action == "controls":
                StartControls()
            if action == "play":
                gameLoop()
            if action=="Main Menu":
                StartScreen()
                
            
    else:
        pygame.draw.rect(gameDisplay, initial_color, (x,y,width,height))
    text_to_button(text, black, x, y, width, height)
    

def pause():

    paused = True
    message_to_screen("Game is paused", red, -100, size="large")
    message_to_screen("Press C to continue or Q to quit.", black, 25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        #gameDisplay.fill(white)
        
        clock.tick(5)
    
def gameLoop():
    global direc #allow access to direction variable to modify
    gameExit = False
    gameOver = False

    # Starting positions for the snake, divide window height and width by 2 to find middle.
    lead_x = display_width/2
    lead_y = display_height/2
    direc = 2 #Starting direction for the HEAD of the snake. (up)

    lead_x_change = 0 #Variable for snake movement along x-axis
    lead_y_change = -20  #Variable for snake movement along y-axis

    snakeList = []  # Create empty list for Snake.
    snakeLength = 4

    # Random position of apple in range from 0 to max window size minus the head of snake (block)
    # Round function is used to align the apple with the snake so perfect overlapping occurs.
    # This happens because the variables lead_x and lead_y always position the snake head within  multiple of 10.
    # Later chose to remove this.
    #randAppleX= round(random.randrange(0, display_width-block_size))#/10.0)*10.0 #Delete eventually, used to be used to ensure that apple thickness was a multiple of 10 when apple and snake size were the same.
    #randAppleY= round(random.randrange(0, display_height-block_size))#/10.0)*10.0
    randAppleX, randAppleY = AppleGen()

    while not gameExit:

        if gameOver == True: #If loop to allow the game over screen to display infront of game, if left in the whileloop then text will overlay.
            message_to_screen("Game Over!", red, -50, size = "large")
            message_to_screen("Press C to play again or Q to quit", black, 50, size = "medium")
            pygame.display.update()

        while gameOver == True:
            #time.sleep(1)
            #gameDisplay.fill(white)Pause screen overlay
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Added if statement so you can use x (window close) to end game during game over screen.
                    gameExit = True
                    gameOver = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: #Quit game when q is pressed
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c: #Play again when c is pressed
                        gameLoop()  #Calls the gameLoop function to play again.

        
        for event in pygame.event.get():  # gets an 'event' from the user
            if event.type == pygame.QUIT:  # QUIT is an event specified by pygame
                gameExit = True  # Exit Loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # left arrow key
                    lead_x_change = -block_size  # move left
                    lead_y_change = 0
                    direc = 1
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                    direc = 0
                elif event.key == pygame.K_UP:  # left arrow key
                    lead_y_change = -block_size# down
                    lead_x_change = 0
                    direc = 2
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size  # up
                    lead_x_change = 0
                    direc = 3
                elif event.key == pygame.K_p: #If the user presses p, game pauses.
                    pause() 
        # Checks whether the snake is outside of bounds
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True     



        # LOGIC
        lead_x += lead_x_change
        lead_y += lead_y_change
        gameDisplay.fill(white)  # Fill bg as white
        # draw rectange (apple)
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])

        
        snakeHead = []  # Create empty list for position of snake
        snakeHead.append(lead_x)  # Append x position of head to snakeHead list
        snakeHead.append(lead_y)  # Append y position of head to snakeHead list  
        snakeList.append(snakeHead) #Append the snakeHead list inside the SnakeList list.

        if len(snakeList) > snakeLength:  # If there are more items in the list than allowed length:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:  # :-1 means anything up to the last element. Note that the last element is the head so without this code an error would occur all the time.
            if eachSegment == snakeHead:  # If a segment has the same co-ordinates as the snake head then collision occurs: game ends.
                gameOver = True
        
        snake(block_size, snakeList)
        score(snakeLength-4)
        pygame.display.update()

#### Older cross-over code:        
#### This block of code can be used (if AppleThickness is used) later to amend difficulty settings, it is an alternate version of the if statements above it EP 22        
##        if lead_x >= randAppleX and lead_x <= randAppleX + AppleThickness:
##            if lead_y >= randAppleY and lead_y <= randAppleY + AppleThickness:
##                randAppleX= round(random.randrange(0, display_width-block_size))#/10.0)*10.0  # The round function is used to align
##                randAppleY= round(random.randrange(0, display_height-block_size))#/10.0)*10.0
##                snakeLength += 1 # When apple is eaten, snake size increase by 1

                
## Newer cross-over / collision code:
        ## Checks whether any edge of the snake is clipping over an apple, remember lead_x is only the top left of the snake so this code compensates for it.
        ## if the top left of snake head is larger than the top left of apple and top right OR top RIGHT of snake is bigger than top left and less than right side of apple.
        if (lead_x > randAppleX and lead_x < randAppleX + AppleThickness) or (lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness):
            if (lead_y > randAppleY and lead_y < randAppleY + AppleThickness) or (lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness):
                #randAppleX= round(random.randrange(0, display_width-AppleThickness))#/10.0)*10.0  # The round function is used to align
                #randAppleY= round(random.randrange(0, display_height-AppleThickness))#/10.0)*10.0
                randAppleX, randAppleY = AppleGen()

                snakeLength += 1 # When apple is eaten, snake size increase by 1
        
        clock.tick(FPS)

    #message_to_screen("You Lose", red) # When the while loop is broken display this message
    #pygame.display.update() # To see message, the display must be updated
    #time.sleep(2) # Delay the screen so that the message can be read, else it would instantly close.

    pygame.quit()
    quit()

StartScreen()
gameLoop()
