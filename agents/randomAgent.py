import random
from agents.agent import Agent

class playerAgent(Agent):
    def __init__(self, player, debug=False, render=False):
        super().__init__(player, debug=debug, render=render)
        self.mctsStruct = None
        self.initPlayer = player
        self.debug = debug
        self.render = render
        
    def selectAction(self, actions, game_state):
        if self.render:
            return random.choice(actions), None
        return random.choice(actions)