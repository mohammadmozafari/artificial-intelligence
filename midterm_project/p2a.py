import random as rnd

num_province = 30

class Graph:
    def __init__(self, num):
        """
        The constructor inits a graph with the given number of vertices.
        """
        self.graph_matrix = [[0 for j in range(num)] for i in range(i)]
        self.colors = [0 for i in range(num)]
        self.num_edges = 0
        self.num_ver = num

    def add_edge(self, x, y):
        """
        This method creates a connection between two given vertices.
        """
        self.graph_matrix[x][y] = 1
        self.graph_matrix[y][x] = 1
        self.num_edges += 1

    def color_node(self, x, color):
        """
        Mark a color for the given vertex.
        """
        self.colors[x] = color

class Genetic:
    def __init__(self, graph, population_size):
        """
        This constructor inits a model for the graph in order to solve it using genetic algorithm
        """
        self.graph = graph
        self.size = population_size
        self.length = graph.num_ver
        self.population = [rnd.randint(1, 4) for i in range(self.length)]

    def delta(self, i, j, ch):
        """
        Given two indices i and j this function computes delta(i, j) as described previously.
        """
        if self.population[ch][i] == self.population[ch][j]:
            return 1
        return 0

    def fitness(self, chrom):
        """
        This function computes the fitness value for a given chromosome.
        """
        f = 0.0
        for i in range(self.length):
            for j in range(self.length):
                f += self.delta(i, j, chrom)
        f /= self.graph.num_edges
        return f

    def selection(self, k):
        """
        This function takes k member and selects the best one according to their fitness value.
        The number of the tornuments depends on the population size and k and equals size/k
        """
        parents = []
        torns = self.size // k
        for i in range(torns):
            candids = [rnd.randint(0, self.size - 1) for j in range(k)]
            chosen = None
            max_fitness = -1.0
            for j in range(k):
                fit = self.fitness(candids[j])
                if fit > max_fitness:
                    max_fitness = fit
                    chosen = j
            
            parents.append(j)
        return parents

    

