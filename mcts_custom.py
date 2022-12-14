"""
MCTS single-agent code from https://github.com/pbsinclair42/MCTS
Adapted to retrieve agent-specific rewards and return action-E[reward] dictionary.
"""
from __future__ import division
from collections import defaultdict

import time
import math
import random


def randomPolicy(state, player):
    while not state.isTerminal():
        try:
            action = random.choice(state.getPossibleActions())
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.takeAction(action)
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
    def __init__(self, player, timeLimit=None, iterationLimit=None, explorationConstant=1/math.sqrt(2),
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
        self.qtable = defaultdict(lambda: 0)

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
        reward = self.rollout(node.state, self.player)
        self.backpropagate(node, reward)

    def selectNode(self, node):
        while not node.isTerminal:
            if node.isFullyExpanded:
                # node = self.getBestChild(node, self.explorationConstant)
                # node = random.choice(list(node.children.items()))[1]
                node = self.UCB(node)
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

            # q_value = node.totalReward / node.numVisits # might not have to divide
            # delta = (1 / node.numVisits) * (reward - q_value)
            # node.totalReward += delta
            # print(delta)
            
            # q_value = self.qtable[hash(str(node.state))]
            # delta = (1 / node.numVisits) * (reward - q_value)
            # newQ = q_value + delta
            # self.qtable[hash(str(node.state))] = newQ

            node.totalReward += reward
            node = node.parent

    def UCB(self, node):
        maxVal = float("-inf")
        max_children = []

        for child in node.children.values():
            # if haven't seen action before, explore it
            if child.numVisits == 0:
                child.numVisits = 1
                return child
            
            # otherwise, use UCB formula
            value = 0
            if child.numVisits > 0:
                # UCT = win ratio + exploration * sqrt(log(parent visits)/child visits)
                value = (child.totalReward / child.numVisits) + \
                    (self.explorationConstant * math.sqrt(math.log(node.numVisits) / child.numVisits))
                #     (self.explorationConstant * math.sqrt(math.log(node.numVisits) / child.numVisits))
                # value = self.qtable[hash(str(child.state))] + \
                
                if value > maxVal:
                    max_children = [child]
                    maxVal = value
                elif value == maxVal:
                    max_children.append(child)
        
        return random.choice(max_children)



    def getBestChild(self, node, explorationValue, returnActions=False):
        bestValue = float("-inf")
        bestNodes = []
        if returnActions:
            actionVals = {}

        for action, child in node.children.items():
            nodeValue = child.totalReward / child.numVisits + explorationValue * math.sqrt(
                2 * math.log(node.numVisits) / child.numVisits)
            
            if returnActions:
                actionVals[action] = child.totalReward / child.numVisits

            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        
        if returnActions:
            return random.choice(bestNodes), actionVals
        
        return random.choice(bestNodes)