from pathlib import Path

import networkx as nx

from src.graph_builder import carregar_dados, construir_grafo
from src.bfs import busca_em_largura
from src.dfs import busca_em_profundidade
from src.metrics import analisar_metricas

from src.visualization import (
    gerar_ranking_canais,
    gerar_grafico_faixa_etaria,
    gerar_grafico_exposicao,
)


def main():
    # Carregamento dos dados
    dados = carregar_dados()

    # Construção do grafo bipartido
    grafo = construir_grafo(dados)

    # Execução dos algoritmos
    inicio = "Instagram"
    resultado_bfs = busca_em_largura(grafo, inicio)
    resultado_dfs = busca_em_profundidade(grafo, inicio)

    print("\n===== BUSCA EM LARGURA (BFS) =====")
    print(f"Total visitado: {len(resultado_bfs)}")

    print("\n===== BUSCA EM PROFUNDIDADE (DFS) =====")
    print(f"Total visitado: {len(resultado_dfs)}")

    # Análise das métricas
    analisar_metricas(grafo)

    # Exportação do grafo para visualização e edição no Gephi
    pasta_outputs = Path("outputs")
    pasta_outputs.mkdir(parents=True, exist_ok=True)
    caminho_gexf = pasta_outputs / "grafo_apostas.gexf"
    nx.write_gexf(grafo, caminho_gexf)

    # Gráficos estatísticos. A disposição visual do grafo é feita no Gephi.
    gerar_ranking_canais(grafo)
    gerar_grafico_faixa_etaria(dados)
    gerar_grafico_exposicao(dados)

    print("\n===== ARQUIVOS GERADOS =====")
    print(f"- {caminho_gexf}")
    print("- outputs/ranking_canais.png")
    print("- outputs/distribuicao_faixa_etaria.png")
    print("- outputs/exposicao_jogos_azar.png")
    print("\nImporte o arquivo GEXF no Gephi para montar a visualização do grafo.")


if __name__ == "__main__":
    main()
