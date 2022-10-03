"""
Class to implement model for Ultimate Tic Tac Toe.
"""
import numpy as np
from ultimatettt_utils import *
from copy import deepcopy

# diction:
    # board = entire UltimateTTT board
    # square = one tile on the UltimateTTT board => a tic-tac-toe board

class Action():
    def __init__(self, player, square, x, y):
        self.player = player
        self.square = square
        self.x = x
        self.y = y
    
    def __str__(self):
        return str((self.player, self.square, self.x, self.y))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.square == other.square and \
            self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.square, self.x, self.y, self.player))


class UltimateTTTRule():
    def __init__(self):
        pass

    def initialGameState(self):
        self.currentPlayer = np.random.choice([1,2])
        self.symbols = {self.currentPlayer: "X", self.getNextPlayer(self.currentPlayer): "O"}
        return UltimateTTTState(getEmptyBoard(), np.array([0,0,0,0,0,0,0,0,0]), self.currentPlayer, self.symbols)
    
    def getNextPlayer(self, player):
        return 2 if player == 1 else 1


class UltimateTTTState():
    def __init__(self, board=None, squares=None, currentPlayer=None, symbols={1: "X", 2: "O"}):
        self.board = {i:[[0,0,0],[0,0,0],[0,0,0]] for i in range(9)} if board is None else board
        self.squares = np.array([0 for _ in range(9)]) if squares is None else squares # 0 = must move; -1 = can't access; 1/2 = player-owned
        self.currentPlayer = 1 if currentPlayer is None else currentPlayer
        self.symbols = symbols
    
    def getCurrentPlayer(self):
        return self.currentPlayer
    
    def getPossibleActions(self):
        possibleActions = []
        if self.isTerminal(): return []

        for square in np.where(self.squares == 0)[0]:
            for row in range(3):
                for col in range(3):
                    if self.board[square][row][col] == 0:
                        possibleActions += [Action(self.currentPlayer, square, row, col)]
        return possibleActions
    
    def takeAction(self, action):
        return generateNextState(self, action)
    
    def isTerminal(self):
        macroBoard = deepcopy(self.squares)
        macroBoard[np.where(macroBoard == -1)] = 0 # make non-taken squares one value
        if fullBoard(macroBoard.reshape((3,3))) or winsTTTBoard(macroBoard.reshape((3,3))):
            return True
    
    def getReward(self):
        macroBoard = deepcopy(self.squares)
        macroBoard[np.where(macroBoard == -1)] = 0 # make non-taken squares one value
        winPlayer = winsTTTBoard(macroBoard.reshape((3,3)), returnPlayer=True)
        
        if self.isTerminal() and winPlayer is not None:
                if winPlayer != self.currentPlayer: return 1
                else: return -1
        return False
    
    def printBoard(self):
        print(boardToString(deepcopy(self.board), deepcopy(self.squares)))

    def __str__(self):
        return f"Board:\n{boardToString(deepcopy(self.board), deepcopy(self.squares))}\nTerminal? {'Yes' if self.isTerminal() else 'No'}\nCurrent Player: {self.currentPlayer}\nSquares: {self.squares}\nLegal Moves: {self.getPossibleActions()}"
