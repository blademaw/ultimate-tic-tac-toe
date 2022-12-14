from mcts_custom import mcts
from agents.agent import Agent

class playerAgent(Agent):
    def __init__(self, player, debug=False, render=False, runtime=1):
        super().__init__(player, debug=debug, render=render)
        self.mctsStruct = None
        self.initPlayer = player
        self.debug = debug
        self.render = render
        self.runtime = runtime
    
    def warmup(self, game_state):
        print("Warming up MCTS agent")
        assert self.mctsStruct is None
        self.mctsStruct = mcts(player=self.player, timeLimit = 150000) # 2.5min warmup

    def selectAction(self, actions, game_state):
        if self.mctsStruct is None:
            # this is the first time we are called, so we need to initialize the MCTS structure
            assert self.player == self.initPlayer
            self.mctsStruct = mcts(player=self.player, timeLimit = self.runtime*1000)
        
        
        if self.debug or self.render:
            # action, val = self.mctsStruct.search(initialState=game_state, needDetails=True)
            # print(f"MCST chose action {action} with expected return {val}")

            action, actionVals = self.mctsStruct.search(initialState=game_state, returnDict=True)
            if self.debug:
                print("MCTS Action Reward Dist:")
                for a, v in actionVals.items():
                    print(f"{a}: {v}")
                print("MCTS chose action", action, "with highest expected return",actionVals[action])

            if self.render:
                return action, actionVals

        else:
            action = self.mctsStruct.search(initialState=game_state)
        assert action in actions

        return action