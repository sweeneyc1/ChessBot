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

    def makeMove(self, move):
        print(move)
        if self.whiteToMove: 
                if self.board[move.startRow][move.startCol][0] == "w":
                    self.board[move.startRow][move.startCol] = "--"
                    self.board[move.endRow][move.endCol] = move.pieceMoved
                    self.moveLog.append(move)
                    self.whiteToMove = False
        if self.whiteToMove == False: 
                if self.board[move.startRow][move.startCol][0] == "b":
                    self.board[move.startRow][move.startCol] = "--"
                    self.board[move.endRow][move.endCol] = move.pieceMoved
                    self.moveLog.append(move)
                    self.whiteToMove = True

class Move():

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

