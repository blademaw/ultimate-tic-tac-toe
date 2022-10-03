class Agent:
    def __init__(self, player):
        self.player = player

    def selectAction(self, actions, game_state):
        return actions[0]