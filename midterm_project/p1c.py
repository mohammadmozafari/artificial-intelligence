import heapq
from p1a import *

def a_star(rubik):
    
    nodes = NodeCount()
    heap = []
    heapq.heapify(heap)
    heapq.heappush(heap, rubik)

    actions = [(0, True), (0, False), (1, True), (1, False), (2, True), (2, False), (3, True), (3, False), (4, True), (4, False), (5, True), (5, False)]
    nodes.change_generated(1)
    nodes.change_in_mem(1)

    while len(heap) != 0:
        x = heapq.heappop(heap)
        nodes.change_in_mem(-1)
        nodes.change_expanded(1)
        if x.goal_test():
            return (build_path(x, None), nodes)
        for action in actions:
            heapq.heappush(heap, x.move(*action))
            nodes.change_generated(1)

    return False, nodes


def main():
    r = get_rubik()
    result, nodes = a_star(r)
    show_solution((result, nodes))

if __name__ == '__main__':
    main()