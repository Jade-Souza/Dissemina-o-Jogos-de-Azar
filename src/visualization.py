import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path


# Caminho onde as visualizações serão salvas
PASTA_OUTPUTS = Path("outputs")

# Colunas da planilha original
COLUNA_IDADE = "Qual é a sua faixa etária?"

COLUNA_EXPOSICAO = (
    "Você já teve contato com conteúdos ou anúncios relacionados "
    "a apostas ou jogos de azar na internet?"
)


def preparar_pasta():
    """Cria a pasta de saída caso ela ainda não exista."""
    PASTA_OUTPUTS.mkdir(parents=True, exist_ok=True)


def gerar_grafo(grafo):
    """Gera a visualização do grafo bipartido."""

    preparar_pasta()

    participantes = [
        no for no, dados in grafo.nodes(data=True)
        if dados["tipo"] == "participante"
    ]

    canais = [
        no for no, dados in grafo.nodes(data=True)
        if dados["tipo"] == "canal"
    ]

    posicoes = nx.bipartite_layout(
        grafo,
        participantes,
        align="vertical",
        scale=2
    )

    plt.figure(figsize=(16, 12))

    nx.draw_networkx_edges(
        grafo,
        posicoes,
        alpha=0.25,
        width=0.8
    )

    nx.draw_networkx_nodes(
        grafo,
        posicoes,
        nodelist=participantes,
        node_size=35,
        node_color="skyblue",
        label="Participantes"
    )

    nx.draw_networkx_nodes(
        grafo,
        posicoes,
        nodelist=canais,
        node_size=900,
        node_color="orange",
        label="Canais"
    )

    # Identifica apenas os canais
    nx.draw_networkx_labels(
        grafo,
        posicoes,
        labels={canal: canal for canal in canais},
        font_size=9,
        font_weight="bold"
    )

    plt.title(
        "Grafo bipartido: participantes e canais de exposição",
        fontsize=14
    )

    plt.legend()
    plt.axis("off")
    plt.tight_layout()

    plt.savefig(
        PASTA_OUTPUTS / "grafo_bipartido.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def gerar_ranking_canais(grafo):
    """Gera um gráfico com o grau de cada canal."""

    preparar_pasta()

    canais = [
        no for no, dados in grafo.nodes(data=True)
        if dados["tipo"] == "canal"
    ]

    ranking = sorted(
        [(canal, grafo.degree(canal)) for canal in canais],
        key=lambda item: item[1],
        reverse=True
    )

    nomes = [item[0] for item in ranking]
    valores = [item[1] for item in ranking]

    plt.figure(figsize=(11, 6))

    barras = plt.barh(nomes, valores)

    plt.bar_label(barras, padding=4)

    plt.title("Quantidade de participantes por canal")
    plt.xlabel("Número de participantes")
    plt.ylabel("Canal")
    plt.gca().invert_yaxis()

    plt.tight_layout()

    plt.savefig(
        PASTA_OUTPUTS / "ranking_canais.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def gerar_grafico_faixa_etaria(dados):
    """Gera um gráfico com a distribuição dos participantes por idade."""

    preparar_pasta()

    ordem_faixas = [
        "18 a 24 anos",
        "25 a 34 anos",
        "35 a 44 anos",
        "45 a 54 anos",
        "55 anos ou mais"
    ]

    respostas = dados[COLUNA_IDADE].dropna().astype(str).str.strip()

    frequencias = respostas.value_counts()

    valores = [
        frequencias.get(faixa, 0)
        for faixa in ordem_faixas
    ]

    plt.figure(figsize=(9, 5))

    barras = plt.bar(ordem_faixas, valores)

    plt.bar_label(barras, padding=3)

    plt.title("Distribuição dos participantes por faixa etária")
    plt.xlabel("Faixa etária")
    plt.ylabel("Número de participantes")

    plt.xticks(rotation=15)
    plt.tight_layout()

    plt.savefig(
        PASTA_OUTPUTS / "distribuicao_faixa_etaria.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def gerar_grafico_exposicao(dados):
    """Gera um gráfico com a exposição aos jogos de azar online."""

    preparar_pasta()

    respostas = (
        dados[COLUNA_EXPOSICAO]
        .dropna()
        .astype(str)
        .str.strip()
        .str.capitalize()
    )

    categorias = ["Sim", "Não"]

    frequencias = respostas.value_counts()

    valores = [
        frequencias.get(categoria, 0)
        for categoria in categorias
    ]

    total = sum(valores)

    plt.figure(figsize=(7, 5))

    barras = plt.bar(categorias, valores)

    rotulos = [
        f"{valor} ({valor / total * 100:.1f}%)" if total > 0
        else "0"
        for valor in valores
    ]

    plt.bar_label(barras, labels=rotulos, padding=3)

    plt.title("Exposição aos jogos de azar online")
    plt.xlabel("Resposta")
    plt.ylabel("Número de participantes")

    plt.tight_layout()

    plt.savefig(
        PASTA_OUTPUTS / "exposicao_jogos_azar.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()