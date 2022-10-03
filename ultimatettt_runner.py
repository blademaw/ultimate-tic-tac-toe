"""
Will eventually be used to run game(s) against two selected agents.
"""
import importlib
from ultimatettt_model import *
from ultimatettt_utils import *
from game import *
from example_boards import state_1, state_2, state_3
from optparse import OptionParser
import sys,traceback


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
    parser.add_option('-a','--agents', help='Two agents separated by a comma to compete against each other.', default="agents.randomAgent,agents.randomAgent")
    parser.add_option('-n','--agent_names',help='Names for agents separated by a comma.', default='')
    parser.add_option('-p','--displayGame', action='store_true', help='Display board output.', default=False)
    parser.add_option('-g','--gameRepeat',type='int',help='Number of games to run.', default=1)

    options, unrec = parser.parse_args(sys.argv[1:])
    assert len(unrec) == 0, "Unrecognized options: " + str(unrec)
    # print(options)
    return options


def loadAgents(match_dict):
    agents = [None] * len(match_dict['agents'])

    for i in range(len(agents)):
        cur_agent = None
        try:
            agentModule = importlib.import_module(match_dict['agents'][i])
            cur_agent = agentModule.playerAgent(i+1) # init agent with ID
        except (NameError, ImportError, IOError):
            print(f"Error: Agent {match_dict['agents'][i]} could not be loaded.",
                    traceback.print_exc())

        if cur_agent is not None:
            agents[i] = cur_agent
    
    return agents


def run(options):
    num_agents = 2
    scores = [0,0,0] # indices 0=tie;1=win for p1;2= win for p2

    agent_names = [] if options.agent_names == '' else options.agent_names.split(",")
    agents = options.agents.split(",")

    for i in range(num_agents - len(agent_names)):
        # agent_names.append(f"player{i+1}") # fill in missing agent names
        agent_names.append(f"{agents[i].split('.')[-1]}")

    match_dict = {}
    match_dict.update({"agents": agents})
    match_dict.update({"agent_names": agent_names})
    match_dict.update({"games": options.gameRepeat})


    for game_index in range(options.gameRepeat):
        game_rule = UltimateTTTRule()
        
        loaded_agents = loadAgents(match_dict)

        for i in range(num_agents):
            print(f"Agent {i}: {match_dict['agents'][i]} loaded.")

        game_obj = Game(
            game_rule,
            loaded_agents,
            agent_names,
            num_agents,
            game_index,
            options.displayGame
        )

        res = game_obj.run() # will be winning agent_index

        scores[res] += 1
    
    print(f"\nResults for {sum(scores)} games:")
    for i in range(1,num_agents+1):
        print(f"\tAgent {agent_names[i-1]} won {scores[i]} games ({100*scores[i]/sum(scores)}%)")


if __name__ == '__main__':
    options  = loadParameters()
    matches = run(options)