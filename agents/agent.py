class Agent:
    def __init__(self, player, debug=False, render=False):
        self.player = player
        self.debug = debug
        self.render = render

    def selectAction(self, actions, game_state):
        if self.render:
            return actions[0], None
        return actions[0]