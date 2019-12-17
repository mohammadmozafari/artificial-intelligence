import midterm_project.p1a as p1a
from collections import deque

def bidirectional_search(rubik):
    """
    This method takes a rubik puzzle and tries to solve it using bidirectional search strategy
    """
    visited = set()
    
    q1 = deque()
    q2 = deque()
    q1.append(rubik)
    visited.add(rubik)
    add_goals_to_queue(q2, visited)
        
    actions = [(0, True), (0, False), (1, True), (1, False), (2, True), (2, False), (3, True), (3, False), (4, True), (4, False), (5, True), (5, False)]

    while (len(q1) != 0) and (len(q2) != 0):
       
        if (len(q1) != 0):
            x = q1.popleft()
            if (x.goal_test) or (x in q2):
                return 'success'
            for action in actions:
                xprime = rubik.move(*action)
                if not xprime in visited:
                    visited.add(xprime)
                    q1.append(xprime)
                else:
                    # TODO: resolve duplicate x'
                    pass

        if (len(q2) != 0):
            xprime = q2.popleft()
            if (x == rubik) or (x in q2):
                return 'success'
            for action in actions:
                x = rubik.move(*action)
                if not x in visited:
                    visited.add(x)
                    q2.append(x)
                else:
                    # TODO: resolve duplicate x'
                    pass
    return 'failure'
        
def add_goals_to_queue(q, visited):
    """
    This method adds all the goals states to the given queue.
    Then marks all the goal states as visited.
    Inputs:
    - q: deque to add the goal states
    - visisted: set of the visited states
    """
    g1 = p1a.Rubik([[[0, 0], [0, 0]], [[1, 1], [1, 1]], [[2, 2], [2, 2]], [[3, 3], [3, 3]], [[4, 4], [4, 4]], [[5, 5], [5, 5]]])
    g2 = p1a.Rubik([[[5, 5], [5, 5]], [[0, 0], [0, 0]], [[1, 1], [1, 1]], [[2, 2], [2, 2]], [[3, 3], [3, 3]], [[4, 4], [4, 4]]])
    g3 = p1a.Rubik([[[4, 4], [4, 4]], [[5, 5], [5, 5]], [[0, 0], [0, 0]], [[1, 1], [1, 1]], [[2, 2], [2, 2]], [[3, 3], [3, 3]]])
    g4 = p1a.Rubik([[[3, 3], [3, 3]], [[4, 4], [4, 4]], [[5, 5], [5, 5]], [[0, 0], [0, 0]], [[1, 1], [1, 1]], [[2, 2], [2, 2]]])
    g5 = p1a.Rubik([[[2, 2], [2, 2]], [[3, 3], [3, 3]], [[4, 4], [4, 4]], [[5, 5], [5, 5]], [[0, 0], [0, 0]], [[1, 1], [1, 1]]])
    g6 = p1a.Rubik([[[1, 1], [1, 1]], [[2, 2], [2, 2]], [[3, 3], [3, 3]], [[4, 4], [4, 4]], [[5, 5], [5, 5]], [[0, 0], [0, 0]]])
    visited.add(g1)
    visited.add(g2)
    visited.add(g3)
    visited.add(g4)
    visited.add(g5)
    visited.add(g6)
    q.append(g1)
    q.append(g2)
    q.append(g3)
    q.append(g4)
    q.append(g5)
    q.append(g6)
    
