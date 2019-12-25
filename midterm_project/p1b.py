from collections import deque
from p1a import *

def bidirectional_search(rubik):
    """
    This method takes a rubik puzzle and tries to solve it using bidirectional search strategy
    """
    nodes = NodeCount()
    visited = set()
    q1 = deque()
    q2 = deque()
    q1.append(rubik)
    visited.add(rubik)
    add_goals_to_queue(q2, visited)

    nodes.change_generated(len(q1) + len(q2))
    nodes.change_in_mem(len(q1) + len(q2))

    intersect = (None, None)    
    actions = [(0, True), (0, False), (1, True), (1, False), (2, True), (2, False), (3, True), (3, False), (4, True), (4, False), (5, True), (5, False)]
    while (len(q1) != 0) and (len(q2) != 0):
        if (len(q1) != 0):
            x = q1.popleft()
            nodes.change_in_mem(-1)
            if x.goal_test():
                intersect = (x, None)
                break
            if x in q2:
                print('yyy')
                for i in q2:
                    if i == x:
                        intersect = (x, i)
                        break
                break
            nodes.change_expanded(1)
            for action in actions:
                xprime = x.move(*action)
                nodes.change_generated(1)
                if not (xprime in visited):
                    visited.add(xprime)
                    q1.append(xprime)
                    nodes.change_in_mem(2)
                else:
                    # TODO: resolve duplicate x'
                    pass

        if (len(q2) != 0):
            xprime = q2.popleft()
            nodes.change_in_mem(-1)
            if xprime == rubik:
                intersect = (None, xprime)
                break
            if xprime in q1:
                print('xxx')
                for i in q1:
                    if i == xprime:
                        intersect = (i, xprime)
                        break
                break
            nodes.change_expanded(1)
            for action in actions:
                x = xprime.move(*action)
                nodes.change_generated(1)
                if not (x in visited):
                    visited.add(x)
                    q2.append(x)
                    nodes.change_in_mem(2)
                else:
                    # TODO: resolve duplicate x'
                    pass
    
    if intersect == (None, None):
        return (False, nodes)

    return (build_path(intersect[0], intersect[1]), nodes)
     
def add_goals_to_queue(q, visited):
    """
    This method adds all the goals states to the given queue.
    Then marks all the goal states as visited.
    Inputs:
    - q: deque to add the goal states
    - visisted: set of the visited states
    """
    g = Rubik([[[0, 0], [0, 0]], [[1, 1], [1, 1]], [[2, 2], [2, 2]], [[3, 3], [3, 3]], [[4, 4], [4, 4]], [[5, 5], [5, 5]]], None, None)
    visited.add(g)
    q.append(g)

    # for i in range(6):
    #     for j in range(4):
    #         visited.add(g)
    #         q.append(g)
    #         g = g.move(2, False).move(5, True)
        
    #     if i <= 3:
    #         g = g.move(0, False).move(4, True)
    #     if i == 3:
    #         g = g.move(3, True).move(1, False)
    #     if i == 4:
    #         g = g.move(3, True).move(3, True).move(1, False).move(1, False)

def main():
    r = get_rubik()
    result, nodes = bidirectional_search(r)
    show_solution((result, nodes))

if __name__ == '__main__':
    main()
