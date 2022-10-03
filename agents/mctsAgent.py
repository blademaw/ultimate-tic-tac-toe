from mcts_custom import mcts
from agents.agent import Agent

class playerAgent(Agent):
    def __init__(self, player, debug=False):
        super().__init__(player, debug=debug)
        self.mctsStruct = None
        self.initPlayer = player
        self.debug = debug

    def selectAction(self, actions, game_state):
        if self.mctsStruct is None:
            # this is the first time we are called, so we need to initialize the MCTS structure
            assert self.player == self.initPlayer
            self.mctsStruct = mcts(player=self.player, timeLimit = 1000)
        
        if self.debug:
            # action, val = self.mctsStruct.search(initialState=game_state, needDetails=True)
            # print(f"MCST chose action {action} with expected return {val}")

            action, actionVals = self.mctsStruct.search(initialState=game_state, returnDict=True)
            print("MCTS Action Reward Dist:")
            for a, v in actionVals.items():
                print(f"{a}: {v}")
            print("MCTS chose action", action, "with highest expected return",actionVals[action])

        else:
            action = self.mctsStruct.search(initialState=game_state)
        assert action in actions

        return action