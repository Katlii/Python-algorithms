#GOD HELP !
from collections import deque
import sys

sys.setrecursionlimit(100000)

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [1] * size

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])  # Path compression
        return self.parent[node]

    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 != root2:
            # Union by rank
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1
            return True
        return False

def kruskal(E, n):
    # Инициализация структуры для отслеживания соединений
    uf = UnionFind(n)

    mincost = 0
    edges_used = 0
    mst_edges = []

    for cost, u, v in E:
        # Найти корневые вершины для u и v
        root_u = uf.find(u)
        root_v = uf.find(v)

        # Если u и v принадлежат разным компонентам, добавляем ребро в MST
        if root_u != root_v:
            uf.union(root_u, root_v)
            mincost += cost
            mst_edges.append((u, v))
            edges_used += 1

        if edges_used == n - 1:
            break

    # Проверяем, удалось ли построить остовное дерево
    if edges_used != n - 1:
        print("No spanning tree")
        return None, []
    else:
        return mincost, mst_edges

def bfs_depth_and_parents(n, edges, root=0):
    parent = [-1] * n
    depth = [-1] * n
    adj_list = [[] for _ in range(n)]

    # Создание смежного списка только для тех вершин, которые имеют рёбра
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)

    # BFS для вычисления глубины и родителя
    queue = deque([root])
    depth[root] = 0

    while queue:
        node = queue.popleft()
        for neighbor in adj_list[node]:
            if depth[neighbor] == -1:  # Если вершина не посещена
                parent[neighbor] = node
                depth[neighbor] = depth[node] + 1
                queue.append(neighbor)

    return parent, depth

def preprocess_lca(n, parent):
    LOG = max(1, n.bit_length())  # Определяем логарифм от n более точно, чтобы уменьшить размер up
    up = [[-1] * LOG for _ in range(n)]

    for v in range(n):
        up[v][0] = parent[v]

    for j in range(1, LOG):
        for v in range(n):
            if up[v][j - 1] != -1:
                tmp = up[v][j - 1]
                up[v][j] = up[up[v][j - 1]][j - 1]

    return up

def find_lca(u, v, depth, up, parent):
    if depth[u] < depth[v]:
        u, v = v, u

    LOG = len(up[0])

    # Поднимаем u на тот же уровень, что и v
    for i in range(LOG - 1, -1, -1):
        if depth[u] - (1 << i) >= depth[v]:
            u = up[u][i]

    if u == v:
        return u

    # Поднимаем u и v одновременно
    for i in range(LOG - 1, -1, -1):
        if up[u][i] != up[v][i]:
            u = up[u][i]
            v = up[v][i]

    return parent[u]

def kruskal_second_network(E, n, first_network_edges, max_cycle_length, parent, depth, up):
    # Инициализация структуры для отслеживания соединений
    uf = UnionFind(n)

    mincost = 0
    edges_used = 0

    for cost, u, v in E:
        # Пропускаем рёбра, которые использованы в первой сети
        if (u, v) in first_network_edges or (v, u) in first_network_edges:
            continue

        # Найти корневые вершины для u и v
        root_u = uf.find(u)
        root_v = uf.find(v)

        # Если u и v принадлежат разным компонентам, добавляем ребро в MST
        if root_u != root_v:
            # Проверяем длину цикла, который может образоваться
            lca = find_lca(u, v, depth, up, parent)
            cycle_length = depth[u] + depth[v] - 2 * depth[lca] + 1

            if cycle_length <= max_cycle_length:
                uf.union(root_u, root_v)
                mincost += cost
                edges_used += 1

        if edges_used == n - 1:
            break

    # Проверяем, удалось ли построить вторую сеть
    if edges_used != n - 1:
        print("No second spanning tree")
        return None
    else:
        return mincost

def main():
    # n, m, D = map(int, input().split())
    # edges = []
    # for _ in range(m):
    #     u, v, cost = map(int, input().split())
    #     edges.append((cost, u - 1, v - 1)) # Индексируем с нуля для удобства работы с UnionFind
    with open ('datapub/pub08.in', 'r') as file:
        lines = file.read().splitlines()
        n, m, D = map(int, lines[0].split())
        edges = []
        for i in range(1, m + 1):
            u, v, cost = map(int, lines[i].split())
            edges.append((cost, u - 1, v - 1))

    # Применение алгоритма Крускала для первой сети
    first_result, first_network_edges_list = kruskal(edges, n)
    if first_result is None:
        return

    # Создание словаря для отслеживания рёбер первой сети
    first_network_edges = {(u, v): True for u, v in first_network_edges_list}

    # Предварительное вычисление глубины и родителей с помощью BFS
    parent, depth = bfs_depth_and_parents(n, first_network_edges_list)
    up = preprocess_lca(n, parent)

    # Применение алгоритма Крускала для второй сети с ограничением на длину цикла
    second_result = kruskal_second_network(edges, n, first_network_edges, D, parent, depth, up)
    print(first_result % 65536, second_result % 65536)

if __name__ == "__main__":
    main()
