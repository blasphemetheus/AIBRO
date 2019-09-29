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
from enum import Enum
from game import Directions


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
    return [s, s, w, s, w, w, s, w]

#-------------------------------------------------
# MY STUFF

# todo: Go through and purge all references to path.list because I added that :>),
#  run with it deleted from util.py

def validate_direction(potentialDirection):
    if isinstance(potentialDirection, str):
        validDirection = set([Directions.SOUTH, \
        Directions.NORTH, Directions.EAST,\
        Directions.WEST])
        if potentialDirection in validDirection:
            return True
        else:
            raise ValueError(potentialDirection, "not a valid Directions")
    else:
        raise ValueError(potentialDirection, "not a str")

def opposite_direction(dir):
    if validate_direction(dir):
        if dir == Directions.NORTH:
            return Directions.SOUTH
        elif dir == Directions.SOUTH:
            return Directions.NORTH
        elif dir == Directions.EAST:
            return Directions.WEST
        elif dir == Directions.WEST:
            return Directions.EAST
        else:
            raise ValueError("Should Never Happen, problem in validate_direction")

def retrieve_states(successor_list):
    accumulating_set = set()
    for successor in successor_list:
        state = successor[0]
        direction = successor[1]
        cost = successor[2]
        accumulating_set.add(state)
    return accumulating_set

def get_state_of_direction(problem, current_state, next_move_direction):
    """
    returns the state of a direction by querying the current_state's successorlist hidden in problem

    :param current_state:
    :param next_move_direction:
    :return:
    """
    for successor in problem.getSuccessors(current_state):
        state = successor[0]
        direction = successor[1]
        cost = successor[2]

        if next_move_direction == direction:
            return state

    raise ValueError("There should be some state that corresponds to this direction :(", direction)


def stack_to_string(some_stack):
    if isinstance(some_stack, util.Stack):
        return str(some_stack.list)


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
    current_state = problem.getStartState()
    fringe = set()
    visited = set()
    path = util.Stack()

    count = 0
    while True:

        #TODO:::: make it so that it picks randomly from the list always when picking the next fn, so doesn't always backtrack
        # the same way and also doesn't always pick from the list of successors in the same way, also put the
        # stuff into functions.
        print("loop")
        # TODO:  remove count check
        if count > 100000:
            return
        else:
            print("")
            print("Run Number:", count + 1)
        # ------------ delete above til the loop start ---------------

        # current_state
        print("Current State:", current_state)

        # ---------------------------------------------
        # check for goalState
        # --------------------------------------------
        if problem.isGoalState(current_state):
            print("the state reached is goal state:", current_state)
            print("the path to get there was:", path.list)
            return path.list

        #_______________________________________________
        # NOT GOALSTATE, NOW DOING DFS EXPANSION
        #_______________________________________________

        #  Make sure visited AND fringe are populated/updated, generate possible_move_set
        # ---------------------------
        print(current_state, "Not Goalstate.")
        # adjust visited
        visited.add(current_state)

        print("Visited is: ", visited)

        # Calculating possible_move_set  ....
        successor_state_set = retrieve_states(problem.getSuccessors(current_state))
        print("Successors with Direction:", problem.getSuccessors(current_state))
        print("Successor States:", successor_state_set)
        possible_new_move_set = set.difference(successor_state_set, visited)
        print("The set of untraveled states that are possible rn:", possible_new_move_set)

        fringe = adjustFringe(fringe, visited, problem.getSuccessors(current_state))
        print("Current Fringe:", fringe)
        print("Current Path:", path.list)

        #    CHECK if there are no more candidates for expansion
        # --------------------------------------------------------
        if len(possible_new_move_set) == 0:
            print("There are no unvisited Successor Candidates")
            # We check that there is still a fringe, and if there isn't we return failure'
            if len(fringe) == 0:
                return "Failure - Ran out of fringe - No more possible new states to move to"
            else:
                print("BackTrack One")
                print("Path", path.list)
                previous_move_direction = path.pop()
                next_move_direction = opposite_direction(previous_move_direction)

                next_move_to = None
                for successor in problem.getSuccessors(current_state):
                    state = successor[0]
                    direction = successor[1]
                    cost = successor[2]

                    if next_move_direction == direction:
                        next_move_to = state
                        break
                    else:
                        continue

                if next_move_to is None:
                    raise ValueError("Despite getting to this Point, there is not move to reverse direction?")
                # ACTUALLY DO THE MOVE (BACKTRACK)
                print("--Backtracking", next_move_direction, "to", next_move_to)
                current_state = moveToSuccessor(successor)
                path.push(direction)
        else:
            print("there are unvisited successor candidates")
            # MOVING TO THIS NEW STATE

            # There is a candidate for new expansion on this level
            # ----------------------------------------------------
            #     Go Through Successors and do stuff

            gonna_move_to = None
            for successor in problem.getSuccessors(current_state):
                state = successor[0]
                direction = successor[1]
                cost = successor[2]

                if gonna_move_to is None:
                    # no previous move decided on
                    if state in visited:
                        # state has been visited, shouldn't travel to by this method, should be a backtracking
                        # movement, continue to next iteration of for loop
                        continue
                    else:
                        # state has not been visited, can travel to, so that's where we go
                        # set gonna_move_to and break out of for loop
                        gonna_move_to = state
                        break
                else:
                    # an iteration of the for loop has been found where gonna_move_to aint none
                    raise ValueError("Should Never Reach because gonna_move_to should always be None at this point")
            print("oUT of the For Loop")

            if gonna_move_to is None:
                 raise ValueError(gonna_move_to, "is null when it shouldn't be - there is a way to move to a new place")
            else:
                gonna_move_dir = None

                for successor in problem.getSuccessors(current_state):
                    state = successor[0]
                    direction = successor[1]
                    cost = successor[2]

                    if gonna_move_to == state:
                        gonna_move_dir = direction
                        break
                    else:
                        continue

                if gonna_move_dir is None:
                    raise ValueError("No Direction found to go along with given state moving to")

                print("--Moving", gonna_move_dir, "to", gonna_move_to)
                current_state = moveToSuccessor(successor)
                path.push(gonna_move_dir)


        #todo : define a data abstraction of path that is useful
        # actually do the move, remember to change path

        # At the Main Main loop yo
        print("Path:", path.list)
        count += 1

# def checkForCurrentSuccessors(problem, current_state):

def stateAlreadyVisited(successor, visited):
    state = successor[0]
    return state in visited


''' ----------------------------------------------- '''
def adjustFringe(fringe, visited, successor_list):
    """
    returns an adjusted fringe
    """
    possibleNextStates = set()
    for possibleMove in successor_list:
        possibleState = possibleMove[0]
        possibleNextStates.add(possibleState)

    fringe.update(possibleNextStates)
    fringe.difference_update(visited)
    return fringe

''' ---------------------------------------------------------- '''

def valid_path_to(cur_state, next_move_state, path):
    """
    reverses the path taken to get to the next_move_state, adding to the path along the way
    :param cur_state:
    :return:
    """
    #some magic to reverse to the next_move_state
    #path is added to at every step to get there or something

    # problem.getSuccessors(current_state)
    # print("Previous Move", previousMove)
    # # todo: WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO do backtrack
    return cur_state, path
def moveToSuccessor(successor):
    """
    returns the new state (meant to mutate current_state to become), also pushes a direction into path
    """
    state = successor[0]
    direction = successor[1]
    cost = successor[2]
    validate_direction(direction)
    return state

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
