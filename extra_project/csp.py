import copy
import time

class CSP:
    def __init__(self, length, domain, is_safe, check):
        assert length == len(domain), 'dimension of domain is not consistant with length'
        
        self.length = length
        self.domain = domain
        self.check = check
        self.is_safe = is_safe

    def solve(self, fc, mrv):
        answer = [None for i in range(self.length)]
        if (not fc) and (not mrv):
            return self.backtrack(answer, 0)
        elif fc and (not mrv):
            return self.backtrack_fc(answer, 0, self.domain)

        # def backtrack(at, domain):
        #     if fc:
        #         pass
        #     else:


        #     my_domain = copy.deepcopy(domain)

        #     for option in my_domain[at]:
        #         answer[at] = option
        #         my_domain[at] = [option]

        #         if fc:
        #             empty = self.check(answer, at, my_domain)
        #             if empty:
        #                 answer[at] = None
        #                 my_domain = copy.deepcopy(domain)
        #                 continue
        #             if None not in answer:
        #                 return answer
        #             else:
        #                 return backtrack(at + 1, my_domain)

        #         else:
        #             if self.is_safe(answer):
        #                 if (None not in answer):
        #                     return answer
        #                 if backtrack(at + 1, domain):
        #                     return answer
        #     return False
        

    def backtrack(self, answer, at):
        for option in self.domain[at]:
            answer[at] = option
            if self.is_safe(answer):
                if (None not in answer):
                    return answer
                if self.backtrack(answer, at + 1):
                    return answer
            answer[at] = None
        return False

    def backtrack_fc(self, answer, at, domain):
        my_domain = copy.deepcopy(domain)
        for option in my_domain[at]:
            answer[at] = option
            my_domain[at] = [option]
            empty = self.check(answer, at, my_domain)
            if empty:
                answer[at] = None
                my_domain = copy.deepcopy(domain)
                continue
            if None not in answer:
                return answer
            else:
                return self.backtrack_fc(answer, at + 1, my_domain)

def forward_check(graph, node_types, answer, node, domain):

    for nei1 in graph[node]:
        if node_types[nei1] == 'C': continue
        do_sum = node_types[nei1] == 'P' or node_types[nei1] == 'H'
        do_left = node_types[nei1] == 'T' or node_types[nei1] == 'P'

        all_possible = [answer[node]]
        for nei2 in graph[node]:
            if (nei2 == node):
                continue
            temp = []
            for y in all_possible:
                for d in domain[nei2]:
                    if do_sum:
                        temp.append(y + d)
                    else:
                        temp.append(y * d)

            all_possible = temp
        
        for i in range(len(all_possible)):
            n = all_possible[i]
            if do_left:
                while n >= 10: n = n // 10
            else: n = n % 10
            all_possible[i] = n

        i = 0
        while i < len(domain[nei1]):
            x = domain[nei1][i]
            if x not in all_possible:
                list.remove(domain[nei1], x)
                i -= 1
            i += 1

        if len(domain[nei1]) == 0:
            return True

    return False

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
    _, graph, node_types = get_input()
    domain = [[(i + 1) for i in range(9)] for j in range(len(graph))]

    csp = CSP(len(graph), domain, lambda x: is_safe(graph, node_types, x),  lambda x, y, z: forward_check(graph, node_types, x, y, z))
    
    beg = time.time()
    print(csp.solve(fc=True, mrv=False))
    end = time.time()
    print(end - beg)

if __name__ == '__main__':
    main()
