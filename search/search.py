# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def generalSearch(problem, fringe):
    closed = []
    fringe.push([(problem.getStartState(), "Stop", 0)])
    while not fringe.isEmpty():
        path = fringe.pop()
        s = path[len(path) - 1]
        s = s[0]
        if problem.isGoalState(s):
            return [x[1] for x in path][1:]
        if s not in closed:
            closed.append(s)
            for successor in problem.getSuccessors(s):
                if successor[0] not in closed:
                    successorPath = path[:]
                    successorPath.append(successor)
                    fringe.push(successorPath)
    return []

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    fringe = util.Stack()
    return generalSearch(problem, fringe)
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    fringe = util.Queue()
    return generalSearch(problem, fringe)
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    return aStarSearch(problem);
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    p_q_of_states = util.PriorityQueue()
    closed_set = []
    closed_set.append(problem.getStartState())
    startSuccesors = problem.getSuccessors(problem.getStartState())
    for successor, action, cost in startSuccesors:
        path = []
        path.append(action)
        crnt_cost = cost + heuristic(successor, problem)
        p_q_of_states.push((successor, path, cost), crnt_cost)
    while not p_q_of_states.isEmpty():
        crnt_state, crnt_path, crnt_path_cost = p_q_of_states.pop()
        if problem.isGoalState(crnt_state):
            goal_path = crnt_path
            return goal_path
        if crnt_state not in closed_set:
            closed_set.append(crnt_state)
            successors = problem.getSuccessors(crnt_state)
            for successor, action, new_cost in successors:
                tmp_path = list(crnt_path)
                tmp_path.append(action)
                tmp_cost = crnt_path_cost + new_cost
                p_q_of_states.push((successor, tmp_path, tmp_cost), (tmp_cost + heuristic(successor, problem)))
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
