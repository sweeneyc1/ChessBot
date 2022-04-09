"""
Main Driver File. Responsible for User Input and displaying current GameState object.
"""

from Chessnut import Game
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
engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\couturep\Downloads\stockfish_14.1_win_x64\stockfish_14.1_win_x64\stockfish_14.1_win_x64.exe")

'''
Initialize a global dictionary of images. Called only once to save resources.
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess/chesspieces/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #access image by calling IMAGES['wp']

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
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
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
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    print(playerClicks[0])
                    print(playerClicks[1])
                    gs.makeMove(move, chessgame)
                    sqSelected = ()
                    playerClicks = []
                    board.push_uci(move.getChessNotation())
                    if not board.is_game_over():
                        print(board)
                        result = engine.play(board, chess.engine.Limit(time=0.1))
                        cpuMove = result.move
                        board.push(cpuMove)
                        conv = moveConversion(cpuMove.__str__())
                        move = ChessEngine.Move(conv[0],conv[1], gs.board)
                        gs.makeMove(move, chessgame)



        drawGameState(SCREEN, gs, validMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()
        p.display.set_caption('Chess Bot')


#Highlight piece and possible moves
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s,(c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow* SQ_SIZE))


#Animate the moves
def animateMove(move, screen, board, clock):
    global colors
    coords= []
    dR = move.endRow - move.startRow
    dC= move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) +abs(dC)) * framesPerSquare
    for frame in range(frameCount+1):


def moveConversion(move):
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    return (ranksToRows[move[1]],filesToCols[move[0]]),(ranksToRows[move[3]],filesToCols[move[2]])

#Used for all graphics for current game state
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(SCREEN)
    drawPieces(SCREEN, gs.board)
    highlightSquares(screen, gs, validMoves, sqSelected)

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
