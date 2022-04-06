# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 18:38:14 2022

@author: barnettl
"""

import chess
import chess.engine

"""change these file paths to where stockfish is installed on your computer"""
engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\barnettl\Downloads\stockfish\stockfish_14.1_win_x64_popcnt.exe")
engine2 = chess.engine.SimpleEngine.popen_uci(r"C:\Users\barnettl\Downloads\stockfish\stockfish_14.1_win_x64_popcnt.exe")
"""print(engine.options)  
print("\n\n")  
engine.configure({"UCI_Elo": 1500})
print(engine.options["UCI_Elo"])"""

engine.configure({"UCI_Elo": 2500})
engine2.configure({"UCI_Elo": 1350})
i = 0
board = chess.Board()
while not board.is_game_over():
    if(i%2==0):
        result = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
    else:
        result = engine2.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
    
    
    print(board)
    print("---------------")
    print(result.move)
    print("---------------")
    
print(board)
if(i%2==0):
    print("engine 1")
else:
    print("engine 2")
engine.quit()
