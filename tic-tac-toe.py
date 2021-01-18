# Import and initialize the pygame library
import pygame
import math

from pygame.locals import *
import pygame.freetype
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 500,500
TOGGLE_BUTTON = (550, 450)
RESET_BUTTON = (550, 400)
screen = pygame.display.set_mode([700, 500])
player = 0
ai = 0
mask = 0
aiActive = True
playerTurn = True
gameRunning = True
GAME_FONT = pygame.freetype.Font("Calibri Regular.ttf", 24)


def reset():
    global screen
    global player
    global ai
    global mask
    global playerTurn
    global gameRunning
    player = 0
    ai = 0
    mask = 0
    
    playerTurn = True
    gameRunning = True
    screen = pygame.display.set_mode([700, 500])
    
    screen.fill((255, 255, 255))
    
    for i in range(4):
        pygame.draw.line(screen, (0, 0, 0), (i*WIDTH/3, HEIGHT), (i*WIDTH/3, 0))
        pygame.draw.line(screen, (0, 0, 0), (0, i * HEIGHT/3),
                                (WIDTH, i * HEIGHT/3))


    pygame.draw.rect(screen, (250,100,0), (TOGGLE_BUTTON[0], TOGGLE_BUTTON[1],125,25))
    GAME_FONT.render_to(screen, (TOGGLE_BUTTON[0]+15, TOGGLE_BUTTON[1]+5), "Toggle AI", (0, 0, 0))
    #textsurface, rect = myfont.render('Some Text', False, (0, 0, 0))


    pygame.draw.rect(screen, (250,100,0), (RESET_BUTTON[0], RESET_BUTTON[1],125,25))
    GAME_FONT.render_to(screen, (RESET_BUTTON[0]+35, RESET_BUTTON[1]+5), "Reset", (0, 0, 0))

reset()

def makeMove(pos, opp, mask, space):
    
    newPos = pos | (2 ** (space + (space//3)))
    newMask = newPos | opp

    return newPos, newMask






def main():
    global playerTurn
    global player
    global mask
    global ai
    global aiActive

    
    
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                space = getSpace(x,y)
                if space != -1 and gameRunning and playerTurn:
                    drawX(space) 
                    player, mask = makeMove(player, ai, mask, space)
                    state = checkState(player, mask)
                
                    if state != -1:
                        endGame(state)
                        break

                    if aiActive:
                        aiMove = minimax (ai, player, mask, 20, -math.inf, math.inf, True)
                        drawO(aiMove[1])
                        ai, mask = makeMove(ai, player, mask, aiMove[1])
                    
                        state = checkState(ai, mask)
                        playerTurn =  not playerTurn
                    
                    if state != -1:
                        endGame(state)
                        break

                    playerTurn =  not playerTurn
                elif space != -1 and gameRunning and  not playerTurn:
                    drawO(space)
                    ai, mask = makeMove(ai, player, mask, space)
                    state = checkState(ai, mask)
                    if state != -1:
                        endGame(state)
                        break
                    playerTurn = not playerTurn
                    
                else:
                    checkButtons(x, y)


        GAME_FONT.render_to(screen, (TOGGLE_BUTTON[0]+15, TOGGLE_BUTTON[1]+5), "Toggle AI", (0, 0, 0))

        pygame.display.flip()

   
    pygame.quit()

def checkButtons(x,y):
    global aiActive
    global playerTurn
    global ai
    global mask
    global player
    if x > RESET_BUTTON[0] and x < RESET_BUTTON[0] + 125 and y > RESET_BUTTON[1] and y < RESET_BUTTON[1]+25:
        reset()
    elif x > TOGGLE_BUTTON[0] and x < TOGGLE_BUTTON[0] + 125 and y > TOGGLE_BUTTON[1] and y < TOGGLE_BUTTON[1]+25:
        aiActive =  not aiActive
        if aiActive and not playerTurn:
            aiMove = minimax (ai, player, mask, 20, -math.inf, math.inf, True)
            drawO(aiMove[1])
            ai, mask = makeMove(ai, player, mask, aiMove[1])
                    
            state = checkState(ai, mask)
            playerTurn =  not playerTurn

def drawX(space):
    x,y = getSpaceTopLeft(space)
    pygame.draw.line(screen, (0, 0, 0), (x, y), (x+(WIDTH/3-5), y+(HEIGHT/3)), 10)
    pygame.draw.line(screen, (0, 0, 0), (x+(WIDTH/3-5), y), (x, y+(HEIGHT/3)), 10)
    pygame.display.flip

def drawO(space):
    x,y = getSpaceCentre(space)
    pygame.draw.circle(screen, (0, 0, 0), (x,y), WIDTH/6, 10)

def endGame(status):
    global gameRunning
    if status == 0:
        GAME_FONT.render_to(screen, (575, 100), "Tie!", (0, 0, 0))
    elif not playerTurn:
        GAME_FONT.render_to(screen, (575, 100), "O Wins!", (0, 0, 0))
    else:
        GAME_FONT.render_to(screen, (575, 100), "X Wins!", (0, 0, 0))
    gameRunning = False
    

def getSpaceTopLeft(space):
    return (space % 3) * (WIDTH/3), (space // 3) * (HEIGHT/3)

def getSpaceCentre(space):
    return ((space % 3) * (WIDTH/3))+(WIDTH/6), ((space // 3) * (HEIGHT/3)) + (HEIGHT/6)


def getSpace(x, y):
    if x < WIDTH and y < HEIGHT:
        return(x//(WIDTH//3)) + (3 * ((y//(HEIGHT//3))))
    else:
        return -1


def checkState(pos, mask):
    m = pos & (pos >> 1)
    if m & (m>>1):
        return 1
    
    m = pos & (pos >> 4)
    if(m & (m >> 4)):
        return 1

    m = pos & (pos >> 5)
    if(m & (m >> 5)):
        return 1
    
    m = pos & (pos >> 3)
    if(m & (m >> 3)):
        return 1
    
    if (mask == 1911):
        return 0
    
    return -1

def minimax(aiPos, playerPos, mask, depth, alpha, beta, maximizingPlayer):
    aiState, playerState = checkState(aiPos, mask), checkState(playerPos, mask)
    if aiState != -1 or playerState != -1:
        if aiState == 1:
            return depth, 0
        elif playerState == 1:
            return -(20-depth), 0
        else:
            return 0, 0
    

    if maximizingPlayer:
        value = -math.inf
        col = 0
        for i in range(9):
            if canPlay(i, mask):
                newAIPos, newMask = makeMove(aiPos, playerPos, mask, i)
                result = minimax(newAIPos, playerPos, newMask, depth-1, alpha, beta, False)[0]
                if result > value:
                    value = result
                    col = i
                alpha = max(alpha, value)
                if alpha >= beta:
                    break

                
            
        return value, col
    else:
        value = math.inf
        col = 0
        for i in range (9):
            if canPlay(i, mask):
                newPlayerPos, newMask = makeMove(playerPos, aiPos, mask, i)
                result = minimax(aiPos, newPlayerPos, newMask, depth-1, alpha, beta, True)[0]
                if result < value:
                    value = result
                    col = i
                beta = min(beta, value)
                if beta <= alpha:
                    break
        
        return value, col
            
                
    
def canPlay (space, mask):
    return ((2 ** (space + (space//3))) & mask) == 0


if __name__ == '__main__':
    main()
