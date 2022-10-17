import sys
from random import choice
from collections import deque

class EightPuzzle:
    def __init__(self, initial_state=[], goal_state=[]):
        self.initial = initial_state
        self.goal = goal_state

    @staticmethod
    def shuffle(arr):
        for _ in range(10):
            legal_actions = list(EightPuzzle().Action(tuple(arr)))
            print('legal actions: ', legal_actions)
            action = choice(legal_actions)
            arr = EightPuzzle().Result(tuple(arr), action)
            print(arr)
        return arr

    def Action(self, state):
        possible_action = {'UP','DOWN','RIGHT','LEFT'}
        blank_id = state.index(0)
        if (blank_id % 3 == 0):
            possible_action.remove('LEFT')
        if (blank_id % 3 == 2):
            possible_action.remove('RIGHT')
        if (blank_id / 3 < 1):
            possible_action.remove('UP')
        if (blank_id / 3 >= 2):
            possible_action.remove('DOWN')
        return possible_action

    def Result(self, state, action):
        state = list(state)
        blank_id = state.index(0)
        if (action == 'UP'):
            state[blank_id], state[blank_id-3] = state[blank_id-3], state[blank_id]
        if (action == 'DOWN'):
            state[blank_id], state[blank_id+3] = state[blank_id+3], state[blank_id]
        if (action == 'LEFT'):
            state[blank_id], state[blank_id-1] = state[blank_id-1], state[blank_id]
        if (action == 'RIGHT'):
            state[blank_id], state[blank_id+1] = state[blank_id+1], state[blank_id]
        return tuple(state)

    def Goal_test(self, state):
        return (state == self.goal)

class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        if (parent):
            self.depth = parent.depth
        else:
            self.depth = 0

    def Child_node(self, action, problem):
        return Node(problem.Result(self.state,action), self, action, self.cost)

    def Expand(self, problem):
        """
        Get all possible state of the ::problem
        """
        List_successor = []
        possible_action = problem.Action(self.state)
        for action in possible_action:
            List_successor.append(self.Child_node(action,problem))
        return List_successor

    def Solution(self):
        node, solution = self, []
        while (node.parent):
            solution.append(node.action)
            node = node.parent
        return list(reversed(solution))

class BFS:
    def __init__(self, problem):
        self.solution = self.breadth_first_graph_search(problem).Solution()

    def breadth_first_graph_search(self,problem):
        node = Node(problem.initial)
        if problem.Goal_test(node.state):
            return node
        frontier = deque([node])
        explored = set()
        while frontier:
            node = frontier.popleft()
            explored.add(node.state)
            children = node.Expand(problem)
            for child in children:
                if child.state not in explored and child not in frontier:
                    if problem.Goal_test(child.state):
                        return child
                    frontier.append(child)
        return None

