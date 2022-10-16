import sys
from random import choice

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
