class Rubik:

    def __init__(self, initial_state):
        self.face = []
        for i in range(6):
            self.face.append(list.copy(initial_state[i]))

    def get_current_state(self):
        result = ''
        for i in range(len(self.face)):
            result += 'face ' + str(i + 1) + ': ' + ', '.join([str(elem) for elem in self.face[i]]) + '\n'
        return result

    def __rotate(self, idx):
        rotated_list = []
        for (x, y) in idx:
            rotated_list.append(self.face[x][y])
        rotated_list = rotated_list[1:] + rotated_list[:1]
        return rotated_list
        
