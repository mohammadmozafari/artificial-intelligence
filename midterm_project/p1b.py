from collections import deque
from p1a import *

def bidirectional_search(rubik):
    """
    This method takes a rubik puzzle and tries to solve it using bidirectional search strategy
    """
    nodes = NodeCount()
    temp_ls = []
    visited1 = set()
    visited2 = set()
    q1 = deque()
    q2 = deque()
    q1.append(rubik)
    temp_ls.append(rubik)
    visited1.add(id(rubik))
    add_goals_to_queue(q2, visited2)
    intersect = (None, None)
    actions = Rubik.get_all_actions()
    nodes.change_generated(1 + len(q2))
    nodes.change_in_mem(1 + len(q2))

    while q1 or q2:
        if q1:
            x = q1.popleft()
            nodes.change_in_mem(-1)
            nodes.change_expanded(1)
            for i in q2:
                if i == x:
                    return (build_path(x, i), nodes)
            for action in actions:
                xprime = x.move(action[0], action[1])
                nodes.change_generated(1)
                if xprime not in visited1:
                    visited1.add(xprime)
                    q1.append(xprime)
                    nodes.change_in_mem(2)

        if q2:
            xprime = q2.popleft()
            nodes.change_in_mem(-1)
            nodes.change_expanded(1)
            for i in q1:
                if i == xprime:
                    return (build_path(xprime, i), nodes)
            for action in actions:
                x = xprime.move(action[0], action[1])
                nodes.change_generated(1)
                if x not in visited2:
                    visited2.add(x)
                    q2.append(x)
                    nodes.change_in_mem(2)

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
    g = Rubik(np.array([[0, 0, 0, 0],
                        [1, 1, 1, 1],
                        [2, 2, 2, 2],
                        [3, 3, 3, 3],
                        [4, 4, 4, 4],
                        [5, 5, 5, 5]]), alg=2)
    visited.add(g)
    q.append(g)
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
