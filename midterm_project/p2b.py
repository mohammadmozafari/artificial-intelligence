import random as rnd
import copy
import math
from p2a import Graph, Genetic

class SimulatedAnealing:
    """
    This class helps to use simulated anealing algorithm to solve map coloring.
    To use this we fist have to initialize it using the constructor.
    Then we can call exec method witch executes the algorithm for the given number of iterations.
    """
    def __init__(self, graph, state, schedule, T0, alpha):
        self.state = state
        self.graph = graph
        self.schedule = schedule
        self.T0 = T0 * 1.0
        self.alpha = alpha * 1.0
        
    def exec(self, count):
        """
        For "count" times we take new successors and choose to go there or not depending
        on their fitness value.
        """
        for t in range(count):
            T = self.schedule(self.T0, self.alpha, t)
            if T == 0:
                return self.state
            
            successor = copy.deepcopy(self.state)
            rand = rnd.randint(0, graph.length - 1)
            new_color = rnd.randint(1, graph.num_colors)
            while new_color == self.state[rand]:
                new_color = rnd.randint(1, graph.num_colors)
            successor[rand] = new_color

            e2 = Genetic.fitness(successor)
            e1 = Genetic.fitness(self.state)
            delta_e = (e2 - e1) * 1.0

            if delta_e >= 0:
                self_state = successor
            else:
                prob = math.exp(delta_e / T)
                unif = rnd.uniform(0, 1)
                if unif <= prob:
                    self_state = successor
            
        return self.state

def mapping_1(T0, alpha, t):
    T = T0 * math.pow(alpha, t)
    return T

def mapping_2(T0, alpha, t):
    T = (T0) / (1 + alpha * math.log10(1 + t))
    return T

def mapping_3(T0, alpha, t):
    T = (T0) / (1 + alpha * t)
    return T

def mapping_4(T0, alpha, t):
    T = (T0) / (1 + alpha * t * t)
    return T
