import copy
import numpy as np
import random as rnd
from itertools import chain

class NodeCount:
    generated_nodes = 0
    expanded_nodes = 0
    in_memory = 0
    max_in_mem = 0

    def change_generated(self, count):
        self.generated_nodes += count
    
    def change_expanded(self, count):
        self.expanded_nodes += count

    def change_in_mem(self, count):
        self.in_memory += count
        if self.in_memory > self.max_in_mem:
            self.max_in_mem = self.in_memory

class Rubik:
    """
    This class represents one instance of rubik puzzle.
    """
    def __init__(self, initial_state, parent=None, parent_move=None, alg=1):
        self.num_faces = initial_state.shape[0]
        self.dim = initial_state.shape[1]
        self.state = np.copy(initial_state)
        self.parent = parent
        self.parent_move = parent_move
        self.alg = alg
        
        if alg >= 2:
            self.hashed = hash(str(self.state))
        if alg == 3:
            self.H = self.calculateH()
            self.G = 0 if parent == None else (parent.G + 5)
    
    def move(self, side, clockwise):
        """
        This method makes a move and create a new rubik cube instance.
        Input
        - side: the number of the face to be rotated
        - clockwise: if True then the rotation is clockwise
        """
        s = self.state
        cw = 1 if clockwise else 3
        if side == 0:
            return self.rotate(((5, 5, 3, 3, 2, 2, 1, 1), (3, 2, 1, 0, 1, 0, 1, 0)), side, cw)
        elif side == 1:
            return self.rotate(((0, 0, 2, 2, 4, 4, 5, 5), (0, 3, 0, 3, 0, 3, 0, 3)), side, cw)
        elif side == 2:
            return self.rotate(((0, 0, 3, 3, 4, 4, 1, 1), (3, 2, 0, 3, 1, 0, 2, 1)), side, cw)
        elif side == 3:
            return self.rotate(((5, 5, 4, 4, 2, 2, 0, 0), (2, 1, 2, 1, 2, 1, 2, 1)), side, cw)
        elif side == 4:
            return self.rotate(((1, 1, 2, 2, 3, 3, 5, 5), (3, 2, 3, 2, 3, 2, 1, 0)), side, cw)
        elif side == 5:
            return self.rotate(((0, 0, 1, 1, 4, 4, 3, 3), (1, 0, 0, 3, 3, 2, 2, 1)), side, cw)

    def goal_test(self):
        """
        This function checks whether we are in final state or not.
        """
        result = np.sum(np.std(self.state, axis=1))
        return True if result == 0 else False

    def rotate(self, idx, num, count):
        """
        Input
        - idx: address of the pieces to be rotated
        - num: number of the surface to be rotated
        - count: number of times to perform rotation
        """
        new_rubik = np.copy(self.state)
        self.rotate_surface(new_rubik, num, count)
        self.rotate_perimeter(new_rubik, idx, 2 * count)
        cw = True if count == 1 else False
        return Rubik(new_rubik, self, (num, cw), alg=self.alg)

    def rotate_surface(self, rubik, surface_num, count):
        """
        Input
        - rubik: state of the rubik
        - surface: number of the surface to be rotated
        - count: number of times to rotate the surface
        """
        rubik[surface_num, :count], rubik[surface_num, count:] = rubik[surface_num, -count:].copy(), rubik[surface_num, :-count].copy()

    def rotate_perimeter(self, rubik, idx, count):
        """
        Input
        - rubik: state of the rubik cube
        - idx: address of the pieces to be rotated
        - count: number of times to rotate
        """
        x = idx[0][-count:] + idx[0][:-count]
        y = idx[1][-count:] + idx[1][:-count]
        rubik[idx] = rubik[(x, y)].copy()

    def calculateH(self):
        """
        This function calculates the H value for the current rubik state
        """
        x = 0
        for i in range(self.num_faces):
            un = np.unique(self.state[i]).shape[0]
            if un == 2:
                x += 1
            elif un == 3:
                x += 2
            elif un == 4:
                x += 4
        return x

    @staticmethod
    def get_actions():
        actions = [(0, False), (1, False), (2, True), (3, True), (4, True), (5, False)]
        rnd.shuffle(actions)
        return actions

    @staticmethod
    def get_all_actions():
        actions = [(0, False), (0, True), (1, False), (1, True), (2, False), (2, True), (3, False), (3, True), (4, False), (4, True), (5, False), (5, True)]
        rnd.shuffle(actions)
        return actions

    def __str__(self):
        st = ''
        for i in range(self.num_faces):
            st += str(self.state[i][0] + 1) + ' ' + str(self.state[i][1] + 1) + ' ' + str(self.state[i][3] + 1) +  ' ' + str(self.state[i][2] + 1) + '\n'
        return st

    def __eq__(self, value):
        """
        Determines whether this object is equal with another given object
        """
        if not type(value) is Rubik:
            return False
        return np.array_equal(value.state, self.state)

    def __hash__(self):
        """
        Returns the hash value for the current object
        """
        return self.hashed

    def __lt__(self, other):
        """
        Takes another object and returns True if current object is less than the give
        """
        f_this = self.G + self.H
        f_other = other.G + other.H
        return f_this < f_other
    
def solve_with_IDS(rubik, initial_depth, final_depth):
    """
    Takes a rubik puzzle and tries to solve it using IDS algorithm.
    Input
    - rubik: initial state of the puzzle
    - initial_depth: left range of the limit
    - final_depth: right range of the limit
    """
    nodes = NodeCount()
    
    def depth_limited_search(rubik, limit, move):
        nonlocal nodes
        if rubik.goal_test():
            return rubik
        elif limit == 0:
            return 'cutoff'
        else:
            cut = False
            nodes.change_expanded(1)
            actions = Rubik.get_actions()
            for action in actions:
                nodes.change_generated(1)
                nodes.change_in_mem(1)
                child = rubik.move(action[0], action[1])
                resp = depth_limited_search(child, limit - 1, action)
                nodes.change_in_mem(-1)
                if resp == 'cutoff':
                    cut = True
                elif resp != False:
                    return resp
            if cut:
                return 'cutoff'
            else:
                return False

    for i in range(initial_depth, final_depth):
        result = []
        resp = depth_limited_search(rubik, i, None)
        if resp == False:
            return resp, nodes
        if (resp != 'cutoff'):
            return build_path(resp, None), nodes

    return None, nodes

def show_solution(result):
    """
    This is a utility function for organized printing on the terminal.
    """
    if result[0] == None:
        print()
        print('no solution found until the specified depth')
    elif result[0] == False:
        print()
        print('no solution exists')
    else:
        for i, move in enumerate(result[0]):
            print('move ' + str(i + 1) + ': face ' + str(move[0] + 1), end=' ')
            if move[1]:
                print('clockwise')
            else:
                print('counter clockwise')
        print()
        print('solution found with ' + str(len(result[0])) + ' moves')
        
    print('number of nodes generated: ' + str(result[1].generated_nodes))
    print('number of nodes expanded: ' + str(result[1].expanded_nodes))
    print('maximum number of nodes in memory: ' + str(result[1].max_in_mem))
    print('----------------------------------------------------')

def get_rubik(alg):
    """
    This is a utility function for taking a rubik puzzle from input.
    """
    s = np.array([[0, 0, 0, 0],
                  [1, 1, 1, 1],
                  [2, 2, 2, 2],
                  [3, 3, 3, 3],
                  [4, 4, 4, 4],
                  [5, 5, 5, 5]])
    for i in range(6):
        face = input()
        face = face.split(' ')
        s[i, 0], s[i, 1], s[i, 3], s[i, 2] = int(face[0]) - 1, int(face[1]) - 1, int(face[2]) - 1, int(face[3]) - 1
    return Rubik(s, alg=alg)

def build_path(a, b):
    """
    Given two nodes that are the intersection of searches we construct the path form source to target.
    """
    path = []
    x = a
    while (x != None) and (x.parent != None):
        path.append(x.parent_move)
        x = x.parent
    path = path[::-1]
    x = b
    while (x != None) and (x.parent != None):
        path.append(x.parent_move)
        x = x.parent
    return path

def main():
    r = get_rubik(1)
    result, nodes = solve_with_IDS(r, 1, 9)
    show_solution((result, nodes))

if __name__ == '__main__':
    main()
