import random as rnd
import copy
from itertools import product

graph = [
    [2, 7, 11, 16]
    [2, 3, 7]
    [0, 1, 7]
    [1, 7, 9, 10]
    [5, 6, 8]
    [4, 8, 9]
    [4, 8, 18, 22]
    [0, 1, 2, 3, 10, 11, 14]
    [4, 5, 6, 9, 13, 17, 18, 19]
    [3, 5, 8, 10, 12, 13]
    [3, 7, 9, 12, 14, 15]
    [0, 7, 14, 16]
    [9, 10, 13, 15]
    [8, 9, 12, 15, 17]
    [7, 10, 11, 15, 16, 20]
    [10, 12, 13, 14, 17, 19, 20]
    [0, 11, 14, 20, 21]
    [8, 13, 15, 19]
    [6, 8, 19, 22, 25, 26]
    [8, 15, 17, 18, 20, 23, 24, 26, 28]
    [14, 15, 16, 19, 21, 23]
    [16, 20, 23]
    [6, 18, 25, 27]
    [19, 20, 21, 24, 26, 28, 29]
    [19, 23, 28]
    [18, 22, 26, 27, 30]
    [18, 19, 23, 25, 28, 29, 30]
    [22, 25, 30]
    [19, 23, 24, 26, 29]
    [23, 26, 28, 30]
    [25, 26, 27, 29]
    [0, 2]
]
vers = 4
edges = 5
colors = 3

class Genetic:
    def __init__(self, graph, num_edges, population_size, num_colors):
        """
        This constructor inits a model for the graph in order to solve it using genetic algorithm
        """
        self.graph = graph
        self.size = population_size
        self.length = len(graph)
        self.edges = num_edges
        self.population = [[rnd.randint(1, num_colors) for i in range(self.length)] for i in range(population_size)]

    def fitness(self, chrom):
        """
        This function computes the fitness value for a given chromosome.
        """
        f = 0.0
        for node, neighbors in enumerate(graph):
            for nei in neighbors:
                if self.population[chrom][node] == self.population[chrom][nei]:
                    f += 1
        f /= (2 * self.edges)
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
        mutated_genes = int(self.size * self.length * mutation_rate)
        if mutated_genes <= 0:
            return
        options = product(range(self.size), range(self.length))
        options = rnd.sample(list(options), mutated_genes)
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

def main():
    gen = Genetic(graph, edges, 5, colors)
    gen.exec(10000, 5, 0.02)
    print(gen.population)
    print(gen.fitness(0))

main()
