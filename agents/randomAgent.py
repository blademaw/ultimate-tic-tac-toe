import random
from agents.agent import Agent

class playerAgent(Agent):
    def selectAction(self, actions, game_state):
        return random.choice(actions)