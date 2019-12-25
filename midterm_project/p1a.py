import copy
from itertools import chain

class NodeCount:
    self.generated_nodes = 0
    self.expanded_nodes = 0
    self.in_memory = 0
    self.max_in_mem = 0

    def change_generated(self, count):
        self.increase_generated += count
    
    def change_expanded(self, count):
        self.change_expanded += count

    def change_in_mem(self, count):
        self.in_memory += count
        if self.in_memory > self.max_in_mem:
            self.max_in_mem = self.in_memory

class Rubik:
    """
    This class represents one instance of rubik puzzle.
    """

    def __init__(self, initial_state, father_move=None):
        self.num_faces = len(initial_state)
        self.dim = len(initial_state[0])
        self.state = copy.deepcopy(initial_state)
        self.fatcher_move = father_move
        x = tuple(chain.from_iterable(chain.from_iterable(self.state)))
        self.hashed = hash(x)
    
    def move(self, side, clockwise):
        """
        This method makes a move and create a new rubik cube instance.
        Input
        - side: the number of the face to be rotated
        - clockwise: if True then the rotation is clockwise
        """
        cw = 1 if clockwise else 3
        if side == 0:
            return self.rotate([(5, 1, 0), (5, 1, 1), (3, 0, 1), (3, 0, 0), (2, 0, 1), (2, 0, 0), (1, 0, 1), (1, 0, 0)], side, cw)
        elif side == 1:
            return self.rotate([(0, 0, 0), (0, 1, 0), (2, 0, 0), (2, 1, 0), (4, 0, 0), (4, 1, 0), (5, 0, 0), (5, 1, 0)], side, cw)
        elif side == 2:
            return self.rotate([(0, 1, 0), (0, 1, 1), (3, 0, 0), (3, 1, 0), (4, 0, 1), (4, 0, 0), (1, 1, 1), (1, 0, 1)], side, cw)
        elif side == 3:
            return self.rotate([(5, 1, 1), (5, 0, 1), (4, 1, 1), (4, 0, 1), (2, 1, 1), (2, 0, 1), (0, 1, 1), (0, 0, 1)], side, cw)
        elif side == 4:
            return self.rotate([(1, 1, 0), (1, 1, 1), (2, 1, 0), (2, 1, 1), (3, 1, 0), (3, 1, 1), (5, 0, 1), (5, 0, 0)], side, cw)
        elif side == 5:
            return self.rotate([(0, 0, 1), (0, 0, 0), (1, 0, 0), (1, 1, 0), (4, 1, 0), (4, 1, 1), (3, 1, 1), (3, 0, 1)], side, cw)

    # TODO: optimize this
    def goal_test(self):
        """
        This function checks whether we are in final state or not.
        """
        for i in range(self.num_faces):
            for j in range(self.dim):
                for k in range(self.dim):
                    if not self.state[i][0][0] == self.state[i][j][k]:
                        return False
        x = list(chain.from_iterable(chain.from_iterable(self.state)))
        return True if len(set(x)) == 6 else False

    def rotate(self, idx, num, count):
        """
        Input
        - idx: address of the pieces to be rotated
        - num: number of the surface to be rotated
        - count: number of times to perform rotation
        """
        new_rubik = copy.deepcopy(self.state)
        self.rotate_surface(new_rubik, num, count)
        self.rotate_perimeter(new_rubik, idx, 2 * count)
        cw = True if count == 1 else False
        return Rubik(new_rubik, (num, cw))

    def rotate_surface(self, rubik, surface_num, count):
        """
        Input
        - rubik: state of the rubik
        - surface: number of the surface to be rotated
        - count: number of times to rotate the surface
        """
        N = self.dim
        for x in range(count):
            for i in range(N // 2):
                for j in range(i, N - i - 1):
                    temp = rubik[surface_num][i][j]
                    rubik[surface_num][i][j] = rubik[surface_num][N - 1 - j][i]
                    rubik[surface_num][N - 1 - j][i] = rubik[surface_num][N - 1 - i][N - 1 - j]
                    rubik[surface_num][N - 1 - i][N - 1 - j] = rubik[surface_num][j][N - 1 - i]
                    rubik[surface_num][j][N - 1 - i] = temp

    def rotate_perimeter(self, rubik, idx, count):
        """
        Input
        - rubik: state of the rubik cube
        - idx: address of the pieces to be rotated
        - count: number of times to rotate
        """
        rotated_list = []
        for (x, y, z) in idx:
            rotated_list.append(rubik[x][y][z])
        rotated_list = rotated_list[-count:] + rotated_list[:-count]
        for i, (x, y, z) in enumerate(idx):
            rubik[x][y][z] = rotated_list[i]

    def __eq__(self, value):
        if not type(value) is Rubik:
            return False
        return value.state == self.state

    def __hash__(self):
        return self.hashed

# TODO: modify this to use parent node for path creation      
def solve_with_IDS(rubik, initial_depth, final_depth):
    
    # TODO: random selection between actions
    actions = [(0, True), (0, False), (1, True), (1, False), (2, True), (2, False), (3, True), (3, False), (4, True), (4, False), (5, True), (5, False)]
    
    generated_nodes, expanded_nodes, max_in_memory, in_memory = 0, 0, 0, 0
    def depth_limited_search(rubik, limit, move):

        nonlocal generated_nodes, expanded_nodes, max_in_memory, in_memory
        if rubik.goal_test():
            if move != None:
                result.append(move)
            return True
        elif limit == 0:
            return 'cutoff'
        else:
            cut = False
            for action in actions:
                
                generated_nodes += 1    # a node is generated
                expanded_nodes += 1     # a node is expanded
                in_memory += 1          # a new node in memory
                if in_memory > max_in_memory:
                    max_in_memory = in_memory
                
                child = rubik.move(action[0], action[1])
                resp = depth_limited_search(child, limit - 1, action)

                in_memory -= 1
                if resp == 'cutoff':
                    cut = True
                elif resp != False:
                    if move != None:
                        result.append(move)
                    return True
            if cut:
                return 'cutoff'
            else:
                return False

    for i in range(initial_depth, final_depth):
        result = []
        resp = depth_limited_search(rubik, i, None)
        if resp != 'cutoff':
            return result[::-1], generated_nodes, expanded_nodes, max_in_memory
    
    return None, generated_nodes, expanded_nodes, max_in_memory

def show_solution(result):
    if result[0] == None:
        print()
        print('no solution found until the specified depth')
    else:
        for i, move in enumerate(result[0]):
            print('move ' + str(i + 1) + ': face ' + str(move[0] + 1), end=' ')
            if move[1]:
                print('clockwise')
            else:
                print('counter clockwise')
        print()
        print('solution found with ' + str(len(result[0])) + ' moves')
        
    print('number of nodes generated: ' + str(result[1]))
    print('number of nodes expanded: ' + str(result[2]))
    print('maximum number of nodes in memory: ' + str(result[3]))
    print('----------------------------------------------------')

def get_rubik():
    s = [[[0, 0], [0, 0]],  [[1, 1], [1, 1]], [[2, 2], [2, 2]],
          [[3, 3], [3, 3]], [[4, 4], [4, 4]], [[5, 5], [5, 5]]]
    for i in range(6):
        face = input()
        face = face.split(' ')
        s[i][0][0], s[i][0][1], s[i][1][0], s[i][1][1] = int(face[0]) - 1, int(face[1]) - 1, int(face[2]) - 1, int(face[3]) - 1
    return Rubik(s)

def main():
    r = get_rubik()
    result = solve_with_IDS(r, 1, 6)
    show_solution(result)

if __name__ == '__main__':
    main()
