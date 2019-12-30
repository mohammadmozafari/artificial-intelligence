import heapq
from p1a import *

def a_star(rubik):
    nodes = NodeCount()
    actions = Rubik.get_actions()
    heap = []
    heapq.heapify(heap)
    heapq.heappush(heap, rubik)
    nodes.change_generated(1)
    nodes.change_in_mem(1)
    while len(heap) != 0:
        x = heapq.heappop(heap)
        nodes.change_in_mem(-1)
        nodes.change_expanded(1)
        if x.goal_test():
            return (build_path(x, None), nodes)
        for action in actions:
            if (x.parent != None) and (x.parent_move[0] == action[0]) and (x.parent_move[1] != action[1]):
                continue
            heapq.heappush(heap, x.move(*action))
            nodes.change_generated(1)
            nodes.change_in_mem(1)

    return False, nodes


def main():
    r = get_rubik()
    result, nodes = a_star(r)
    show_solution((result, nodes))

if __name__ == '__main__':
    main()
