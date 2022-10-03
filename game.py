from copy import deepcopy

from ultimatettt_utils import winsTTTBoard

class Game:
    def __init__(self, game_rule, agents, agent_names, num_agents, game_index, display_game=True, debug=False):
        for i, p in enumerate(agents): assert p.player-1 == i
        
        self.game_rule = game_rule
        self.agents = agents
        self.agent_names = agent_names
        self.num_agents = num_agents
        self.game_index = game_index
        self.display_game = display_game
        self.debug = debug
        self.actionCounter = 0

    def run(self):
        while not self.game_rule.gameEnds():
            # agent_index is randomly initialized, so Agent 1 goes first/second 50% of time
            agent_index = self.game_rule.getCurrentPlayer() - 1
            agent = self.agents[agent_index]
            if self.display_game and self.actionCounter == 0:
                print(f"Agent {agent_index}, {self.agent_names[agent_index]} is going first.")
                self.actionCounter += 1

            game_state = self.game_rule.currentState

            actions = self.game_rule.getPossibleActions(game_state)

            if self.display_game:
                if self.debug:
                    print(self.game_rule.debugState())
                else: 
                    print(self.game_rule)
            
            selected = agent.selectAction(deepcopy(actions), deepcopy(game_state))

            self.game_rule.update(selected)

            if self.display_game:
                # TODO: Put this in a Displayer class?
                print(f"Agent {self.agent_names[agent_index]} chooses square {selected.square}, cell ({selected.x},{selected.y}).")

        # TODO: turn this call into a better organized process (reshaping + calling WinsTTTBoard)
        winningPlayer = winsTTTBoard(deepcopy(self.game_rule.currentState.squares.reshape((3,3))), returnPlayer=True)
        
        if self.display_game:
            if self.debug:
                    print(self.game_rule.debugState())
            else: 
                print(self.game_rule)
        if winningPlayer is not None:
            print(f"Game {self.game_index+1} Result:\n\tAgent {winningPlayer-1}: {self.agent_names[winningPlayer-1]} wins.")
        else:
            print(f"Game {self.game_index+1} Result:\n\tthe game is a tie.")
        
        return winningPlayer if winningPlayer is not None else 0