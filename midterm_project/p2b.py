from p2a import Graph

class SimulatedAnealing:
    def __init__(self, graph, state, schedule):
        self.state = state
        self.graph = graph
        self.schedule = schedule
    
    def exec(self, count):
        for t in range(count):
            T = self.schedule(t)
            if T == 0:
                return self.state
            next = 
            
        return self.state
