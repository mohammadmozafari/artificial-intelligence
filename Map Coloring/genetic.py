import random as rnd
import copy
import matplotlib.pyplot as plt
from itertools import product

class Genetic:
    def __init__(self, graph, num_edges, population_size, num_colors):
        """
        This constructor inits a model for the graph in order to solve it using genetic algorithm
        """
        self.graph = graph
        self.size = population_size
        self.length = len(graph)
        self.edges = num_edges
        self.num_colors = num_colors
        self.population = [[rnd.randint(1, num_colors) for i in range(self.length)] for i in range(population_size)]

    def fitness(self, chrom):
        """
        This function computes the fitness value for a given chromosome.
        """
        f = 0.0
        for node, neighbors in enumerate(self.graph):
            for nei in neighbors:
                if self.population[chrom][node] != self.population[chrom][nei]:
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
            for j in candids:
                fit = self.fitness(j)
                if fit > max_fitness:
                    max_fitness = fit
                    chosen = j
            parents.append(chosen)
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
            y = 0
            while True:
                y = rnd.randint(0, len(parents) - 1)
                if x != y: break
            children.append(self.crossover(self.population[parents[x]], self.population[parents[y]]))
        self.population = children
        
    def crossover(self, x, y):
        """
        This function takes two parents and creates a child from them.
        Inputs
        - x: index of the first chromosome
        - y: index of the second chromosome
        """
        child = copy.deepcopy(x)
        mask = [rnd.uniform(0, 1) for i in range(self.length)]
        for i in range(self.length):
            if mask[i] > 0.5:
                child[i] = y[i]
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
            self.population[options[i][0]][options[i][1]] = rnd.randint(1, self.num_colors)
        
    def exec(self, num_iters, k, mutation_rate):
        """
        This part executes the algorithm for num_iters iterations.
        """
        high_hist = []
        low_hist = []
        middle_hist = []
        for i in range(num_iters):
            high, low, middle = self.stats()
            high_hist.append(high)
            low_hist.append(low)
            middle_hist.append(middle)
            parents = self.selection(k)
            self.new_generation(parents)
            self.mutation(mutation_rate)
        return high_hist, low_hist, middle_hist

    def stats(self):
        high, low, ave = -1, -1, 0.0
        for i, chrom in enumerate(self.population):
            fit = self.fitness(i)
            ave += fit
            if fit > high:
                high = fit
            if fit < low or low == -1:
                low = fit 
        return high, low, (ave/self.size)

def get_graph():
    ver = int(input('enter number of vertices: '))
    graph = []
    edges = 0
    for i in range(ver):
        temp_list = []
        face = input()
        face = face.split(' ')
        for j in face:
            temp_list.append(int(j))
            edges += 1
        graph.append(temp_list)

    return graph, ver, edges // 2

def show_data(high, low, middle, title):
    plt.figure()
    plt.title(title)
    plt.plot(high, label='Maximum')
    plt.plot(low, label='Minimum')
    plt.plot(middle, label='Average')
    plt.legend()
    plt.savefig('C:\\Users\\Mohammad\\Desktop\\figures\\' + title + '.png')
    print(title, 'saved.')

def main():

    # params
    # generations = [50, 500, 5000]
    # mutation_rates = [0.01, 0.02, 0.05, 0.1]
    # population_sizes = [10, 100, 1000]
    # ks = [2, 5, 10]
    # colors = 4

    # graph, N, M = get_graph()

    # for gen in generations:
    #     for mut in mutation_rates:
    #         for p in population_sizes:
    #             for k in ks:
    #                 if p == 10 and k > 2:
    #                     continue
    #                 genet = Genetic(graph, M, p, colors)
    #                 data = genet.exec(gen, k, mut)
    #                 title = 'generations=%d, population=%d, mutation rate=%.2f, k=%d' % (gen, p, mut, k)
    #                 show_data(*data, title)

    # params
    generations = 50
    mutation_rate = 0.01
    population_size = 100
    k = 5
    colors = 4

    graph, N, M = get_graph()
    genet = Genetic(graph, M, population_size, colors)
    genet.exec(generations, k, mutation_rate)

    high = -1
    best = None
    for i, chrom in enumerate(genet.population):
        fit = genet.fitness(i)
        if fit > high:
            high = fit
            best = chrom

    print()
    print('best coloring')        
    print(best)

if __name__ == '__main__':
    main()
