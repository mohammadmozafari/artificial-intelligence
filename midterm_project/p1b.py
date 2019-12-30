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
     
# def add_goals_to_queue(q, visited):
#     """
#     This method adds all the goals states to the given queue.
#     Then marks all the goal states as visited.
#     Inputs:
#     - q: deque to add the goal states
#     - visisted: set of the visited states
#     """
#     g = Rubik(np.array([[0, 0, 0, 0],
#                         [1, 1, 1, 1],
#                         [2, 2, 2, 2],
#                         [3, 3, 3, 3],
#                         [4, 4, 4, 4],
#                         [5, 5, 5, 5]]), alg=2)
#     visited.add(g)
#     q.append(g)
    # for i in range(6):
    #     for j in range(4):
    #         visited.add(g)
    #         q.append(g)
    #         g = g.move(2, False).move(5, True)
    #         g.parent = None
    #         g.parent_move = None
    #     if i <= 3:
    #         g = g.move(0, False).move(4, True)
    #     if i == 3:
    #         g = g.move(3, True).move(1, False)
    #     if i == 4:
    #         g = g.move(3, True).move(3, True).move(1, False).move(1, False)
    #     g.parent = None
    #     g.parent_move = None

def main():
    r = get_rubik(2)
    result, nodes = bidirectional_search(r)
    show_solution((result, nodes))

if __name__ == '__main__':
    main()
