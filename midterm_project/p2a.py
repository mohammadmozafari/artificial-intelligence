import random as rnd
import copy
from itertools import product

num_province = 30

class Graph:
    def __init__(self, num, num_colors):
        """
        The constructor inits a graph with the given number of vertices.
        """
        self.graph_matrix = [[0 for j in range(num)] for i in range(i)]
        self.colors = [0 for i in range(num)]
        self.num_edges = 0
        self.num_ver = num
        self.num_colors = num_colors

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
        self.population = [rnd.randint(1, graph.num_colors) for i in range(self.length)]

    def delta(self, i, j, ch):
        """
        Given two indices i and j this function computes delta(i, j) as described previously.
        """
        if self.population[ch][i] == self.population[ch][j]:
            return 1
        return 0

    # TODO: optimize this. better if we use adjacency list.
    def fitness(self, chrom):
        """
        This function computes the fitness value for a given chromosome.
        """
        f = 0.0
        for i in range(self.length):
            for j in range(self.length):
                if self.graph.matrix[i][j] == 1:
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

    def new_generation(self, parents):
        """
        This function takes the selected parents and creates a number of new chromosomes.
        The number of children equals the size of the original population.
        Inputs
        - parents: a list containing the index of the parent chromosomes
        """
        children = []
        for i in range(self.size):
            x = rnd.randint(0, len(parents) - 1)
            y = rnd.randint(0, len(parents) - 1)
            children.append(self.crossover(x, y))
        self.population = children
        
    def crossover(self, x, y):
        """
        This function takes two parents and creates a child from them.
        Inputs
        - x: index of the first chromosome
        - y: index of the second chromosome
        """
        child = copy.deepcopy(self.population[x])
        mask = [rnd.uniform(0, 1) for i in range(self.length)]
        for i in range(self.length):
            if mask[i] > 0.5:
                child[i] = self.population[y][i]
        return child

    def mutation(self, mutation_rate):
        """
        This function mutates some of the genes in some of the chromosomes.
        The number of genes to be mutated is computated with the following formula: (populationSize * chromosomeLength * mutaionRate) 
        """
        mutated_genes = self.size * self.length * mutation_rate
        options = product(range(self.size), range(self.length))
        options = rnd.sample(options, mutated_genes)
        for i in range(mutated_genes):
            self.population[options[i][0]][options[i][1]] = rnd.randint(1, self.graph.num_colors)
        
    def exec(self, num_iters, k, mutation_rate):
        """
        This part executes the algorithm for num_iters iterations.
        """
        for i in range(num_iters):
            parents = self.selection(k)
            self.new_generation(parents)
            self.mutation(mutation_rate)

