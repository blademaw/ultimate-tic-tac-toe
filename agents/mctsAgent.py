from mcts_custom import mcts
from agents.agent import Agent

class playerAgent(Agent):
    def __init__(self, player):
        super().__init__(player)
        self.mctsStruct = None
        self.initPlayer = player

    def selectAction(self, actions, game_state):
        if self.mctsStruct is None:
            # this is the first time we are called, so we need to initialize the MCTS structure
            assert self.player == self.initPlayer
            self.mctsStruct = mcts(player=self.player, timeLimit = 1000)
        
        # action, val = self.mctsStruct.search(initialState=game_state, needDetails=True)
        action = self.mctsStruct.search(initialState=game_state)
        assert action in actions

        # print(f"MCST chose action {action} with expected return {val}")

        return action