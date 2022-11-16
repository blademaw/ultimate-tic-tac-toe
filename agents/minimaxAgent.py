# NOTE: all heuristics must be bounded by (-10, 10) -- or can i replace with inf?
import random
import numpy as np
from agents.agent import Agent

def move_ratio_heuristic(game_state, player):
    # heuristic: minimize opponent moves, maximize player moves
    if game_state.getCurrentPlayer() == player:
        return len(game_state.getPossibleActions())
    else:
        # return max (could also be average?) number of moves for me in next turn
        return max([len(game_state.takeAction(a).getPossibleActions()) for a in game_state.getPossibleActions()])
        # /len(game_state.getPossibleActions())

winning_sols = [((0,0),(0,1),(0,2)), ((1,0),(1,1),(1,2)), ((2,0),(2,1),(2,2)), ((0,0),(1,0),(2,0)), ((0,1),(1,1),(2,1)), ((0,2),(1,2),(2,2)), ((0,0),(1,1),(2,2)), ((0,2),(1,1),(2,0))]
def almost_won_squares_heuristic(game_state, player):
    # heuristic: number of squares that are one move away to be won by the player
    total = 0
    val_dict = {player:1, 0:0}
    available_boards = np.where((game_state.squares == 0) | (game_state.squares == -1))[0]
    # print(available_boards)
    for b in [game_state.board[i] for i in available_boards]:
        for sol in winning_sols:
            if np.sum([-1 if val_dict.get(b[sol[i][0]][sol[i][1]]) is None else val_dict[b[sol[i][0]][sol[i][1]]] for i in range(3)]) >= 2:
                total += 1
                break
    return total

def won_squares_heuristic(game_state, player):
    # heuristic: number of squares that are won by the player
    return np.sum(game_state.squares == player)

class playerAgent(Agent):
    def __init__(self, player, debug=False, render=False):
        super().__init__(player, debug=debug, render=render)
        self.initPlayer = player
        self.debug = debug
        self.render = render
    
    def minimax(self, state, depth, alpha, beta, maximizingPlayer, q_dict={}, initCall=False, h_func=move_ratio_heuristic):
        stateTerminal = state.isTerminal()
        if depth == 0 or stateTerminal:
            if stateTerminal: return state.getReward(self.player)*float('inf')
            return h_func(state, self.player)

        if maximizingPlayer:
            value = float('-inf')
            for action in state.getPossibleActions():
                value = max(value, self.minimax(state.takeAction(action), depth - 1, alpha, beta, False))
                # print(' '*(depth*4), action, value)
                alpha = max(alpha, value)
                if initCall:
                    q_dict[action] = value

                if alpha >= beta:
                    break
            return value

        else:
            value = float('inf')
            for action in state.getPossibleActions():
                value = min(value, self.minimax(state.takeAction(action), depth - 1, alpha, beta, True))
                # print(' '*(depth*4), action, value)
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value
        
    def selectAction(self, actions, game_state):
        DEPTH = 5
        q_dict = {}
        self.minimax(game_state, DEPTH, float('-inf'), float('inf'), True, q_dict=q_dict, initCall=True)
        
        max_actions = []
        max_v = float('-inf')
        for a,v in q_dict.items():
            if v > max_v:
                max_v = v
                max_actions = [a]
            elif v == max_v:
                max_actions.append(a)
        max_action = max_actions[0] if len(max_actions) == 1 else random.choice(max_actions)

        if self.debug:
            print("Action array:")
            for a,v in q_dict.items():
                print(a,":",v)
            print("Chosen action:", max_action, "with value", max_v)
        if self.render:
            return max_action, q_dict
        return max_action