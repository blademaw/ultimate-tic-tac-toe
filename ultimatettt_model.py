"""
Implements classes for playing Ultimate Tic-Tac-Toe.
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
        self.currentPlayer = None # keep this so I know it never gets called
        self.currentState = self.initialGameState()
        self.actionCounter = 0

    def initialGameState(self):
        currentPlayer = np.random.choice([1,2]) # randomly choose who goes first
        self.symbols = {currentPlayer: "X", self.getNextPlayer(currentPlayer): "O"} # init symbols
        return UltimateTTTState(
            getEmptyBoard(),
            np.array([0,0,0,0,0,0,0,0,0]),
            currentPlayer,
            self.symbols
        )

    def getCurrentPlayer(self):
        return self.currentState.getCurrentPlayer()
    
    def getNextPlayer(self, player):
        return 2 if player == 1 else 1
    
    def generateNextState(self, state, action):
        """ Generates a new state given a current state and action """
        newState = deepcopy(state)
        newState.board[action.square][action.x][action.y] = action.player
        newState.currentPlayer = 2 if state.currentPlayer == 1 else 1
        newState.squares = getSquares(deepcopy(newState), action)
        return newState
    
    def getPossibleActions(self, state):
        return state.getPossibleActions()
    
    def gameEnds(self):
        return self.currentState.isTerminal()
    
    def update(self, action):
        curState = self.currentState
        self.currentState = self.generateNextState(curState, action)
        self.currentPlayer = self.currentState.getCurrentPlayer()
        self.actionCounter += 1
    
    def __str__(self):
        # return str(self.currentState)
        return f"\nMove {self.actionCounter}: Agent #{self.getCurrentPlayer()} ({self.symbols[self.getCurrentPlayer()]}) to play:\n" + \
            self.currentState.printBoard()
    
    def debugState(self):
        return f"\nMove {self.actionCounter}: Agent #{self.getCurrentPlayer()} ({self.symbols[self.getCurrentPlayer()]}) to play:\n" + str(self.currentState)


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
        # print(self.squares)
        if self.isTerminal(): return []

        for square in np.where(self.squares == 0)[0]:
            # print(square)
            for row in range(3):
                # print(row)
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
            # print(macroBoard, True)
            return True
        # print(macroBoard, False)
        return False
    
    def getReward(self, player):
        macroBoard = deepcopy(self.squares)
        macroBoard[np.where(macroBoard == -1)] = 0 # make non-taken squares one value
        winPlayer = winsTTTBoard(macroBoard.reshape((3,3)), returnPlayer=True)
        
        if self.isTerminal():
            if winPlayer is None: # win = 1, lose = -1, tie = 0
                return 0
            else:
                return 1 if winPlayer == player else -1
        return False
    
    def printBoard(self):
        return boardToString(deepcopy(self.board), deepcopy(self.squares))

    def __str__(self):
        return f"Board:\n{boardToString(deepcopy(self.board), deepcopy(self.squares), self.symbols)}\nTerminal? {'Yes' if self.isTerminal() else 'No'}\nCurrent Player: {self.currentPlayer}\nSquares: {self.squares}\nLegal Moves: {self.getPossibleActions()}"
