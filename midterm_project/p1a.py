import copy

class Rubik:

    def __init__(self, initial_state):
        self.num_faces = len(initial_state)
        self.dim = len(initial_state[0])
        self.state = copy.deepcopy(initial_state)
    
    # def move(self, side, num):
    #     if side == 0:
    #         pass
    #     elif side == 1:
    #         pass
    #     elif side == 2:
    #         pass
    #     elif side == 3:
    #         pass
    #     elif side == 4:
    #         rotate((5, 1, 1), (5, 0, 1), (4, 1, 1),
    #                (4, 0, 1), (2, 1, 1), (2, 0, 1), (0, 1, 1), (0, 1, 1), 4)
    #     elif side == 5:
    #         pass

    # def rotate(self, idx, num):
    #     new_rubik = copy.deepcopy(rubik)

    #     pass

    """
    Input
    - rubik: state of the rubik
    - surface: number of the surface to be rotated
    - count: number of times to rotate the surface
    """
    def rotate_surface(self, rubik, surface_num, count):
        N = self.dim
        for x in range(count):
            for i in range(N // 2):
                for j in range(i, N - i - 1):
                    temp = rubik[surface_num][i][j]
                    rubik[surface_num][i][j] = rubik[surface_num][N - 1 - j][i]
                    rubik[surface_num][N - 1 - j][i] = rubik[surface_num][N - 1 - i][N - 1 - j]
                    rubik[surface_num][N - 1 - i][N - 1 - j] = rubik[surface_num][j][N - 1 - i]
                    rubik[surface_num][j][N - 1 - i] = temp

    """
    Input
    - rubik: state of the rubik cube
    - idx: address of the pieces to be rotated
    - count: number of times to rotate
    """
    def rotate_perimeter(self, rubik, idx, count):
        rotated_list = []
        for (x, y, z) in idx:
            rotated_list.append(rubik[x][y][z])
        rotated_list = rotated_list[-count:] + rotated_list[:-count]
        for i, (x, y, z) in enumerate(idx):
            rubik[x][y][z] = rotated_list[i]
        
