from collections import defaultdict

class Graph:
    def __init__(self, num_nodes):
        self.adj_list = defaultdict(list)
        self.num_nodes = num_nodes

    def add_edge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def weisfeiler_lehman_hash(self, iterations=3):
        labels = {}
        for node, neighbors in self.adj_list.items():
            labels[node] = len(neighbors)

        for i in range(iterations):
            new_labels = {}
            for node in self.adj_list:
                neighbor_labels = []
                for neighbor in self.adj_list[node]:
                    neighbor_labels.append(labels[neighbor])
                neighbor_labels = sorted(neighbor_labels)
                new_labels[node] = hash((labels[node], tuple(neighbor_labels)))
            labels = new_labels

        all_labels = []
        for value in labels.values():
            all_labels.append(value)
        certificate = tuple(sorted(all_labels))
        return certificate

def process_graph(graph_data):
    A, B, bonds = graph_data
    graph = Graph(A)

    for bond in bonds:
        A1, A2 = bond
        graph.add_edge(A1, A2)

    return graph.weisfeiler_lehman_hash()

def main():
    M, A, B = map(int, input().split())

    molecules_data = []
    index = 1
    for _ in range(M):
        bonds = []
        for _ in range(B):
            A1, A2 =  map(int, input().split())
            bonds.append((A1, A2))
            index += 1
        molecules_data.append((A, B, bonds))
    certificates = []
    for molecule_data in molecules_data:
        certificates.append(process_graph(molecule_data))
    structural_classes = defaultdict(int)

    for cert in certificates:
        if cert in structural_classes:
            structural_classes[cert] += 1
        else:
            structural_classes[cert] = 1

    counts = []
    for count in structural_classes.values():
        counts.append(count)
    counts = sorted(counts)

    result = ""
    for count in counts:
        result += str(count) + " "
    print(result.strip())

if __name__ == "__main__":
    main()
