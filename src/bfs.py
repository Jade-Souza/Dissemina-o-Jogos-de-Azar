from collections import deque


def busca_em_largura(grafo, inicio):
    """
    Executa a busca em largura (BFS).

    Retorna a ordem em que os vértices são visitados.
    """

    if inicio not in grafo:
        raise ValueError("Vértice inicial não encontrado.")

    visitados = set()
    fila = deque([inicio])
    ordem_visita = []

    visitados.add(inicio)

    while fila:

        vertice = fila.popleft()
        ordem_visita.append(vertice)

        for vizinho in sorted(grafo.neighbors(vertice)):

            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)

    return ordem_visita