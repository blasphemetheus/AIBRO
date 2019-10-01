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
from game import Directions
import random


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


# --------------------------------------------------------------------
# MY STUFF ---- Data Structures and Objects and utils

class State(object):
    """
    A state is a representation of a Successor instance as found in Pacman.

    Equality is measured by the location, which is within the successor,
    not just by the successor with all of its elements.
    """
    def __init__(self, successorObject):
        """
        Creates a State with a given successor
        :param successorObject:
        """
        self.location = successorObject[0]
        self.direction = successorObject[1]
        self.cost = successorObject[2]

    def __eq__(self, other):
        """
        Returns whether this (self) State is equal to the given "other" thing, which we
        assume is another State. Equality is for us is exactly the same ignoring Cost.
        We are overriding the default equality function. We care about location and
        direction.

        :param other: the other State
        :return: whether this State and the other are equal
        """
        if not isinstance(other, State):
            return False

        if self.location == other.location and self.direction == other.direction:
            return True
        else:
            return False

    def sameLocation(self, other):
        """
        Returns whether this State is about the same location ignoring direction, cost.
        :param other: the other State
        :return:
        """
        if not isinstance(other, State):
            raise ValueError(
                "Should have passed in a State to compare for sameLocation:", other)

        if self.location == other.location:
            return True
        else:
            return False

# --------------------------------------------- MY STUFF Fns--------------


def get_state_of_direction(problem, current_location, next_move_direction):
    """
    returns the state of a direction by querying the current_location's successorlist
     hidden in problem

    :param current_location:
    :param next_move_direction:
    :return:
    """
    for successor in problem.getSuccessors(current_location):
        state = successor[0]
        direction = successor[1]
        cost = successor[2]

        if next_move_direction == direction:
            return state

    raise ValueError("There should be some state that corresponds to this direction :(",
                     direction)


# def stack_to_string(some_stack):
#
#     if isinstance(some_stack, util.Stack):
#         return str(some_stack.list)
# TODO: Remember to take out the change to util.py (added a toString to stack)


def this_visited(successor, visited):
    """
    Returns whether the given successor has been visited.
    :param successor: given successor (location, direction, cost)
    :param visited: a set of locations
    :return: a boolean, whether the successsor has a location in the set of visited
    """
    location = successor[0]
    return location in visited


def all_visited(successor_list, visited):
    """
    Returns whether they are all visited.

    :param successor_list: the list of successor states to check
    :param visited: the set of locations to check against
    :return: whether all them successor states have been visited (are in visited)
    """
    counter_bool = True
    # look through get successors, if we find the location is the same in
    for suc in successor_list:
        if this_visited(suc, visited):
            continue
        else:
            counter_bool = False
    return counter_bool


def fetch_direction(given_location, successor_list):
    """
    Returns a direction given a successor_list and given_location (the direction of that
    given_location in the successorList). Else it raises a ValueError.
    :param given_location: the given location (game.Directions)
    :param successor_list: the given successorList
    :return: the corresponding direction to the location provided
    """
    for suc in successor_list:
        suc_location = suc[0]
        suc_direction = suc[1]
        suc_cost = suc[2]

        if given_location == suc_location:
            return suc_direction
        else:
            continue
    raise ValueError("There was no direction corresponding to the given_location:",
                     given_location)


def fetch_location(given_direction, successor_list):
    """
    Returns a location given a successor_list and given_direction (the location of that
    given_direction in the successorList). Else it raises a ValueError.
    :param given_direction: the given direction
    :param successor_list: the given successor_list
    :return: stuff
    """
    for suc in successor_list:
        suc_location = suc[0]
        suc_direction = suc[1]

        if given_direction == suc_direction:
            return suc_location
        else:
            continue
    raise ValueError(
        "There was no location for the given Direction in the successorList")


def gimme_unvisited_location(visited, successor_list):
    """
    Returns an unvisited location in the successor_list. Raises a ValueError if it does
    not find an unvisited location in successor_list. Checks whether location is visited
    using visited.

    :param visited: a set of locations
    :param successor_list:
    :return:
    """
    for suc in successor_list:
        location = suc[0]

        if location in visited:
            # state has been visited, so we shouldn't go there unless by backtracking.
            # We know there is an unvisited location at this level of the successor_list
            # so we continue in the for loop until we find it
            continue
        else:
            # state has not been visited, so we should go there
            gonna_move_to = location
            return gonna_move_to
    raise ValueError("There should be a location in the given successor_list that has "
                     "not been visited but it seems like there was not")


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first. graph search algorithm, not tree
    search. The Fringe is not really used here. Expansion happens when finding a new
    move to make basically. If there are no new moves, then backtrack until there is a
    new move. Maintain a set of visited locations to check against.

    returns a list of actions to get to the goal (in the form of a List), which we
    maintain as a Stack (LIFO)

    Picks randomly from the successors when finding a new move (not backtracking).
    """
    current_location = problem.getStartState()
    fringe = util.Stack()
    # first state added to visited first
    visited = set()
    path = util.Stack()

    # Start the While Loop
    going = True
    while going:
        # add this location to the visited set
        visited.add(current_location)

        # quality of life prints
        print("")
        print("Current Location:", current_location)
        print("Current Successors:", problem.getSuccessors(current_location))

        # check for goalState
        if problem.isGoalState(current_location):
            print("Found Goal State: the path to get there was:", path.list)
            return path.list

        # NOT GOALSTATE, NOW DOING Expansion (depth first search expansion of fringe)
        # check for candidates for expansion
        if len(problem.getSuccessors(current_location)) == 0:
            print("Failure, No Successors.")
            raise ValueError("Failure, initialized to a disconnected node that isn't "
                             "goalstate")

        # For DFS we expand the fringe in a sort of non-explicit way, the successors
        # we have access to
        #expand_fringe(problem, current_location, visited, fringe)
        # check if all successors have been visited
        if all_visited(problem.getSuccessors(current_location), visited):
            # all successors have been visited, so we BACKTRACK
            # no checking of the fringe at this stage for DFS :)
            print("Backtracking")
            previous_move_direction = path.pop()
            print("Previous Move Dir:", previous_move_direction)
            print("Path:", path.list)
            next_move_direction = Directions.REVERSE[previous_move_direction]

            next_move_location = fetch_location(next_move_direction,
                                                        problem.getSuccessors(
                                                            current_location))

            # the important bit, the move, the backtrack, the mutation
            current_location = next_move_location
            # take us to next iteration of while loop pls!
            continue
        else:
            # There is a candidate for new expansion on this level (unvisited successor)
            print("Moving to new expansion")
            shuffled_successor_list = problem.getSuccessors(current_location)
            random.shuffle(shuffled_successor_list)

            # go through and find an unvisited location, travel there
            desired_location = gimme_unvisited_location(visited, shuffled_successor_list)

            desired_direction = fetch_direction(desired_location,
                                                problem.getSuccessors(current_location))

            # ACTUALLY DO THE MOVE
            path.push(desired_direction)
            current_location = desired_location
            print("Path:", path.list)
            continue


def expand_fringe(problem, current_location, visited, fringe):
    """
    Expands the fringe according to DFS search.

    Makes sure the visited set has the current_location, adds the successors to the fringe
    if they aren't already there.

    :param problem:
    :param current_location:
    :param visited:
    :param fringe:
    :return:
    """
    #  Make sure visited AND fringe are populated/updated, generate possible_move_set
    # ---------------------------
    # adjust visited
    visited.add(current_location)
    print("Visited is: ", visited)

    # Calculating possible_move_set  ....
    for suc in problem.getSuccessors(current_location):
        location = suc[0]
        last_seen_but_not_visited = fringe.pop()
        if last_seen_but_not_visited == location:
            fringe.push(last_seen_but_not_visited)
        else:
            fringe.push(last_seen_but_not_visited)
            pass

    successor_state_set = retrieve_states(problem.getSuccessors(current_location))
    print("Successors with Direction:", problem.getSuccessors(current_location))
    print("Successor States:", successor_state_set)
    possible_new_move_set = set.difference(successor_state_set, visited)
    print("The set of untraveled states that are possible rn:", possible_new_move_set)

    fringe = adjustFringeDFS(fringe, visited, problem.getSuccessors(current_location))
    print("Current Fringe:", fringe)

# def checkForCurrentSuccessors(problem, current_location):

def stateAlreadyVisited(successor, visited):
    state = successor[0]
    return state in visited


''' ----------------------------------------------- '''


def adjustFringeDFS(fringe, visited, successor_list) -> set:
    """
    returns an adjusted fringe for DFS
    """
    possibleNextStates = set()
    for possibleMove in successor_list:
        possibleState = possibleMove[0]
        possibleNextStates.add(possibleState)

    fringe.update(possibleNextStates)
    fringe.difference_update(visited)
    return fringe


def adjustFringeBFS(fringe, visited, successor_list) -> set:
    """
    returns an adjusted Fringe for BFS
    :param fringe:
    :param visited:
    :param successor_list:
    :return:
    """
    possibleNextStates = set()
    for possibleMove in successor_list:
        possibleState = possibleMove[0]
        possibleNextStates.add(possibleState)

    fringe.update(possibleNextStates)
    fringe.difference_update(visited)
    return fringe


def retrieve_states(successor_list):
    """
    return all the states extracted from the given successor_list
    :param successor_list:
    :return:
    """
    accumulating_set = set()

    for successor in successor_list:
        state = successor[0]
        direction = successor[1]
        cost = successor[2]
        accumulating_set.add(state)

    return accumulating_set
#  ----------------------------------------------------------


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    Uses a Fifo data structure (queue), expands fringe at a different time
    """
    current_location = problem.getStartState()
    fringe = util.Queue()
    visited = util.Queue()

    # Start the While Loop
    going = True
    while going:
        # add this location to the visited set
        visited.push(current_location)

        # quality of life prints
        print("")
        print("Current Location:", current_location)
        print("Current Successors:", problem.getSuccessors(current_location))

        # check for goalState
        if problem.isGoalState(current_location):
            print("Found Goal State: the path to get there was:", visited.list)
            return visited

        # NOT GOALSTATE, NOW DOING Expansion (depth first search expansion of fringe)
        # check for candidates for expansion
        if len(problem.getSuccessors(current_location)) == 0:
            print("Failure, No Successors.")
            raise ValueError("Failure, initialized to a disconnected node that isn't "
                             "goal-state")

        # For BFS we expand the fringe, so when can see them we expand them?

        print("All them Successors:", problem.getSuccessors(current_location))

        # todo: fringe expansion might be non-literally a fn, more of a task
        #expand_fringe(problem, current_location, visited, fringe)
        # check if all successors have been visited, if so then
        #   continue after moving to the next thing in queue
        if all_visited(problem.getSuccessors(current_location), visited):
            # all successors have been visited, so we MOVE ON
            print("MOVING ON")
            previous_move_direction = path.pop()
            print("Previous Move Dir:", previous_move_direction)
            print("Path:", path.list)
            next_move_direction = Directions.REVERSE[previous_move_direction]

            next_move_location = fetch_location(next_move_direction,
                                                        problem.getSuccessors(
                                                            current_location))

            # the important bit, the move, the backtrack, the mutation
            current_location = next_move_location
            # take us to next iteration of while loop pls!
            continue
        else:
            # There is a candidate for new expansion on this level (unvisited successor)
            print("Moving to new expansion")
            shuffled_successor_list = problem.getSuccessors(current_location)
            random.shuffle(shuffled_successor_list)

            # go through and find an unvisited location, travel there
            desired_location = gimme_unvisited_location(visited, shuffled_successor_list)

            desired_direction = fetch_direction(desired_location,
                                                problem.getSuccessors(current_location))

            # ACTUALLY DO THE MOVE
            path.push(desired_direction)
            current_location = desired_location
            print("Path:", path.list)
            continue

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



# def recursiveDepthLimitSearch(node, problem, limit):
#     '''
#     returns a sol or failure/cutoff
#     '''
#     if problem.GoalTest(node.state):
#         return Solution(node)
#     elif limit == 0:
#         return cutoff
#     else:
#         cutoffOccured = False
#         for action in problem.Actions(node.State):
#             child = ChildNode(problem, node, action)
#             result = recursiveDepthLimitSearch(child, problem, limit - 1)
#             if result == cutoff:
#                 cutoffOccured = True
#             elif result != failure:
#                 return result
#         if cutoffOccured:
#             return cutoff
#         else:
#             return failure
#
#     "*** YOUR CODE HERE ***"
#     util.raiseNotDefined()




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
