class CSP:
    def __init__(self, length, domain, is_safe):
        assert length == len(domain), 'dimension of domain is not consistant with length'
        
        self.length = length
        self.is_safe = is_safe


    def solve(self):
        answer = [None for i in range(self.length)]
        def backtrack(until):
            for opt in self.options:
                answer[position] = opt
                if self.is_safe(answer):
                    if until >= self.length or backtrack(until + 1):
                        return answer
            return False
        return backtrack(0)


def is_safe(graph, node_types, answer):
    def mult_neis(index):
        x = 0
        for i in graph[index]:
            x *= (1 if answer[i] == None else answer[i])
        return x
    def sum_neis(index):
        x = 0
        for i in graph[index]:
            x += (1 if answer[i] == None else answer[i])
        return x

    for i, num in enumerate(answer):
        if num == None: continue
        if node_types[i] == 'T':
            m = mult_neis(i)
            while m > 9: m /= 10
            if m != num: return False
        elif node_types[i] == 'S':
            m = mult_neis(i)
            m %= 10
            if m != num: return False
        elif node_types[i] == 'P':
            s = sum_neis(i)
            while s > 9: s /= 10
            if s != num: return False
        elif node_types[i] == 'H':
            s = sum_neis(i)
            s %= 10
            if s != num: return False
        else: pass

def get_input():
    V, E = input().split(' ')
    V, E = int(V), int(E)
    graph = [[] for i in range(V)]
    node_types = input()
    for i in range(E):
        x, y = input().split(' ')
        x, y = int(x), int(y)
        graph[x].append(y)
        graph[y].append(x)
    return E, graph, node_types

def main():
    edges, graph, node_types = get_input()
    print(edges)
    print(graph)
    print(node_types)


if __name__ == '__main__':
    main()