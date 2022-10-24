from agents.agent import Agent
from ultimatettt_model import Action

class playerAgent(Agent):
    def __init__(self, player, debug=False, render=False):
        super().__init__(player, debug=debug, render=render)
        self.mctsStruct = None
        self.initPlayer = player
        self.debug = debug
        self.render = render
        
    def selectAction(self, actions, game_state):
        validInput = False
        while not validInput:
            try:
                humanString = input("Type action in form 'square, row, col' or 'resign': ")
                action = Action(self.player, *list(map(int,humanString.split(","))))
                if action in actions:
                    validInput = True
                else:
                    print("Not an available action.")
            except:
                if humanString == "resign":
                    action = humanString
                    validInput = True
                print("Invalid action. Please try again.")
        return action