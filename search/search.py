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

def depthFirstSearch(problem):
    """
    returns a sol or failure/cutoff
    """
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    from game import Directions
    return treeSearch(problem, "dfs")

    print("Start:", problem.getStartState)
    thing = util.stack
    thing.pop
    thing = util.stack()
    thing.heappop

    return recursiveDepthLimitSearch(node, problem, limit)


def treeSearch(problem, strategy):
    """
    returns a sol or failure
    """
    # so the solution (the list of directions is actually a stack) we return it
    # as a list when we return it

    # so the fringe is something else, it's just a bunch of nodes that we can
    # reach, which one we expand first is decided by the search algorithm, so
    # for this one, I'm expanding one of them, then always expanding one of the
    # sucessors if they are there, then expanding etc, and if there are none
    # then I go backwards one layer and maintain a list of already-checked nodes,
    # checking them for equality in the list of checked before adding new ones

    # it's lit
    
    # initialize the search tree using the initial state of problem
    currentState = problem.getStartState()
    print("Start State:", currentState)
    fringe = util.Stack()
    print(problem.getSuccessors(currentState))
    solution = util.Stack()

    while True:
        # noCandidatesForExpansion
        successorList = problem.getSuccessors(currentState)

        if len(successorList) == 0:
            print("should return failure")
            return "failure"
        if strategy == "bfs":
            print("do bfs expansion")
        elif strategy == "dfs":
            print("do dfs expansion")

        if problem.isGoalState(problem.getStartState()):
            print("start state is goal state")
            return solution
        else:
            newNodes = problem.getSuccessors(currentState)
            fringe.push(newNodes)

def recursiveDepthLimitSearch(node, problem, limit):
    '''
    returns a sol or failure/cutoff
    '''
    if problem.GoalTest(node.state):
        return Solution(node)
    elif limit == 0:
        return cutoff
    else:
        cutoffOccured = False
        for action in problem.Actions(node.State):
            child = ChildNode(problem, node, action)
            result = recursiveDepthLimitSearch(child, problem, limit - 1)
            if result == cutoff:
                cutoffOccured = True
            elif result != failure:
                return result
        if cutoffOccured:
            return cutoff
        else:
            return failure

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
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
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
