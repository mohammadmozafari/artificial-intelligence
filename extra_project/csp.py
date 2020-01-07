def solve(options, length, is_safe):
    """
    This is a general engine for backtracking. It can be applied to any CSP problem given
    proper inputs
    Inputs
    options: domain of the variables
    length: number of variables
    is_safe: function that checks if current assignment violates our constraints
    """
    answer = [None for i in range(length)]
    def backtrack(until):
        for opt in options:
            answer[position] = opt
            if is_safe(answer, until):
                if until >= length or backtrack(until + 1):
                    return answer
        return False
    return backtrack(0)