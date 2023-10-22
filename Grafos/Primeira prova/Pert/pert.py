import networkx as nx
import matplotlib.pyplot as plt

def calculate_TMC_TMT(G):
    vertices = list(G.nodes)
    edges = list(G.edges)
    
    vertex_data = [{"vertice": vertice, "TMC": 0, "TMT": 1000} for vertice in vertices]
    weightEdges = [G[edges[i][0]][edges[i][1]]['weight'] for i in range(len(edges))]
    
    # Cálculo dos tempos TMC
    for vertice in vertices:
        for i in range(len(edges)):
            if edges[i][1] == vertice:
                newTMC = vertex_data[edges[i][0] - 1].get("TMC") + weightEdges[i]
                if newTMC > vertex_data[vertice - 1].get("TMC"):
                    vertex_data[vertice - 1]["TMC"] = newTMC
    
    # Encontrando o último vértice do grafo
    fila = []
    for vertice in vertices:
        cont = 0
        for i in range(len(edges)):
            if vertice != edges[i][0]:
                cont += 1
        if cont == len(edges):
            fila.append(vertice)
            vertex_data[vertice - 1]["TMT"] = vertex_data[vertice - 1]["TMC"]
    
    # Cálculo dos tempos TMT
    for vertice in fila:
        for i in range(len(edges)):
            if edges[i][1] == vertice:
                antecessor = edges[i][0]
                weightEdges = G[edges[i][0]][edges[i][1]]['weight']
                newTMT = vertex_data[vertice - 1]["TMT"] - weightEdges
                if vertex_data[antecessor - 1]["TMT"] > newTMT:
                    vertex_data[antecessor - 1]["TMT"] = newTMT
                if antecessor not in fila:
                    fila.append(antecessor)
    
    return vertex_data, edges

def find_critical_path(vertex_data, edges):
    crit = []
    for edge in edges:
        begin = edge[0]
        end = edge[1]
        if vertex_data[begin - 1]["TMT"] - vertex_data[end - 1]["TMC"] == 0:
            crit.append(edge)
    return crit

G = nx.read_weighted_edgelist("arquivo.txt", nodetype=int, create_using=nx.DiGraph())
vertex_data, edges = calculate_TMC_TMT(G)

print("Tempo mais cedo e Tempo mais tarde de cada vértice:")
for vertice in vertex_data:
    print(vertice)

critical_path = find_critical_path(vertex_data, edges)
print("\nFaz parte do caminho crítico as arestas:", critical_path)

