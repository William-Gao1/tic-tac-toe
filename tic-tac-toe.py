# Import and initialize the pygame library
import pygame
import math

from pygame.locals import *
pygame.init()

player = 0
ai = 0
mask = 0
playerTurn = True
screen = pygame.display.set_mode([500, 500])
WIDTH, HEIGHT = screen.get_size()
screen.fill((255, 255, 255))


def makeMove(pos, opp, mask, space):
    
    newPos = pos | (2 ** (space + (space//3)))
    newMask = newPos | opp

    return newPos, newMask



for i in range(3):
    pygame.draw.line(screen, (0, 0, 0), (i*WIDTH/3, HEIGHT), (i*WIDTH/3, 0))
    pygame.draw.line(screen, (0, 0, 0), (0, i * HEIGHT/3),
                            (WIDTH, i * HEIGHT/3))


def main():
    global playerTurn
    global player
    global mask
    global ai

    
    
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                space = getSpace(x,y)
                drawX(space) 
                player, mask = makeMove(player, ai, mask, space)
                checkState(player, mask)
                
                

                
                aiMove = minimax (ai, player, mask, 20, -math.inf, math.inf, True)
                print(aiMove)
                #print(canPlay (0, mask))
                drawO(aiMove[1])
                ai, mask = makeMove(ai, player, mask, aiMove[1])
                checkState(ai, mask)

    
        pygame.display.flip()

   
    pygame.quit()


def drawX(space):
    x,y = getSpaceTopLeft(space)
    pygame.draw.line(screen, (0, 0, 0), (x, y), (x+(WIDTH/3-5), y+(HEIGHT/3)), 10)
    pygame.draw.line(screen, (0, 0, 0), (x+(WIDTH/3-5), y), (x, y+(HEIGHT/3)), 10)
    pygame.display.flip

def drawO(space):
    x,y = getSpaceCentre(space)
    pygame.draw.circle(screen, (0, 0, 0), (x,y), WIDTH/6, 10)


def getSpaceTopLeft(space):
    return (space % 3) * (WIDTH/3), (space // 3) * (HEIGHT/3)

def getSpaceCentre(space):
    return ((space % 3) * (WIDTH/3))+(WIDTH/6), ((space // 3) * (HEIGHT/3)) + (HEIGHT/6)


def getSpace(x, y):
    return (x//(WIDTH//3)) + (3 * ((y//(HEIGHT//3))))


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
