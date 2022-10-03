class Agent:
    def __init__(self, player, debug=False):
        self.player = player
        self.debug = debug

    def selectAction(self, actions, game_state):
        return actions[0]