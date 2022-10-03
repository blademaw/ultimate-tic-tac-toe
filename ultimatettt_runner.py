"""
Will eventually be used to run game(s) against two selected agents.
"""
from ultimatettt_model import *
from ultimatettt_utils import *
from example_boards import state_1, state_2, state_3
from optparse import OptionParser
import sys
from mcts_custom import mcts


def loadParameters():
    """
    Processes commands from command line.
    """
    usageStr = """
    USAGE:      python ultimatettt_runner.py <options>
    EXAMPLES:   (1) python ultimatettt_runner.py
                    - starts a game with two random agents.
                (2) python ultimatettt_runner.py -a MyAgent1,MyAgent2
                    - starts a fully automated game where MyAgent1 competes against MyAgent2.
    """
    parser = OptionParser(usageStr)
    parser.add_option('-a','--agents', help='Two agents separated by a comma to compete against each other.', default="agents.random,agents.random")

    options, unrec = parser.parse_args(sys.argv[1:])
    assert len(unrec) == 0, "Unrecognized options: " + str(unrec)
    print(options)
    return options


def run(options, msg):
    pass


if __name__ == '__main__':
    # msg = ""
    # options  = loadParameters()
    # matches = run(options, msg)

    # print("State 1:")
    # state_1.printBoard()
    # print("State 2:")
    # print(str(state_2))

    state_2_move = Action(1, 6, 2, 0)
    # print(f"Executing action: {str(state_2_move)}\n")
    state_2_prime = state_2.takeAction(state_2_move)

    print("State 2':")
    print(str(state_2_prime))

    ultimateMCTS = mcts(player=2, timeLimit = 1000)
    action, val = ultimateMCTS.search(initialState=state_2_prime, needDetails=True)

    # state_2_move_2 = Action(2, 6, 1, 0)
    # print(f"Executing action: {str(state_2_move_2)}\n")
    print(f"MCTS believes action {str(action)} is the best with expected return {val}.\nI think it's (2, 6, 1, 1).")
    state_2_prime_2 = state_2_prime.takeAction(action)
    # state_2_prime_2 = state_2_prime.takeAction(state_2_move_2)
    # state_2_prime_win = state_2_prime.takeAction(Action(2, 6, 1, 1))

    print("State 2'':")
    print(str(state_2_prime_2))

    # state_2_move_3 = Action(1, 1, 2, 2)
    # print(f"Executing action: {str(state_2_move_3)}\n")
    # state_2_prime_3 = state_2_prime_2.takeAction(state_2_move_3)

    # print("State 2''':")
    # print(str(state_2_prime_3))

    # state_2_move_4 = Action(2, 6, 1, 1)
    # print(f"Executing action: {str(state_2_move_4)}\n")
    # state_2_prime_4 = state_2_prime_3.takeAction(state_2_move_4)

    # print("State 2'''':")
    # print(str(state_2_prime_4))

    # print("State 3:")
    # print(str(state_3))