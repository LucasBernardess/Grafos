import networkx as nx
from collections import deque

def fordFulkerson(grafo, origem, destino):
    # Inicializa o fluxo máximo como 0
    fluxo_maximo = 0

    # Enquanto houver um caminho aumentante no grafo residual
    while True:
        # Encontra um caminho aumentante usando a busca em largura
        caminho, capacidade = encontrarCaminhoAumentante(grafo, origem, destino)

        # Se não houver mais caminho aumentante, termina o loop
        if caminho is None:
            break

        # Atualiza o grafo residual e o fluxo máximo
        atualizarGrafoResidual(grafo, caminho, capacidade)
        fluxo_maximo += capacidade

    return fluxo_maximo

def encontrarCaminhoAumentante(grafo, origem, destino):
    fila = deque([origem])
    antecessor = {origem: None}

    while fila:
        atual = fila.popleft()

        if atual not in grafo:
            continue  # Evita o erro se o nó não estiver no grafo

        for vizinho, dados_aresta in grafo[atual].items():
            if 'capacidade' not in dados_aresta or 'fluxo' not in dados_aresta:
                continue  # Evita o erro se as chaves necessárias não estiverem presentes

            capacidade_residual = dados_aresta['capacidade'] - dados_aresta['fluxo']

            if capacidade_residual > 0 and vizinho not in antecessor:
                antecessor[vizinho] = atual
                if vizinho == destino:
                    # Encontrou o caminho aumentante
                    caminho = []
                    while vizinho is not None:
                        caminho.insert(0, vizinho)
                        vizinho = antecessor[vizinho]

                    # Calcula a capacidade do caminho aumentante considerando a capacidade residual
                    capacidade = min(capacidade_residual for u, v in zip(caminho, caminho[1:]) 
                                    if 'capacidade' in grafo[u][v] and 'fluxo' in grafo[u][v] and grafo[u][v]['capacidade'] - grafo[u][v]['fluxo'] > 0)

                    return caminho, capacidade

                fila.append(vizinho)

    # Não há mais caminhos aumentantes
    return None, 0

def atualizarGrafoResidual(grafo, caminho, capacidade):
    # Atualiza o grafo residual subtraindo o fluxo do caminho aumentante
    for i in range(len(caminho) - 1):
        u, v = caminho[i], caminho[i + 1]
        
        # Atualiza o fluxo na aresta direta
        grafo[u][v]['fluxo'] += capacidade
        
        # Certifica-se de que a aresta reversa exista
        if not grafo.has_edge(v, u):
            grafo.add_edge(v, u, capacidade=0, fluxo=0)
        else:
            # Atualiza o fluxo na aresta reversa considerando a capacidade original
            grafo[v][u]['fluxo'] -= capacidade


# Função para ler o grafo a partir de um arquivo
def lerGrafoDoArquivo(nome_arquivo):
    grafo = nx.DiGraph()
    
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            u, v, capacidade = map(int, linha.strip().split())
            grafo.add_edge(u, v, capacidade=capacidade, fluxo=0)
    
    return grafo

def main():
    grafo = lerGrafoDoArquivo('arquivo.txt')
    
    origem, destino = 1, 5
    
    fluxo_maximo = fordFulkerson(grafo, origem, destino)
    print(f"Fluxo Máximo: {fluxo_maximo}")
    
    # Imprime o fluxo em cada aresta
    for u, v, dados in grafo.edges(data=True):
        print(f"Aresta ({u}, {v}): Fluxo = {dados['fluxo']}")

if __name__ == "__main__":
    main()