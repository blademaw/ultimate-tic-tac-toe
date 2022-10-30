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
        # if we have a center avaiable, pick one.
        action_arr = []
        chosen_action = None

        for action in actions:
            if action.x == 1 and action.y == 1:
                action_arr.append(action)

        if len(action_arr) > 0:
            chosen_action = random.choice(action_arr)
        else:
            chosen_action = random.choice(actions)

        if self.render:
            return chosen_action, None
        return chosen_action