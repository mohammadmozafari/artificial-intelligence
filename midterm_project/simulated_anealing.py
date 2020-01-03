import random as rnd
import copy
import math
import matplotlib.pyplot as plt
from genetic import get_graph

class SimulatedAnealing:
    """
    This class helps to use simulated anealing algorithm to solve map coloring.
    To use this we fist have to initialize it using the constructor.
    Then we can call exec method witch executes the algorithm for the given number of iterations.
    """
    def __init__(self, graph, num_edges, num_colors, schedule, T0, alpha):
        self.length = len(graph)
        self.state = [rnd.randint(1, num_colors) for i in range(self.length)]
        self.edges = num_edges
        self.colors = num_colors
        self.graph = graph
        self.schedule = schedule
        self.T0 = T0 * 1.0
        self.alpha = alpha * 1.0

    def fitness(self, chrom):
        """
        This function computes the fitness value for a given chromosome.
        """
        f = 0.0
        for node, neighbors in enumerate(self.graph):
            for nei in neighbors:
                if chrom[node] != chrom[nei]:
                    f += 1
        f /= (2 * self.edges)
        return f
        
    def exec(self, count):
        """
        For "count" times we take new successors and choose to go there or not depending
        on their fitness value.
        """
        hist_t = []
        hist_fit = []
        for t in range(count):
            T = self.schedule(self.T0, self.alpha, t)
            hist_t.append(T)
            hist_fit.append(self.fitness(self.state))
            if T == 0:
                return self.state
            
            successor = copy.deepcopy(self.state)
            rand = rnd.randint(0, self.length - 1)
            new_color = rnd.randint(1, self.colors)
            while new_color == self.state[rand]:
                new_color = rnd.randint(1, self.colors)
            successor[rand] = new_color

            e1 = self.fitness(self.state)
            e2 = self.fitness(successor)
            delta_e = (e2 - e1) * 1.0

            if delta_e >= 0:
                self.state = successor
            else:
                prob = math.exp(delta_e / T)
                unif = rnd.uniform(0, 1)
                if unif <= prob:
                    self.state = successor
            
        return self.state, hist_t, hist_fit

def mapping_1(T0, alpha, t):
    T = T0 * math.pow(alpha, t)
    return T

def mapping_2(T0, alpha, t):
    T = (T0) / (1 + alpha * math.log(1 + t))
    return T

def mapping_3(T0, alpha, t):
    T = (T0) / (1 + alpha * t)
    return T

def mapping_4(T0, alpha, t):
    T = (T0) / (1 + alpha * t * t)
    return T

def main():
    # params
    colors = 4
    iters = 10000
    T0 = 500
    alpha = 40

    graph, N, M = get_graph()
    sa = SimulatedAnealing(graph, M, colors, mapping_2, T0, alpha)
    state, t, fit = sa.exec(iters)
    print(state)

    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(fit)
    ax2.plot(t)
    plt.show()

if __name__ == '__main__':
    main()
