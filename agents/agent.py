class Agent:
    def __init__(self, player, debug=False, render=False):
        self.player = player
        self.debug = debug
        self.render = render

    def warmup(self, game_state):
        print(f"Warming up agent {self.player}")

    def selectAction(self, actions, game_state):
        if self.render:
            return actions[0], None
        return actions[0]