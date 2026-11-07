import pandas as pd
import networkx as nx
import xml.etree.ElementTree as ET


CAMINHO_PLANILHA = "data/dados_originais.xlsx"
CAMINHO_GRAFO = "outputs/grafo_apostas.gexf"

COLUNA_CANAIS = (
    "Qual foi a principal forma pela qual você teve contato "
    "com esse tipo de conteúdo?"
)

CANAIS = [
    "Instagram",
    "YouTube",
    "Influenciadores",
    "Amigos/conhecidos",
    "TikTok",
    "Sites esportivos",
    "Facebook",
    "Outro",
    "X/Twitter"
]

CORRECOES = {
    "Amingos/conhecidos": "Amigos/conhecidos",
    "SItes esportivos": "Sites esportivos"
}


def carregar_dados():
    """Carrega as respostas do formulário."""

    return pd.read_excel(CAMINHO_PLANILHA)


def construir_grafo(dados):
    """Constrói o grafo bipartido de participantes e canais."""

    grafo = nx.Graph()

    # Adiciona os participantes
    for indice in range(len(dados)):
        participante = f"P{indice + 1:03d}"

        grafo.add_node(
            participante,
            label="",
            tipo="participante",
            bipartite=0
        )

    # Adiciona os canais
    for canal in CANAIS:
        grafo.add_node(
            canal,
            label=canal,
            tipo="canal",
            bipartite=1
        )

    # Cria as arestas
    for indice, resposta in enumerate(dados[COLUNA_CANAIS]):

        if pd.isna(resposta):
            continue

        participante = f"P{indice + 1:03d}"

        canais_selecionados = [
            canal.strip()
            for canal in str(resposta).split(",")
        ]

        for canal in canais_selecionados:

            canal = CORRECOES.get(canal, canal)

            # "Não me lembro" não é um canal de divulgação.
            if canal == "Não me lembro":
                continue

            if canal in CANAIS:
                grafo.add_edge(participante, canal)

    return grafo


def ajustar_rotulos_gexf(caminho):
    """
    Define os rótulos do arquivo GEXF.

    Participantes: rótulo vazio.
    Canais: nome do próprio canal.
    """

    arvore = ET.parse(caminho)
    raiz = arvore.getroot()

    for no in raiz.iter():

        if no.tag.endswith("node"):

            identificador = no.get("id", "")

            if identificador.startswith("P"):
                no.set("label", "")
            else:
                no.set("label", identificador)

    arvore.write(
        caminho,
        encoding="UTF-8",
        xml_declaration=True
    )


def validar_grafo(grafo):
    """Apresenta informações para validar a construção."""

    participantes = [
        no for no, dados in grafo.nodes(data=True)
        if dados["tipo"] == "participante"
    ]

    canais = [
        no for no, dados in grafo.nodes(data=True)
        if dados["tipo"] == "canal"
    ]

    componentes = list(nx.connected_components(grafo))

    participantes_isolados = [
        no for no in participantes
        if grafo.degree(no) == 0
    ]

    print("\n===== VALIDAÇÃO DO GRAFO =====")

    print(f"Participantes: {len(participantes)}")
    print(f"Canais: {len(canais)}")
    print(f"Total de vértices: {grafo.number_of_nodes()}")
    print(f"Total de arestas: {grafo.number_of_edges()}")

    print(f"Componentes conexas: {len(componentes)}")
    print(f"Participantes isolados: {len(participantes_isolados)}")

    maior_componente = max(componentes, key=len)

    print(
        f"Maior componente: {len(maior_componente)} vértices"
    )

    print("\nGrau dos canais:")

    for canal in canais:
        print(f"{canal}: {grafo.degree(canal)}")


if __name__ == "__main__":

    dados = carregar_dados()

    grafo = construir_grafo(dados)

    validar_grafo(grafo)

    # Exporta o grafo para GEXF
    nx.write_gexf(grafo, CAMINHO_GRAFO)

    # Ajusta os rótulos para a visualização no Gephi
    ajustar_rotulos_gexf(CAMINHO_GRAFO)

    print(f"\nGrafo salvo em {CAMINHO_GRAFO}")