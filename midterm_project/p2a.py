import random as rnd
import copy
from itertools import product

graph = [
    [1, 2, 3],
    [0, 2],
    [0, 1, 3],
    [0, 2]
]
vers = 4
edges = 5

class Genetic:
    def __init__(self, graph, num_edges, population_size):
        """
        This constructor inits a model for the graph in order to solve it using genetic algorithm
        """
        self.graph = graph
        self.size = population_size
        self.length = len(graph)
        self.edges = num_edges
        self.population = [rnd.randint(1, graph.num_colors) for i in range(self.length)]

    def fitness(self, chrom):
        """
        This function computes the fitness value for a given chromosome.
        """
        f = 0.0
        for node, neighbors in enumerate(graph):
            for nei in neighbors:
                if self.population[chrom][i] == self.population[chrom][nei]:
                    f += 1
        f /= (2 * self.num_edges)
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

