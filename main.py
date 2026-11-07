from src.graph_builder import carregar_dados, construir_grafo
from src.bfs import busca_em_largura
from src.dfs import busca_em_profundidade
from src.metrics import analisar_metricas

from src.visualization import (
    gerar_grafo,
    gerar_ranking_canais,
    gerar_grafico_faixa_etaria,
    gerar_grafico_exposicao
)


def main():

    # Carregamento dos dados
    dados = carregar_dados()

    # Construção do grafo
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

    # Geração das visualizações
    gerar_grafo(grafo)
    gerar_ranking_canais(grafo)

    # Novos gráficos da pesquisa
    gerar_grafico_faixa_etaria(dados)
    gerar_grafico_exposicao(dados)

    print("\n===== VISUALIZAÇÕES GERADAS =====")
    print("- outputs/grafo_bipartido.png")
    print("- outputs/ranking_canais.png")
    print("- outputs/distribuicao_faixa_etaria.png")
    print("- outputs/exposicao_jogos_azar.png")


if __name__ == "__main__":
    main()