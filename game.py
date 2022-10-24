from copy import deepcopy
from render_board import *
import os, datetime
import numpy as np

from ultimatettt_utils import winsTTTBoard

class Game:
    def __init__(self, game_rule, agents, agent_names, num_agents, game_index, options):
        for i, p in enumerate(agents): assert p.player-1 == i
        # TODO: refactor to use options instead of plethora of arguments
        self.game_rule = game_rule
        self.agents = agents
        self.agent_names = agent_names
        self.num_agents = num_agents
        self.game_index = game_index
        self.display_game = options.displayGame
        self.debug = options.debug
        self.render = options.render
        self.fileType = options.fileType
        self.warmup = options.warmup

        self.actionCounter = 0
        self.moves = np.zeros(3)

        self.renderBoard = RenderBoard()

        self.game_out_path = os.path.join("output", f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}", f"game_{self.game_index}")
        if self.render:
            for i in range(self.num_agents): os.makedirs(os.path.join(self.game_out_path, f"{i}"))

    def run(self):
        resigned = False

        if self.warmup:
            for a in self.agents:
                a.warmup(self.game_rule.current_state) # will always be initial state

        while not self.game_rule.gameEnds():
            # agent_index is randomly initialized, so Agent 1 goes first/second 50% of time
            agent_index = self.game_rule.getCurrentPlayer() - 1
            agent = self.agents[agent_index]
            # if self.display_game and self.actionCounter == 0:
            #     print(f"Agent {agent_index}, {self.agent_names[agent_index]} is going first.")
            #     self.actionCounter += 1

            game_state = self.game_rule.currentState

            actions = self.game_rule.getPossibleActions(game_state)

            if self.display_game:
                if self.debug:
                    print(self.game_rule.debugState())
                else: 
                    print(self.game_rule)
            
            if self.render:
                selected, rewardDict = agent.selectAction(deepcopy(actions), deepcopy(game_state))
                self.renderBoard.saveGameBoard(
                    deepcopy(game_state),
                    self.actionCounter,
                    self.game_out_path,
                    os.path.join(f"{agent_index}",f"{self.actionCounter}"),
                    rewardDict,
                    self.fileType
                )
            else:
                selected = agent.selectAction(deepcopy(actions), deepcopy(game_state))

            if selected == "resign":
                print(f"Agent {agent_index}, {self.agent_names[agent_index]} resigned.")
                winningPlayer = 3 - agent_index
                resigned = True
                break

            self.game_rule.update(selected)

            if self.display_game:
                # TODO: Put this in a Displayer class?
                print(f"Agent {self.agent_names[agent_index]} chooses square {selected.square}, cell ({selected.x},{selected.y}).")
            
            self.actionCounter += 1
            self.moves[agent_index + 1] += 1

        # TODO: turn this call into a better organized process (reshaping + calling WinsTTTBoard)
        if not resigned:
            winningPlayer = winsTTTBoard(deepcopy(self.game_rule.currentState.squares.reshape((3,3))), returnPlayer=True)
        
        # render end state of game
        if self.render:
            self.renderBoard.saveGameBoard(
                deepcopy(self.game_rule.currentState),
                self.actionCounter,
                self.game_out_path,
                os.path.join(f"{agent_index}",f"{self.actionCounter}"),
                None,
                self.fileType,
                True
            )

        if self.display_game:
            if self.debug:
                    print(self.game_rule.debugState())
            else: 
                print(self.game_rule)
        if winningPlayer is not None:
            print(f"Game {self.game_index+1} Result:\n\tAgent {winningPlayer-1}: {self.agent_names[winningPlayer-1]} wins.")
        else:
            print(f"Game {self.game_index+1} Result:\n\tthe game is a tie.")
        
        winningPlayer = winningPlayer if winningPlayer is not None else 0
        return winningPlayer, self.moves