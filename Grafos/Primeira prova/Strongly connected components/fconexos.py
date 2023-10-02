import networkx as nx
import matplotlib.pyplot as plt

def fconexos(graph):
    def dfs_reverse(node, visitado, pilha):
        visitado[node] = True
        for neighbor in graph.predecessors(node):
            if not visitado[neighbor]:
                dfs_reverse(neighbor, visitado, pilha)
        pilha.append(node)

    def dfs(node, visitado, scc):
        visitado[node] = True
        scc.add(node)
        for neighbor in graph.neighbors(node):
            if not visitado[neighbor]:
                dfs(neighbor, visitado, scc)

    visitado = {node: False for node in graph.nodes()}
    pilha = []

    for node in graph.nodes():
        if not visitado[node]:
            dfs_reverse(node, visitado, pilha)

    reversed_graph = graph.reverse()

    strongly_connected_components = []
    visitado = {node: False for node in reversed_graph.nodes()}

    while pilha:
        node = pilha.pop()
        if not visitado[node]:
            scc = set()
            dfs(node, visitado, scc)
            if len(scc) > 1:  # Verificar se o tamanho do SCC é maior que 1
                strongly_connected_components.append(scc)

    return strongly_connected_components

G = nx.read_edgelist("arquivo.txt", create_using = nx.DiGraph())

scc = fconexos(G)

print(scc)

nx.draw(G, with_labels=True, font_weight='regular')
plt.show()    

