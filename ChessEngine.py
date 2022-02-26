"""
Responsible for storing information about the current state of a chess game and determining valid moves and log them.
"""
class GameState():
    def __init__(self):
        #8x8 2d list, each element has 2 characters.
        #The first character represents color of the piece, 'b' or 'w'
        #The second character represents type of piece, 'K', 'Q', 'R', 'B', 'N' or 'p'
        #"--" represents empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.moveLog = []