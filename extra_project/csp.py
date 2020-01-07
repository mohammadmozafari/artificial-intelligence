class CSP:
    def __init__(self, length, domain, is_safe):
        assert length == len(domain), 'dimension of domain is not consistant with length'
        
        self.length = length
        self.domain = domain
        self.is_safe = is_safe

    def solve(self):
        answer = [None for i in range(self.length)]
        def backtrack(at):
            for option in self.domain[at]:
                answer[at] = option
                if self.is_safe(answer):
                    if (None not in answer):
                        return answer
                    if backtrack(at + 1):
                        return answer
                answer[at] = None
            return False
        return backtrack(0)


def is_safe(graph, node_types, answer):
    def mult_neis(neis):
        x = 1
        for i in neis:
            x *= i
        return x

    def sum_neis(neis):
        x = 0
        for i in neis:
            x += i
        return x

    for i, num in enumerate(answer):
        if num == None: continue
        neis = [answer[j] for j in graph[i]]
        if None in neis: continue

        if node_types[i] == 'T':
            m = mult_neis(neis)
            while m > 9: m //= 10
            if m != num: return False
        elif node_types[i] == 'S':
            m = mult_neis(neis)
            m %= 10
            if m != num: return False
        elif node_types[i] == 'P':
            s = sum_neis(neis)
            while s > 9: s //= 10
            if s != num: return False
        elif node_types[i] == 'H':
            s = sum_neis(neis)
            s %= 10
            if s != num: return False
        else: pass
    return True

def get_input():
    V, E = input().split(' ')
    V, E = int(V), int(E)
    graph = [[] for i in range(V)]
    node_types = input().split(' ')
    for i in range(E):
        x, y = input().split(' ')
        x, y = int(x), int(y)
        graph[x].append(y)
        graph[y].append(x)
    return E, graph, node_types

def main():
    edges, graph, node_types = get_input()
    domain = [[(i + 1) for i in range(9)] for j in range(len(graph))]

    csp = CSP(len(graph), domain, lambda x: is_safe(graph, node_types, x))
    print(csp.solve())

if __name__ == '__main__':
    main()
