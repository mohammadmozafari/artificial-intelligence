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
    g = p1a.Rubik([[[0, 0], [0, 0]], [[1, 1], [1, 1]], [[2, 2], [2, 2]], [[3, 3], [3, 3]], [[4, 4], [4, 4]], [[5, 5], [5, 5]]])

    for i in range(6):
        for j in range(4):
            visited.add(g)
            q.append(g)
            g = g.move(2, False).move(5, True)
        
        if i <= 3:
            g = g.move(0, False).move(4, True)
        if i == 3:
            g = g.move(3, True).move(1, False)
        if i == 4:
            g = g.move(3, True).move(3, True).move(1, False).move(1, False)