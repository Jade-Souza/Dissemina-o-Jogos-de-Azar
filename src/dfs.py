def busca_em_profundidade(grafo, inicio):
    """
    Executa a busca em profundidade (DFS).

    Retorna a ordem em que os vértices são visitados.
    """

    if inicio not in grafo:
        raise ValueError("Vértice inicial não encontrado.")

    visitados = set()
    pilha = [inicio]
    ordem_visita = []

    while pilha:

        vertice = pilha.pop()

        if vertice not in visitados:

            visitados.add(vertice)
            ordem_visita.append(vertice)

            vizinhos = sorted(grafo.neighbors(vertice), reverse=True)

            for vizinho in vizinhos:

                if vizinho not in visitados:
                    pilha.append(vizinho)

    return ordem_visita