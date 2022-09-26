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
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    
    "*** YOUR CODE HERE ***"

    init_node = (problem.getStartState(), [])
    frontier = [init_node]
    explored = set()
    while len(frontier) != 0:
        curr_node = frontier.pop(len(frontier) - 1)
        curr_node_state = curr_node[0]
        curr_node_path = curr_node[1]
        explored.add(curr_node_state)
        if problem.isGoalState(curr_node_state):
            return curr_node_path

        children = problem.getSuccessors(curr_node_state)
        for (next_state, action, cost) in children:
            if next_state not in explored:
                for node in frontier:
                    if node[0] == next_state:
                        frontier.remove(node)
                frontier.append((next_state, curr_node_path + [action]))
    return []

    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    init_node = (problem.getStartState(), [])  # node stores its state and actions leading to the node from the root

    frontier = [init_node]
    explored = set()

    while len(frontier) != 0:
        curr_node = frontier.pop(0)
        curr_node_state = curr_node[0]
        curr_node_path = curr_node[1]
        explored.add(curr_node_state)

        if problem.isGoalState(curr_node_state):
            return curr_node_path

        children = problem.getSuccessors(curr_node_state)  # successors() returns a tuple of (state, directions, cost)
        for (next_state, action, cost) in children:
            if next_state not in explored:
                contain_node = False
                for node in frontier:
                    if node[0] == next_state:
                        contain_node = True
                if not contain_node:
                    frontier.append((next_state, curr_node_path + [action]))
    return []  # returns no actions

    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    # node store state, path cost, and path
    init_node = (problem.getStartState(), 0, [])

    frontier = util.PriorityQueue()
    frontier.push(init_node, init_node[1])
    explored = set()

    while not frontier.isEmpty():
        curr_node = frontier.pop()
        curr_node_state = curr_node[0]
        curr_node_cost = curr_node[1]
        curr_node_path = curr_node[2]
        explored.add(curr_node_state)

        if problem.isGoalState(curr_node_state):
            return curr_node_path

        children = problem.getSuccessors(curr_node_state)  # successors() returns a tuple of (state, directions, cost)
        for (child_state, action, cost) in children:

            next_cost = curr_node_cost + cost
            next_path = curr_node_path + [action]
            next_node = child_state, next_cost, next_path

            queue_heap = frontier.heap     # entry = (priority, self.count, item) item is node (state, cost, path)

            if child_state not in explored:
                if child_state not in (heap_state[2][0] for heap_state in queue_heap):
                    frontier.push(next_node, next_cost)

                elif child_state in (heap_state[2][0] for heap_state in queue_heap):
                    for entry in queue_heap:
                        if entry[2][0] == child_state and entry[0] > next_cost:
                            frontier.update(next_node, next_cost)

    return []

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

    initial_state = problem.getStartState()
    init_node = (initial_state, [], 0)   # (state, path, cost)
    frontier = util.PriorityQueue()
    frontier.push(init_node, heuristic(initial_state, problem))  # frontier entries consist of tuples: (priority, self.count, item)
    explored = set()

    while not frontier.isEmpty():
        curr_node = frontier.pop()
        curr_node_state = curr_node[0]
        curr_node_path = curr_node[1]
        curr_node_cost = curr_node[2]
        explored.add(curr_node_state)

        if problem.isGoalState(curr_node_state):
            return curr_node_path

        children = problem.getSuccessors(curr_node_state)
        for (next_state, action, step_cost) in children:
            next_cost = curr_node_cost + step_cost
            next_path = curr_node_path + [action]
            next_node = (next_state, next_path, next_cost)
            next_priority = next_cost + heuristic(next_state, problem)

            queue_heap = frontier.heap

            if next_state not in explored:
                if next_state not in (heap_state[2][0] for heap_state in queue_heap):
                    frontier.push(next_node, next_priority)

                elif next_state in (heap_state[2][0] for heap_state in queue_heap):
                    for entry in queue_heap:
                        if entry[2][0] == next_state and entry[0] > next_priority:
                            frontier.update(next_node, next_priority)

    return []

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
