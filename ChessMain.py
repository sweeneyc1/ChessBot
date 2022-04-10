"""
Main Driver File. Responsible for User Input and displaying current GameState object.
"""

from Chessnut import Game
from matplotlib.pyplot import pause
import pygame as p
import ChessEngine
import chess
import chess.engine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}
SCREEN = p.display.set_mode((WIDTH, HEIGHT))
engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\mpete\Downloads\stockfish_14.1_win_x64_popcnt\stockfish_14.1_win_x64_popcnt.exe")
'''
Initialize a global dictionary of images. Called only once to save resources.
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
            IMAGES[piece] = p.transform.scale(p.image.load("C:/Users/mpete/Documents/ChessBot/chesspieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))    #access image by calling IMAGES['wp']

'''
Main Driver. Handle user input and updating graphics.
'''
def main():
    chessgame = Game()
    board = chess.Board()
    p.init()
    SCREEN = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    SCREEN.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    pauseupdates = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            if board.is_game_over():
                print("Check & Mate")
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                    #ValidMoveGeneration
                if len(playerClicks) == 1:
                    rowRank = get_Row(row)
                    colRank = get_Col(col)
                    rowColRank = colRank+rowRank
                    allmoves = chessgame.get_moves()
                    if allmoves != []:
                        pauseupdates = True
                        validMoves = [i for i in allmoves if i.startswith(rowColRank)]
                        print("All Posible moves for "+ rowColRank + " are: ")
                        print(validMoves)
                        for move in validMoves:
                            highlightSquares(SCREEN, gs, move, sqSelected)
                        

                if len(playerClicks) == 2:
                    pauseupdates = False
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    #print(move.getChessNotation())
                    #print(playerClicks[0])
                    #print(playerClicks[1])
                    valid = gs.makeMove(move, chessgame)
                    if gs.moveLog != []:
                        animateMove(gs.moveLog[-1], SCREEN, gs.board, clock)
                    sqSelected = ()
                    playerClicks = []
                    if not board.is_game_over() and valid:
                        board.push_uci(move.getChessNotation())
                        print(board)
                        result = engine.play(board, chess.engine.Limit(time=0.1))
                        cpuMove = result.move
                        board.push(cpuMove)
                        conv = moveConversion(cpuMove.__str__())
                        move = ChessEngine.Move(conv[0],conv[1], gs.board)
                        gs.makeMove(move, chessgame)
                        animateMove(gs.moveLog[-1], SCREEN, gs.board, clock)

        if pauseupdates == False:
            drawGameState(SCREEN, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        p.display.set_caption('Chess Bot')


#Highlight piece and possible moves
def highlightSquares(screen, gs, move, sqSelected):
                print(move)
                move=cordConversion(move)
                print(move)

                image = p.transform.scale(p.image.load("C:/Users/mpete/Documents/ChessBot/chesspieces/blue.png"), (SQ_SIZE, SQ_SIZE))
                image.set_alpha(128)
                screen.blit(image, p.Rect(move[1]*SQ_SIZE,move[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                p.display.update(move[1]*SQ_SIZE,move[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE)
                
#Animate the moves
def animateMove(move, screen, board, clock):
    global colors
    coords= []
    dR = move.endRow - move.startRow
    dC= move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) +abs(dC)) * framesPerSquare
    for frame in range(frameCount+1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)



def moveConversion(move):
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    return (ranksToRows[move[1]],filesToCols[move[0]]),(ranksToRows[move[3]],filesToCols[move[2]])

def cordConversion(move):
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    return (ranksToRows[move[3]],filesToCols[move[2]])

#Used for all graphics for current game state
def drawGameState(screen, gs):
    drawBoard(SCREEN)
    drawPieces(SCREEN, gs.board)

#to draw squares on board
def drawBoard(SCREEN):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(SCREEN, color, p.Rect(c*SQ_SIZE,r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


# to draw pieces on the board
def drawPieces(SCREEN, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                SCREEN.blit(IMAGES[piece], p.Rect(c*SQ_SIZE,r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
def get_Row(val):
    for key, value in ranksToRows.items():
        if val == value:
            return key

def get_Col(val):
    for key, value in filesToCols.items():
        if val == value:
            return key

# menu page for game intro
def intro():
    p.init()
    clock = p.time.Clock()

    #colors for buttons
    red = (200,0,0)
    green = (0,200,0)
    blue = (0,0,200)

    bright_red = (255,0,0)
    bright_green = (0,255,0)
    bright_blue = (0,0,255)

    intro = True
    while intro:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                quit()

        SCREEN.fill(p.Color("white"))
        largeText = p.font.Font('freesansbold.ttf',80)
        TextSurf, TextRect = text_objects("Chessbot", largeText)
        TextRect.center = ((WIDTH/2),(HEIGHT/2))
        SCREEN.blit(TextSurf, TextRect)

        button("easy", 50, 300, 100, 33, green, bright_green)
        button("intermediate", 170, 300, 150, 33, blue, bright_blue)
        button("advanced", 340, 300, 150, 33, red, bright_red)

        p.display.update()
        clock.tick(15)

# for text
def text_objects(text, font):
    textSurface = font.render(text, True, p.Color("black"))
    return textSurface, textSurface.get_rect()

# button
def button(msg,x,y,w,h,ic,ac):
    mouse = p.mouse.get_pos()
    click = p.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        p.draw.rect(SCREEN, ac,(x,y,w,h))

        if click[0] == 1 and msg != None:
            if msg == "easy":
                #set mode to easy
                engine.configure({"UCI_Elo": 1350})
                main()
            elif msg == "intermediate":
                #set mode to intermediate
                engine.configure({"UCI_Elo": 1800})
                main()
            elif msg == "advanced":
                #set mode to advanced
                engine.configure({"UCI_Elo": 2500})
                main()

    else:
        p.draw.rect(SCREEN, ic,(x,y,w,h))

    smallText = p.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    SCREEN.blit(textSurf, textRect)

intro()
