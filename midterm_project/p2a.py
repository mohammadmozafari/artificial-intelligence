import random as rnd

num_province = 30

class Graph:
    def __init__(self, num):
        self.graph_matrix = [[0 for j in range(num)] for i in range(i)]
        self.colors = [0 for i in range(num)]

    def add_edge(self, x, y):
        self.graph_matrix[x][y] = 1
        self.graph_matrix[y][x] = 1

    def color_node(self, x, color):
        self.colors[x] = color

class Genetic:
    def __init__(self, chromosome_length, population_size):
        self.length = chromosome_length
        self.size = population_size
        self.population = [rnd.randint(1, 4) for i in range(self.length)]



