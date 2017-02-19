# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
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
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()


class Node:
    def __init__(self, state, parent=None, cost=0, action=None):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.action = action


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def generic_search(problem, frontier, passcost=False):
    root = Node(problem.getStartState())

    # if root is a goal state already, just return empty list of moves
    if problem.isGoalState(root.state):
        return []

    frontier_states = set()
    explored_states = set()

    frontier_states.add(root.state)
    if passcost:
        frontier.push(root, 0)
    else:
        frontier.push(root)

    while True:
        if frontier.isEmpty():
            raise Exception('Empty frontier')

        node = frontier.pop()
        frontier_states.remove(node.state)
        explored_states.add(node.state)

        # Expand the node
        actions = problem.getSuccessors(node.state)
        for state, action, cost in actions:
            if (state in explored_states) or (state in frontier_states):
                continue

            if problem.isGoalState(state):
                solution = [action]
                backnode = node
                while backnode.parent is not None:
                    solution = [backnode.action] + solution
                    backnode = backnode.parent
                return solution

            child = Node(state, parent=node, action=action, cost=node.cost + cost)
            frontier_states.add(child.state)
            if passcost:
                frontier.push(child, node.cost + child.cost)
            else:
                frontier.push(child)


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    return generic_search(problem, util.Stack())


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    return generic_search(problem, util.Queue())


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    return generic_search(problem, util.PriorityQueue(), True)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    def astarcost(item):
        g = item.cost
        h = heuristic(item.state, problem)
        return g + h

    return generic_search(problem, util.PriorityQueueWithFunction(astarcost), False)
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
