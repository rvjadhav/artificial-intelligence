# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodLeft = sum(int(j) for i in newFood for j in i)

        if foodLeft > 0:
            foodDistances = [manhattanDistance(newPos, (x, y))
                              for x, row in enumerate(newFood)
                              for y, food in enumerate(row)
                              if food]
            shortestFood = min(foodDistances)
        else:
            shortestFood = 0

        if newGhostStates:
            ghostDistances = [manhattanDistance(ghost.getPosition(), newPos)
                               for ghost in newGhostStates]
            shortestGhost = min(ghostDistances)

            if shortestGhost == 0:
                shortestGhost = -2000
            else:
                shortestGhost = -5 / shortestGhost
        else:
            shortestGhost = 0

        return -2 * shortestFood + shortestGhost - 40 * foodLeft

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        def searchDepth(state, depth, agent):
            if agent == state.getNumAgents():
                if depth == self.depth:
                    return self.evaluationFunction(state)
                else:
                    return searchDepth(state, depth + 1, 0)
            else:
                actions = state.getLegalActions(agent)

                if len(actions) == 0:
                    return self.evaluationFunction(state)

                next_states = (
                    searchDepth(state.generateSuccessor(agent, action),
                                 depth, agent + 1)
                    for action in actions
                )

                return (max if agent == 0 else min)(next_states)

        return max(
            gameState.getLegalActions(0),
            key=lambda x: searchDepth(gameState.generateSuccessor(0, x), 1, 1)
        )

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def minVal(state, depth, agent, alpha, beta):
            if agent == state.getNumAgents():
                return maxVal(state, depth + 1, 0, alpha, beta)

            val = None
            for action in state.getLegalActions(agent):
                successor = minVal(state.generateSuccessor(agent, action), depth, agent + 1, alpha, beta)
                val = successor if val is None else min(val, successor)

                if alpha is not None and val < alpha:
                    return val

                beta = val if beta is None else min(beta, val)

            if val is None:
                return self.evaluationFunction(state)

            return val

        def maxVal(state, depth, agent, alpha, beta):
            assert agent == 0

            if depth > self.depth:
                return self.evaluationFunction(state)

            val = None
            for action in state.getLegalActions(agent):
                successor = minVal(state.generateSuccessor(agent, action), depth, agent + 1, alpha, beta)
                val = max(val, successor)

                if beta is not None and val > beta:
                    return val

                alpha = max(alpha, val)

            if val is None:
                return self.evaluationFunction(state)

            return val

        val, alpha, beta, best = None, None, None, None
        for action in gameState.getLegalActions(0):
            val = max(val, minVal(gameState.generateSuccessor(0, action), 1, 1, alpha, beta))
            # if val >= beta: return action
            if alpha is None:
                alpha, best = val, action
            else:
                alpha, best = max(val, alpha), action if val > alpha else best

        return best

    def average(lst):
        lst = list(lst)
        return sum(lst) / len(lst)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        def maxValue(state, currentDepth):
            currentDepth = currentDepth + 1
            if state.isWin() or state.isLose() or currentDepth == self.depth:
                return self.evaluationFunction(state)
            a = float('-Inf')
            for pAction in state.getLegalActions(0):
                a = max(a, expValue(state.generateSuccessor(0, pAction), currentDepth, 1))
            return a

        def expValue(state, currentDepth, ghostNum):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            a = 0
            for pAction in state.getLegalActions(ghostNum):
                if ghostNum == gameState.getNumAgents() - 1:
                    a = a + (maxValue(state.generateSuccessor(ghostNum, pAction), currentDepth)) / len(
                        state.getLegalActions(ghostNum))
                else:
                    a = a + (expValue(state.generateSuccessor(ghostNum, pAction), currentDepth, ghostNum + 1)) / len(
                        state.getLegalActions(ghostNum))
            return a

            # Body of expectimax starts here: #

        pacmanActions = gameState.getLegalActions(0)
        maximum = float('-Inf')
        maxAction = ''
        for action in pacmanActions:
            currentDepth = 0
            currentMax = expValue(gameState.generateSuccessor(0, action), currentDepth, 1)
            if currentMax > maximum or (currentMax == maximum and random.random() > .3):
                maximum = currentMax
                maxAction = action
        return maxAction


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    heuristic = 0

    for st in newScaredTimes:
        heuristic += st
        # print "st",st

    ghostDistances = []
    for gs in newGhostStates:
        ghostDistances += [manhattanDistance(gs.getPosition(), newPos)]
    # print "ghostDist",ghostDistances

    foodList = newFood.asList()

    wallList = currentGameState.getWalls().asList()

    emptyFoodNeighbors = 0
    foodDistances = []

    def foodNeighbors(foodPos):
        foodNeighbors = []
        foodNeighbors.append((foodPos[0] - 1, foodPos[1]))
        foodNeighbors.append((foodPos[0], foodPos[1] - 1))
        foodNeighbors.append((foodPos[0], foodPos[1] + 1))
        foodNeighbors.append((foodPos[0] + 1, foodPos[1]))
        return foodNeighbors

    for f in foodList:
        neighbors = foodNeighbors(f)
        for fn in neighbors:
            if fn not in wallList and fn not in foodList:
                emptyFoodNeighbors += 1
        foodDistances += [manhattanDistance(newPos, f)]
    # print "food",foodDistances

    inverseFoodDist = 0
    if len(foodDistances) > 0:
        inverseFoodDist = 1.0 / (min(foodDistances))

        # print "ifd",inverseFoodDist

        # print "st",newScaredTimes

    heuristic += (min(ghostDistances) * ((inverseFoodDist ** 4)))
    # heuristic += min(ghostDistances)*2
    heuristic += currentGameState.getScore() - (float(emptyFoodNeighbors) * 4.5)
    # print emptyFoodNeighbors,currentGameState.getScore(),currentGameState.getScore()-(float(emptyFoodNeighbors)*9),heuristic
    # heuristic *= 1.0/len(foodDistances)
    # heuristic -= inverseFoodDist**2
    # print "heuristic:",heuristic
    return heuristic
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

