import networkx as nx


def analisar_metricas(grafo):

    participantes = [
        no for no, dados in grafo.nodes(data=True)
        if dados["tipo"] == "participante"
    ]

    canais = [
        no for no, dados in grafo.nodes(data=True)
        if dados["tipo"] == "canal"
    ]

    componentes = list(nx.connected_components(grafo))

    maior_componente = max(componentes, key=len)

    participantes_maior = [
        no for no in maior_componente
        if no in participantes
    ]

    canais_maior = [
        no for no in maior_componente
        if no in canais
    ]

    isolados = [
        no for no in participantes
        if grafo.degree(no) == 0
    ]

    # Graus dos canais
    graus_canais = {
        canal: grafo.degree(canal)
        for canal in canais
    }

    # Densidade específica de um grafo bipartido
    densidade_bipartida = (
        grafo.number_of_edges()
        / (len(participantes) * len(canais))
    )

    # Grau médio dos participantes
    grau_medio_participantes = (
        sum(grafo.degree(no) for no in participantes)
        / len(participantes)
    )

    # Grau médio dos canais
    grau_medio_canais = (
        sum(grafo.degree(no) for no in canais)
        / len(canais)
    )

    print("\n===== MÉTRICAS DO GRAFO =====")

    print(f"Vértices: {grafo.number_of_nodes()}")
    print(f"Arestas: {grafo.number_of_edges()}")

    print(f"\nComponentes conexas: {len(componentes)}")

    print(
        f"Maior componente: {len(maior_componente)} vértices"
    )

    print(
        f"Participantes na maior componente: "
        f"{len(participantes_maior)}"
    )

    print(
        f"Canais na maior componente: "
        f"{len(canais_maior)}"
    )

    print(f"Participantes isolados: {len(isolados)}")

    print(
        f"\nDensidade bipartida: "
        f"{densidade_bipartida:.2%}"
    )

    print(
        f"Grau médio dos participantes: "
        f"{grau_medio_participantes:.2f}"
    )

    print(
        f"Grau médio dos canais: "
        f"{grau_medio_canais:.2f}"
    )

    print("\nRanking dos canais:")

    ranking = sorted(
        graus_canais.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for canal, grau in ranking:
        print(f"{canal}: {grau}")