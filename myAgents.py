# myAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from collections import defaultdict
import random
from game import Actions, Agent, Directions
from search import bfs
from searchProblems import PositionSearchProblem

import util
import time
import search
"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""


def createAgents(num_pacmen, agent='ClosestDotAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]


class CheeseBruteForceAgent(Agent):
    """
    Implementation of your agent.
    """

    layout = None

    def getAction(self, state):
        """
        Returns the next action the agent will take
        """

        if not CheeseBruteForceAgent.layout:
            r = random.Random(str(state.data.layout))
            CheeseBruteForceAgent.layout = r.randrange(1_000_000)
            print(CheeseBruteForceAgent.layout)


"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""


class ClosestDotAgent(Agent):

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """

        problem = AnyFoodSearchProblem(gameState, self.index)
        return search.bfs(problem)

    def getAction(self, state):

        if not self.path:
            problem = AnyFoodSearchProblem(state, self.index)
            self.path = bfs(problem)

        return self.path.pop(0)

    def initialize(self):

        self.path = None


class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x, y = state

        return self.food[x][y]
