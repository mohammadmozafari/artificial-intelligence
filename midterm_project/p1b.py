from collections import deque
from p1a import *

def bidirectional_search(rubik):
    """
    This method takes a rubik puzzle and tries to solve it using bidirectional search strategy
    """
    nodes = NodeCount()
    if rubik.goal_test():
        return (build_path(rubik, None), nodes)

    visited1 = set()
    visited2 = set()
    q1 = deque()
    q2 = deque()
    q1.append(rubik)
    visited1.add(rubik)
    add_goals_to_queue(q2, visited2)
    nodes.change_generated(len(q1) + len(q2))
    nodes.change_in_mem(len(q1) + len(q2))
    intersect = (None, None)
    actions = Rubik.get_all_actions()

    while (len(q1) != 0) and (len(q2) != 0):
        if (len(q1) != 0):
            x = q1.popleft()
            nodes.change_in_mem(-1)
            nodes.change_expanded(1)
            for action in actions:
                xprime = x.move(action[0], action[1])
                nodes.change_generated(1)
                brk = False
                if xprime.goal_test():
                    intersect = (xprime, None)
                    brk = True
                    break
                else:
                    try:
                        i = q2.index(xprime)
                        intersect = (xprime, q2[i])
                        brk = True
                        break
                    except:
                        pass
                    if not (xprime in visited1):
                        visited1.add(xprime)
                        q1.append(xprime)
                        nodes.change_in_mem(2)
            if brk: break

        if (len(q2) != 0):
            xprime = q2.popleft()
            nodes.change_in_mem(-1)
            nodes.change_expanded(1)
            for action in actions:
                x = xprime.move(action[0], action[1])
                nodes.change_generated(1)
                brk = False
                if x == rubik:
                    intersect = (None, x)
                    brk = True
                    break
                else:
                    try:
                        i = q1.index(x)
                        intersect = (q1[i], x)
                        brk = True
                        break
                    except:
                        pass
                    if not (x in visited2):
                        visited2.add(x)
                        q2.append(x)
                        nodes.change_in_mem(2)
            if brk: break
    
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
