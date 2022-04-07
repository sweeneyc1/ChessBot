"""
Main Driver File. Responsible for User Input and displaying current GameState object.
"""
from Chessnut import Game
import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Initialize a global dictionary of images. Called only once to save resources.
'''
def loadImages():
    pieces = ['wR', 'wp', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess/chesspieces/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        #IMAGES[piece] = p.transform.scale(p.image.load("C:/Users/mpete/Documents/ChessBot/chesspieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #access image by calling IMAGES['wp']

'''
Main Driver. Handle user input and updating graphics.
'''
def main():
    chessgame = Game()
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
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
                    #here
                    rowRank = get_Row(row)
                    colRank = get_Col(col)
                    rowColRank = rowRank+colRank
                    #print(rowColRank)
                    allmoves = chessgame.get_moves()
                    posmoves = [x for x in allmoves if rowColRank in x]
                    print("All Posible moves for "+ rowColRank + " are: ")
                    print(posmoves)
                    
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move, chessgame)
                    sqSelected = ()
                    playerClicks = []



        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        p.display.set_caption('Chess Bot')

#Used for all graphics for current game state
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

#to draw squares on board
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE,r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


# to draw pieces on the board
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE,r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
                
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
main()
