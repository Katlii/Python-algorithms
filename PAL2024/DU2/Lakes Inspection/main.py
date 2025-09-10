from collections import defaultdict, deque
import sys
sys.setrecursionlimit(10**6)

class LakeDistrict:
    def __init__(self, LA, CA, DO, canals):
        self.LA = LA  
        self.CA = CA  
        self.DO = DO  
        self.graph = defaultdict(list) 
        self.reverse_graph = defaultdict(list)
        self.sccs = [] 
        self.scc_id = [-1] * LA 
        self.canals = canals

        for a, b in canals:
            self.graph[a].append(b)
            self.reverse_graph[b].append(a)

    def dfs(self, graph, node, start, visited, path_cost, moved, path, best_result, component_costs):
        if node == start and moved:
            if path_cost > best_result['max_cost']:
                best_result['max_cost'] = path_cost
                best_result['max_path'] = path[:]
            return

        visited.add(node)
        path.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited or neighbor == start:
                self.dfs(graph, neighbor, start, visited.copy(), path_cost + component_costs[neighbor], moved or neighbor != start, path, best_result, component_costs)

        path.pop()

    def find_max_cycle_path_from_start(self, graph, component_costs, start_node):
        visited = set()
        best_result = {'max_cost': 0, 'max_path': []}
        path = []
        self.dfs(graph, start_node, start_node, visited, component_costs[start_node], moved=False, path=path, best_result=best_result, component_costs=component_costs)
        return best_result['max_path']

    def kosaraju_scc(self):
        visited = [False] * self.LA
        order = []

        def dfs(node):
            visited[node] = True
            for neighbor in self.graph[node]:
                if not visited[neighbor]:
                    dfs(neighbor)
            order.append(node)

        for i in range(self.LA):
            if not visited[i]:
                dfs(i)

        visited = [False] * self.LA

        def reverse_dfs(node, current_scc):
            visited[node] = True
            self.scc_id[node] = len(self.sccs)
            current_scc.append(node)
            for neighbor in self.reverse_graph[node]:
                if not visited[neighbor]:
                    reverse_dfs(neighbor, current_scc)

        for node in reversed(order):
            if not visited[node]:
                current_scc = []
                reverse_dfs(node, current_scc)
                self.sccs.append(current_scc)

    def build_scc_graph(self):
        scc_graph = defaultdict(list)
        for a, b in self.canals:
            if self.scc_id[a] != self.scc_id[b]:
                scc_graph[self.scc_id[a]].append(self.scc_id[b])
        for i in range(len(self.sccs)):
            if i not in scc_graph:
                scc_graph[i] = []
        print("scc_graph", scc_graph)
        return scc_graph

    def max_lakes_to_visit(self):
        self.kosaraju_scc()
        scc_graph = self.build_scc_graph()

        component_costs = {}
        for i in range(len(self.sccs)):
            component_costs[i] = len(self.sccs[i])
        start_scc = self.scc_id[self.DO]
        idk = []
        for a in scc_graph:
            for b in scc_graph[a]:
                if a == start_scc or b == start_scc:
                    scc_graph[a].remove(b)
                    scc_graph[b].append(a)
                    max_cycle_path = self.find_max_cycle_path_from_start(scc_graph, component_costs, start_scc)
                    idk.append(max_cycle_path)
                    scc_graph[a].append(b)
                    scc_graph[b].remove(a)
        maximum = 0
        for i in range(len(idk)):
            maximum = max(maximum, sum([component_costs[node] for node in idk[i]]))
        return maximum


def main():
    with open('datapub/pub01.in', 'r') as file:
        data = file.read().splitlines()
    LA, CA, DO = map(int, data[0].split())
    #LA, CA, DO = map(int, input().split())
    canals = []
    for _ in range(CA):
        #canals.append(tuple(map(int, input().split())))
        canals.append(tuple(map(int, data[_+1].split())))
    lake_district = LakeDistrict(LA, CA, DO, canals)
    result = lake_district.max_lakes_to_visit()
    print(result)



if __name__ == "__main__":
    main()