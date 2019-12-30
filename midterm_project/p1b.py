from collections import deque
from p1a import *
import time

def bidirectional_search(rubik):
    """
    This method takes a rubik puzzle and tries to solve it using bidirectional search strategy
    """
    nodes = NodeCount()
    g = Rubik.get_goal(2)
    visited1 = set([rubik])
    visited2 = set([g])
    
    q1 = deque([rubik])
    q2 = deque([g])

    actions = Rubik.get_all_actions()
    nodes.change_generated(1 + len(q2))
    nodes.change_in_mem(1 + len(q2))

    while q1 or q2:
        if q1:
            x = q1.popleft()
            nodes.change_in_mem(-1)
            nodes.change_expanded(1)
            if x in q2:
                return (build_path(x, q2[q2.index(x)]), nodes)
            for action in actions:
                xprime = x.move(action[0], action[1])
                nodes.change_generated(1)
                if xprime not in visited1:
                    visited1.add(xprime)
                    q1.append(xprime)
                    nodes.change_in_mem(2)

        if q2:
            x = q2.popleft()
            nodes.change_in_mem(-1)
            nodes.change_expanded(1)
            if x in q1:
                return (build_path(q1[q1.index(x)], x), nodes)
            for action in actions:
                xprime = x.move(action[0], action[1])
                nodes.change_generated(1)
                if xprime not in visited2:
                    visited2.add(xprime)
                    q2.append(xprime)
                    nodes.change_in_mem(2)
                    
    return (False, nodes)

def main():
    r = get_rubik()
    result, nodes = bidirectional_search(r)
    show_solution((result, nodes))

if __name__ == '__main__':
    main()
