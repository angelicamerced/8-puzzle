from random import randint
from matrix import Matrix
from queue import PriorityQueue, Queue
import random
import pygame
import numpy as np
import time
import global_colors

class Algo:

    def __init__(self, x, y, width, height, lastSolveTime, move, cost, matrix,  blocks = [], final_state = "1,2,3,4,5,6,7,8,0"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.lastSolveTime = lastSolveTime
        self.move = move
        self.cost = cost
        self.matrix = matrix
        self.blocks = blocks
        self.final_state = final_state

    @staticmethod
    def new(x, y, width, height):
        return Algo(x, y, width, height, 0, [], 0, Matrix(3,3), [])

    def validNumbers(self, numbers):
        valid = False
        if len(numbers) == 9:
            ref = list(range(9))
            valid = True
            for i in numbers:
                if int(i) not in ref:
                    valid = False
                else:
                    ref.remove(int(i))
        return valid

    def randomBlocks(self):
        n = randint(30,40)
        for i in range(n):
            zero = self.matrix.searchBlock(0)
            possibleMoves = []
            #move up
            if zero[0] > 0:
                possibleMoves.append(self.matrix.moveup)
            if zero[0] < 2:
                possibleMoves.append(self.matrix.movedown)
            if zero[1] > 0:
                possibleMoves.append(self.matrix.moveleft)
            if zero[1] < 2:
                possibleMoves.append(self.matrix.moveright)
            random.choice(possibleMoves)(zero)
        random_moves = self.setBlocksMatrix()
        return random_moves

    def setBlocksMatrix(self):
        blocks = []
        block_x=self.x
        block_y=self.y
        block_w = self.width/3
        block_h = self.height/3

        m = self.matrix.getMatrix() # kani ang need as output for bfs()
        i=0
        for k in range(3):
            for j in range(3):
                blocks.append({'rect':pygame.Rect(block_x, block_y, block_w, block_h),'color':global_colors.WHITE,'block':m[k][j]})
                block_x += block_w+1
                i+=1
            block_y += block_h+1
            block_x = self.x
        self.blocks = blocks
        list_of_blocks = m.ravel().tolist()
        return list_of_blocks

    def setBlocks(self, string):
        numbers = string.split(",")
        blocks = []
        if self.validNumbers(numbers) :
            block_x=self.x
            block_y=self.y

            block_w = self.width/3
            block_h = self.height/3
            self.matrix.buildMatrix(string)
            i=0
            for k in range(3):
                for j in range(3):
                    blocks.append({'rect':pygame.Rect(block_x, block_y, block_w, block_h),'color':global_colors.WHITE,'block':int(numbers[i])})
                    block_x += block_w+1 #right
                    i+=1
                block_y += block_h+1 #down
                block_x = self.x
            self.blocks = blocks
            return True
        return False

    def initialize(self):
        blocks = self.final_state
        self.setBlocks(blocks)

    def existsIn(self,elem, list = []):
        for item in list:
            if item.isEqual(elem):
                return True
        return False

    @staticmethod
    def bfs(initial_state, response={}):
        start_time = time.time()
        start_node = Puzzle(initial_state, None, None, 0)
        if start_node.goal_test():
            end_time = time.time()
            comp_time = end_time - start_time
            solution = start_node.find_solution()
            return comp_time, solution
        q = Queue()
        q.put(start_node)
        explored=[]
        while not(q.empty()):
            node=q.get()
            explored.append(node.state)
            children=node.generate_child()
            for child in children:
                print('Finding solution')
                print(child)
                if child.goal_test():
                    end_time = time.time()
                    comp_time = end_time - start_time
                    solution = child.find_solution()
                    moves = []
                    for move in solution:
                        if move == 'U':
                            moves.append('up')
                        elif move == 'D':
                            moves.append('down')
                        elif move == 'L':
                            moves.append('left')
                        elif move == 'R':
                            moves.append('right')
                    return comp_time, moves
                q.put(child)
        return 0, []

    def a_star(self):
        start_time = time.time()
        node = self.matrix
        Mfinal = Matrix(3,3)
        Mfinal.buildMatrix(self.final_state) #1,2,3,4,5,6,7,8,0
        final = Mfinal.getMatrix()
        queue = PriorityQueue()
        queue.put(node)
        visitedNodes = []
        indexSelected = 0
        n = 1
        while (not node.isEqual(final) and not queue.empty()):
            node = queue.get()
            visitedNodes.append(node)
            moves = []
            childNodes = node.getPossibleNodes(moves)
            for i in range(len(childNodes)):
                if not self.existsIn(childNodes[i].getMatrix(), visitedNodes):
                    childNodes[i].move = moves[i]
                    childNodes[i].manhattanDist()
                    childNodes[i].setPrevious(node)
                    # Cumulating the cost function
                    childNodes[i].cost = node.cost + node.manhattanDistCost(childNodes[i])
                    childNodes[i].dist += childNodes[i].cost
                    queue._put(childNodes[i])
            n += 1
            auxCost = 0

        moves = []
        self.cost = n
        if(node.isEqual(final)):
            moves.append(node.move)
            nd = node.previous
            while nd != None:
                if nd.move != '':
                    moves.append(nd.move)
                nd = nd.previous

        end_time = time.time()
        self.lastSolveTime = end_time-start_time
        return moves[::-1]

class Puzzle:
    goal_state=[1,2,3,4,5,6,7,8,0]
    heuristic=None
    evaluation_function=None
    needs_hueristic=True
    num_of_instances=0

    def __init__(self,state,parent,action,path_cost,needs_hueristic=False):
        self.parent=parent
        self.state=state
        self.action=action
        if parent:
            self.path_cost = parent.path_cost + path_cost
        else:
            self.path_cost = path_cost
        if needs_hueristic:
            self.needs_hueristic=True
            self.generate_heuristic()
            self.evaluation_function=self.heuristic+self.path_cost
        Puzzle.num_of_instances+=1

    def __str__(self):
        return str(self.state[0:3])+'\n'+str(self.state[3:6])+'\n'+str(self.state[6:9])

    def generate_heuristic(self):
        self.heuristic=0
        for num in range(1,9):
            distance=abs(self.state.index(num) - self.goal_state.index(num))
            i=int(distance/3)
            j=int(distance%3)
            self.heuristic=self.heuristic+i+j

    def goal_test(self):
        if self.state == self.goal_state:
            return True
        return False

    @staticmethod
    def find_legal_actions(i,j, prev_action=''):
        legal_action = ['U', 'D', 'L', 'R']
        if i == 0 or prev_action == 'D':  # up is disable
            legal_action.remove('U')
        if i == 2 or prev_action == 'U':  # down is disable
            legal_action.remove('D')
        if j == 0 or prev_action == 'R': # left is disable
            legal_action.remove('L')
        if j == 2 or prev_action == 'L': # right is disable
            legal_action.remove('R')
        return legal_action

    @staticmethod
    def find_blank_pos(arr):
        x = arr.index(0)
        i = int(x / 3)
        j = int(x % 3)
        return i,j,x

    @staticmethod
    def get_random_move(arr, prev_action):
        i,j,_ = Puzzle.find_blank_pos(arr)
        action = random.choice(Puzzle.find_legal_actions(i,j, prev_action))
        return action

    def generate_child(self):
        children = []
        i,j,x = Puzzle.find_blank_pos(self.state)
        legal_actions = Puzzle.find_legal_actions(i,j)

        for action in legal_actions:
            new_state = self.state.copy()
            if action == 'U':
                new_state[x], new_state[x-3] = new_state[x-3], new_state[x]
            elif action == 'D':
                new_state[x], new_state[x+3] = new_state[x+3], new_state[x]
            elif action == 'L':
                new_state[x], new_state[x-1] = new_state[x-1], new_state[x]
            elif action == 'R':
                new_state[x], new_state[x+1] = new_state[x+1], new_state[x]
            children.append(Puzzle(new_state,self,action,1,self.needs_hueristic))
        return children

    def find_solution(self):
        solution = []
        solution.append(self.action)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]
        solution.reverse()
        return solution