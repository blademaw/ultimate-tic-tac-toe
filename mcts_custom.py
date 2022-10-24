"""
MCTS single-agent code from https://github.com/pbsinclair42/MCTS
Adapted to retrieve agent-specific rewards and return action-E[reward] dictionary.
"""
from collections import defaultdict
from ultimatettt_model import Action

import time
import math
import random

import numpy as np

from ultimatettt_utils import winsTTTBoard


def randomPolicy(state, player,PRINTOUT):
    while not state.isTerminal():
        try:
            # selects random action, can be improved by heuristics

            action = random.choice(state.getPossibleActions())
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.takeAction(action)

    if PRINTOUT and action in (Action(2, 3, 0, 2), Action(2, 3, 1, 0), Action(2, 3, 1, 1)):
                print('determined reward of', state.getReward(player))
    #debugging
    # if state.getReward(player) == 1:
    #     print(state)
    if state.getReward(player) == 1:
        assert player == winsTTTBoard(state.squares.reshape((3,3)), True)
        if PRINTOUT:
            print(action)
    if PRINTOUT and state.getReward(player) == -1:
        return -1
    
    return state.getReward(player)


class treeNode():
    def __init__(self, state, parent):
        self.state = state
        self.isTerminal = state.isTerminal()
        self.isFullyExpanded = self.isTerminal
        self.parent = parent
        self.numVisits = 0
        self.totalReward = 0
        self.children = {}

    def __str__(self):
        s=[]
        s.append("totalReward: %s"%(self.totalReward))
        s.append("numVisits: %d"%(self.numVisits))
        s.append("isTerminal: %s"%(self.isTerminal))
        s.append("possibleActions: %s"%(self.children.keys()))
        return "%s: {%s}"%(self.__class__.__name__, ', '.join(s))


class mcts():
    def __init__(self, player, timeLimit=None, iterationLimit=None, explorationConstant=1 / math.sqrt(2),
                 rolloutPolicy=randomPolicy):
        if timeLimit != None:
            if iterationLimit != None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.timeLimit = timeLimit
            self.limitType = 'time'
        else:
            if iterationLimit == None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iterationLimit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iterationLimit
            self.limitType = 'iterations'
        self.explorationConstant = explorationConstant
        self.rollout = rolloutPolicy
        self.player = player

    def search(self, initialState, needDetails=False, returnDict=False):
        self.root = treeNode(initialState, None)

        if self.limitType == 'time':
            timeLimit = time.time() + self.timeLimit / 1000
            while time.time() < timeLimit:
                self.executeRound()
        else:
            for i in range(self.searchLimit):
                self.executeRound()

        if returnDict:
            bestChild, actionVals = self.getBestChild(self.root, 0, returnActions=True)
        else:
            bestChild = self.getBestChild(self.root, 0)
            
        action=(action for action, node in self.root.children.items() if node is bestChild).__next__()
        if returnDict:
            return action, actionVals
        if needDetails:
            # return {"action": action, "expectedReward": bestChild.totalReward / bestChild.numVisits}
            return action, bestChild.totalReward / bestChild.numVisits
        else:
            return action

    def executeRound(self):
        node = self.selectNode(self.root)
        if all(node.state.squares == np.array([2, 1, -1, 0, 2, 1, 2, -1, 1])):
            PRINTOUT = True
            print("current total reward is",node.totalReward)
        else:
            PRINTOUT = False
        reward = self.rollout(node.state, self.player,PRINTOUT)
        if PRINTOUT: print("node reward", reward)
        self.backpropagate(node, reward)

    def selectNode(self, node):
        while not node.isTerminal:
            if node.isFullyExpanded:
                node = self.getBestChild(node, self.explorationConstant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.state.getPossibleActions()
        for action in actions:
            if action not in node.children:
                newNode = treeNode(node.state.takeAction(action), node)
                node.children[action] = newNode
                if len(actions) == len(node.children):
                    node.isFullyExpanded = True
                return newNode

        raise Exception("Should never reach here")

    def backpropagate(self, node, reward):
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            node = node.parent

    def getBestChild(self, node, explorationValue, returnActions=False):
        bestValue = float("-inf")
        bestNodes = []
        x = -1 if node.state.getCurrentPlayer() != self.player else 1
        x=1
        printing=all(node.state.squares == np.array([2, 1, -1, 0, 2, 1, 2, -1, 1]))
        if returnActions:
            actionVals = {}

        for action, child in node.children.items():
            nodeValue = x* child.totalReward / child.numVisits + explorationValue * math.sqrt(
                2 * math.log(node.numVisits) / child.numVisits)

            if returnActions or printing:
                print(action, f"{x} * {child.totalReward} / {child.numVisits} + {explorationValue} * {math.sqrt(2 * math.log(node.numVisits) / child.numVisits)}")
                print(f"\t{nodeValue}")
            if returnActions:
                actionVals[action] = child.totalReward / child.numVisits

            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        if printing: print()
        
        if returnActions:
            return random.choice(bestNodes), actionVals
        
        return random.choice(bestNodes)