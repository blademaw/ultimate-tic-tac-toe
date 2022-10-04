class Agent:
    def __init__(self, player, debug=False, render=False):
        self.player = player
        self.debug = debug
        self.render = render

    def selectAction(self, actions, game_state):
        return actions[0]