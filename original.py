import random, time, pygame, sys
# 랜덤함수, 시간스레드용, 파이게임, 시스템(IO사용)
from pygame.locals import *
 #파이게임 라이브러리 가져옴.
FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 680
BOXSIZE = 15
BOARDWIDTH = 20
BOARDHEIGHT = 40
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#               R    G    Bㅑ,
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BORDERCOLOR = RED
BGCOLOR = GRAY
TEXTCOLOR = BLACK
TEXTSHADOWCOLOR = GRAY
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS) # 각 네모칸 색에 맞는 밝은색 지정.

TEMPLATEWIDTH = 6
TEMPLATEHEIGHT = 6

A_SHAPE_TEMPLATE = [['......',
                     '......',
                     '...0..',
                     '..000.',
                     '.0...0',
                     '......'],

                    ['.0....',
                     '..0...',
                     '..00..',
                     '..0...',
                     '.0....',
                     '......'],

                    ['......',
                     '......',
                     '0...0.',
                     '.000..',
                     '..0...',
                     '......'],
                    
                    ['......',
                     '...0..',
                     '..0...',
                     '.00...',
                     '..0...',
                     '...0..']]

B_SHAPE_TEMPLATE = [['......',
                     '......',
                     '...00.',
                     '.000..',
                     '...00.',
                     '......'],
                    
                    ['......',
                     '...0..',
                     '...0..',
                     '..000.',
                     '..0.0.',
                     '......'],

                     ['......',
                     '.00...',
                     '..000.',
                     '.00...',
                     '......',
                     '......'],

                     ['......',
                     '..0.0.',
                     '..000.',
                     '...0..',
                     '...0..',
                     '......']]

C_SHAPE_TEMPLATE = [['......',
                     '.0000.',
                     '.0....',
                     '.0000.',
                     '......',
                     '......'],
                    
                    ['......',
                     '.000..',
                     '.0.0..',
                     '.0.0..',
                     '.0.0..',
                     '......'],

                     ['......',
                     '......',
                     '.0000.',
                     '....0.',
                     '.0000.',
                     '......'],

                     ['......',
                     '..0.0.',
                     '..0.0.',
                     '..0.0.',
                     '..000.',
                     '......']]

D_SHAPE_TEMPLATE = [['......',
                     '...0..',
                     '...0..',
                     '...0..',
                     '.00000',
                     '......'],
                    
                    ['.0....',
                     '.0....',
                     '.0000.',
                     '.0....',
                     '.0....',
                     '......'],

                    ['......',
                     '....0.',
                     '....0.',
                     '.0000.',
                     '....0.',
                     '....0.'],

                     ['......',
                     '......',
                     '.00000',
                     '...0..',
                     '...0..',
                     '...0..']]

E_SHAPE_TEMPLATE = [['......',
                     '..000.',
                     '..0...',
                     '.0000.',
                     '......',
                     '......'],
                    
                    ['......',
                     '......',
                     '..0...',
                     '..000.',
                     '..0.0.',
                     '..0.0.'],

                     ['......',
                     '......',
                     '.0000.',
                     '...0..',
                     '.000..',
                     '......'],

                     ['......',
                     '......',
                     '....0.',
                     '..000.',
                     '..0.0.',
                     '..0.0.']]

F_SHAPE_TEMPLATE = [['......',
                     '....0.',
                     '....0.',
                     '....0.',
                     '....0.',
                     '....0.'],
                    
                    ['......',
                     '......',
                     '.00000',
                     '......',
                     '......',
                     '......']]

PIECES = {'A': A_SHAPE_TEMPLATE,
          'B': B_SHAPE_TEMPLATE,
          'C': C_SHAPE_TEMPLATE,
          'D': D_SHAPE_TEMPLATE,
          'E': E_SHAPE_TEMPLATE,
          'F': F_SHAPE_TEMPLATE}


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    ygame.display.set_caption('HELLTRIS') #이름 저장
 
    showTextScreen('HELLTRIS')
    runGame()
    showTextScreen('Game Over')


def runGame():
    # setup variables for the start of the game
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    while True: # game loop
        if fallingPiece == None:
            # 떨어지는 물체다 없으면, 다음게 떨어짐.
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() # 떨어지는 타임 리셋

            if not isValidPosition(board, fallingPiece):
                return# 포지션에 끼울 물체 없으면 게임 오버함.

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP:
                if (event.key == K_p):
                    # 게임 멈춤
                    DISPLAYSURF.fill(BGCOLOR)
                    
                    showTextScreen('Paused')#멈춤 표시 
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False

            elif event.type == KEYDOWN:
                # 키를 누르면 위치가 바뀜.
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                # 여분 자리 있으면 회전 가능하게.
                elif (event.key == K_UP or event.key == K_w):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                elif (event.key == K_q): # rotate the other direction
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                # 아래 키 누르면 빨리 떨어지게.
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # 스페이스 누르면 바로 아래로 떨어짐.
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

        
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        # 폴링 타임만큼 시간 스레드가 흐르면 다 떨어진걸로 간주.
        if time.time() - lastFallTime > fallFreq:
            # 객체 바닥에 닿으면
            if not isValidPosition(board, fallingPiece, adjY=1):
                # 보드에 부착
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                # 안닿으면 계속 아래로 감.
                fallingPiece['y'] += 1
                lastFallTime = time.time()

         # 스크린에 표시할 정보.
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkForKeyPress():
   # 키누르는거 이벤트로 받기/
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showTextScreen(text):
    
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # 아무키나 누르시오...
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

 #esc버튼 누르거나 x버튼 눌러도 종료 되게 만들기.
def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate() 
        pygame.event.post(event)


def calculateLevelAndFallFreq(score):
    #렙 올라갈수록 속도가 빨라짐
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq

def getNewPiece():
    # 랜덤 로테이션이랑 랜덤 컬러 
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2,
                'color': random.randint(0, len(COLORS)-1)}
    return newPiece


def addToBoard(board, piece):
    
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
    
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board


def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
    
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

def isCompleteLine(board, y):
    
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True


def removeCompleteLines(board):
   numLinesRemoved = 0
    y = BOARDHEIGHT - 1 
    while y >= 0:
        if isCompleteLine(board, y):
            
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
          
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            
        else:
            y -= 1 
    return numLinesRemoved


def convertToPixelCoords(boxx, boxy):
   
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
   
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def drawBoard(board):
    
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])


def drawStatus(score, level):
    
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)

# 외관 나타내기
def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
       pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))


def drawNextPiece(piece):
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)


if __name__ == '__main__':
    main()