"""
Used for commonly-invoked/used functions useful for playing UltimateTTT.
"""
# TODO: refactor this to use UltimateTTTRule
from copy import copy, deepcopy
import numpy as np


def generateNextState(state, action):
    """ Generates a new state given a current state and action """
    newState = deepcopy(state)
    assert newState.board[action.square][action.x][action.y] == 0 # ensure cell not taken

    newState.board[action.square][action.x][action.y] = action.player
    newState.currentPlayer = 2 if state.currentPlayer == 1 else 1 # FIXME: should use GameRule
    newState.squares = getSquares(deepcopy(newState), action)
    return newState


def getNeighboringCells(x,y):
    """ Returns an np array of neighboring cell indices in a 3x3 grid for a cell (for square selection purposes) """
    indices = np.reshape(range(9),(3,3))
    return np.array(list(set(list(indices[max(0,x-1):x+2,max(0,y-1):y+2].flatten())) - set([x*3 + y])))


def getSquares(state, action):
    """ Returns updated squares np.array for square selection/availability for next turn """
    squares = state.squares
    squares[np.where(state.squares == 0)] = -1 # set past-available to neutral (not won/tied)
    
    # check if newly-filled cell in square leads to capture or tie
    boardWon = winsTTTBoard(deepcopy(state.board[action.square]))
    if boardWon:
        squares[action.square] = action.player # player owns square
    elif not boardWon and fullBoard(state.board[action.square]):
        squares[action.square] = -2 # set to tie
    
    # check if next player can go on square corresponding to past player's chosen cell
    squareIndex = action.x * 3 + action.y
    if squares[squareIndex] == -1:
        squares[squareIndex] = 0 # limit next move to only this square
        return squares
    else:
        # get available neighboring squares
        neighborIndices = getNeighboringCells(action.x,action.y)
        neighborValues = squares[neighborIndices]
        validSquares = neighborIndices[np.where(neighborValues == -1)]

        if len(validSquares) == 0:
            # if no adjacent cells available, choose other randomly
            otherSquareIndices = np.array(list(set(range(9)) - set(neighborIndices) - set([squareIndex])))
            if len(otherSquareIndices) == 0: return squares
            
            otherSquareValues = squares[otherSquareIndices]
            validSquares = otherSquareIndices[np.where(otherSquareValues == -1)]

        squares[validSquares] = 0 # update available squares to discovered available
        return squares


def winsTTTBoard(board, returnPlayer=False):
    """ Returns whether or not board is won, and optionally the winning player. """
    board = np.array(board) 
    board[np.where(board == -1)] = 0 # make unavailable squares one digit (might be redundant)
    board[np.where(board == -2)] = 0 # do not return ties (rep. as -2) as a winner

    if not returnPlayer:
        # check rows, cols, diags
        anyRowsWon = any([(len(set(board[i,:]))==1 and set(board[i,:])!={0}) for i in range(3)])
        anyColsWon = any([(len(set(board[:,i]))==1  and set(board[:,i])!={0}) for i in range(3)])
        anyDiagWon = any([(len(set(diag))==1 and set(diag)!={0}) for diag in [np.diagonal(board),np.fliplr(board).diagonal()]])

        return anyRowsWon or anyColsWon or anyDiagWon
    else:
        for rowSet in [set(board[i,:]) for i in range(3)]:
            if len(rowSet) == 1: 
                if list(rowSet)[0] != 0: return list(rowSet)[0]
        for colSet in [set(board[:,i]) for i in range(3)]:
            if len(colSet) == 1:
                if list(colSet)[0] != 0: return list(colSet)[0]
        for diagSet in [set(diag) for diag in [np.diagonal(board),np.fliplr(board).diagonal()]]:
            if len(diagSet) == 1:
                if list(diagSet)[0] != 0: return list(diagSet)[0]
        
    return None


def fullBoard(board):
    """ Returns whether or not a board is currently saturated """
    board = np.array(board).flatten()
    return len(np.where(board == 0)[0]) == 0


def getEmptyBoard():
    """ Returns an empty game board """
    return deepcopy({
        0: [[0,0,0],[0,0,0],[0,0,0]],
        1: [[0,0,0],[0,0,0],[0,0,0]],
        2: [[0,0,0],[0,0,0],[0,0,0]],
        3: [[0,0,0],[0,0,0],[0,0,0]],
        4: [[0,0,0],[0,0,0],[0,0,0]],
        5: [[0,0,0],[0,0,0],[0,0,0]],
        6: [[0,0,0],[0,0,0],[0,0,0]],
        7: [[0,0,0],[0,0,0],[0,0,0]],
        8: [[0,0,0],[0,0,0],[0,0,0]]
    })


def boardToString(board, squares, symbols={1: "X", 2: "O"}):
    """ Returns a string representation of a macro board """
    winSquareDict = {
        "X": [['X','X','X'],['X','X','X'],['X','X','X']],
        "O": [['O','O','O'],['O','O','O'],['O','O','O']]
    }
    winSquareCount = {
        symbol: np.sum(squares == player) for (player, symbol) in symbols.items()
    }
    b = board # for readability
    
    for squareIndex in range(9):
        if squares[squareIndex] not in (0, -1, -2): # FIXME: turn these into enums
            winSymbol = symbols[squares[squareIndex]]
            b[squareIndex] = winSquareDict[winSymbol]
        else:
            # NOTE: I'm hard-coding a lot of this, but this should never be a problem
            b[squareIndex] = np.array(b[squareIndex], dtype='<U1')
            b[squareIndex][np.where(b[squareIndex] == str(1))] = symbols[1]
            b[squareIndex][np.where(b[squareIndex] == str(2))] = symbols[2]
            b[squareIndex][np.where(b[squareIndex] == "0")] = " "
    
    # OPTIMIZE: this is dumb -- use comprehension or some better method (vertical concatenation?)
    board_str = """
                 |               |
     {b[0][0][0]} | {b[0][0][1]} | {b[0][0][2]}   |   {b[1][0][0]} | {b[1][0][1]} | {b[1][0][2]}   |   {b[2][0][0]} | {b[2][0][1]} | {b[2][0][2]}    
    ———|———|———  |  ———|———|———  |  ———|———|———   
     {b[0][1][0]} | {b[0][1][1]} | {b[0][1][2]}   |   {b[1][1][0]} | {b[1][1][1]} | {b[1][1][2]}   |   {b[2][1][0]} | {b[2][1][1]} | {b[2][1][2]}    
    ———|———|———  |  ———|———|———  |  ———|———|———   
     {b[0][2][0]} | {b[0][2][1]} | {b[0][2][2]}   |   {b[1][2][0]} | {b[1][2][1]} | {b[1][2][2]}   |   {b[2][2][0]} | {b[2][2][1]} | {b[2][2][2]} 
                 |               |
—————————————————|———————————————|—————————————————
                 |               |
     {b[3][0][0]} | {b[3][0][1]} | {b[3][0][2]}   |   {b[4][0][0]} | {b[4][0][1]} | {b[4][0][2]}   |   {b[5][0][0]} | {b[5][0][1]} | {b[5][0][2]}    
    ———|———|———  |  ———|———|———  |  ———|———|———   
     {b[3][1][0]} | {b[3][1][1]} | {b[3][1][2]}   |   {b[4][1][0]} | {b[4][1][1]} | {b[4][1][2]}   |   {b[5][1][0]} | {b[5][1][1]} | {b[5][1][2]}    
    ———|———|———  |  ———|———|———  |  ———|———|———   
     {b[3][2][0]} | {b[3][2][1]} | {b[3][2][2]}   |   {b[4][2][0]} | {b[4][2][1]} | {b[4][2][2]}   |   {b[5][2][0]} | {b[5][2][1]} | {b[5][2][2]} 
                 |               |
—————————————————|———————————————|—————————————————
                 |               |
     {b[6][0][0]} | {b[6][0][1]} | {b[6][0][2]}   |   {b[7][0][0]} | {b[7][0][1]} | {b[7][0][2]}   |   {b[8][0][0]} | {b[8][0][1]} | {b[8][0][2]}    
    ———|———|———  |  ———|———|———  |  ———|———|———   
     {b[6][1][0]} | {b[6][1][1]} | {b[6][1][2]}   |   {b[7][1][0]} | {b[7][1][1]} | {b[7][1][2]}   |   {b[8][1][0]} | {b[8][1][1]} | {b[8][1][2]}    
    ———|———|———  |  ———|———|———  |  ———|———|———   
     {b[6][2][0]} | {b[6][2][1]} | {b[6][2][2]}   |   {b[7][2][0]} | {b[7][2][1]} | {b[7][2][2]}   |   {b[8][2][0]} | {b[8][2][1]} | {b[8][2][2]} 
                 |               |
""".format(b=b)
    
    if winSquareCount["X"] > 0 or winSquareCount["O"] > 0:
        board_str = list(board_str)
        for s in symbols.values():
            for _ in range(winSquareCount[s]):
                start_pos = "".join(board_str).find(f' {s} | {s} | {s} ')
                board_str[start_pos:start_pos+11] = list(" "*11)
                board_str[start_pos+51:start_pos+51+11] = list(" "*11)
                board_str[start_pos+51*2:start_pos+51*2+11] = list(" "*5 + s + " "*5)
                board_str[start_pos+51*3:start_pos+51*3+11] = list(" "*11)
                board_str[start_pos+51*4:start_pos+51*4+11] = list(" "*11)
        board_str = "".join(board_str)
    
    return board_str