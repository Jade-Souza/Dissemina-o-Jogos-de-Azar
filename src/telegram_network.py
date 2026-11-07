#!/usr/bin/env python3
"""Exporta a rede direcionada de recomendações documentadas para o Gephi.

Uso: python src/telegram_network.py
O script constrói e exporta o grafo em GEXF. A visualização é feita no Gephi.
"""
from pathlib import Path
import csv
import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
ENTRADA = ROOT / "data" / "relacoes_telegram_ibict.csv"
SAIDA = ROOT / "outputs" / "telegram" / "rede_recomendacoes_telegram.gexf"
CAMPOS = {"canal_origem", "canal_recomendado", "membros_origem",
          "membros_destino", "pagina_relatorio", "fonte"}


def carregar_relacoes():
    if not ENTRADA.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {ENTRADA}")
    with ENTRADA.open(encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        faltantes = CAMPOS - set(leitor.fieldnames or [])
        if faltantes:
            raise ValueError(f"Colunas ausentes no CSV: {sorted(faltantes)}")
        dados = list(leitor)
    if not dados:
        raise ValueError("O CSV não contém relações.")
    return dados


def construir_grafo(relacoes):
    grafo = nx.DiGraph()
    for relacao in relacoes:
        origem = relacao["canal_origem"].strip()
        destino = relacao["canal_recomendado"].strip()
        if not origem or not destino:
            raise ValueError("Existe uma relação com canal de origem/destino vazio.")
        grafo.add_node(origem, tipo="canal", membros=int(relacao["membros_origem"]))
        grafo.add_node(destino, tipo="canal", membros=int(relacao["membros_destino"]))
        grafo.add_edge(origem, destino,
                       tipo_relacao="recomendacao_documentada",
                       pagina_relatorio=relacao["pagina_relatorio"],
                       fonte=relacao["fonte"])
    return grafo


def main():
    grafo = construir_grafo(carregar_relacoes())
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    nx.write_gexf(grafo, SAIDA)
    print("===== REDE DE RECOMENDAÇÕES DOCUMENTADAS NO TELEGRAM =====")
    print(f"Relações: {grafo.number_of_edges()}")
    print(f"Canais distintos: {grafo.number_of_nodes()}")
    print(f"Componentes fracamente conexas: {nx.number_weakly_connected_components(grafo)}")
    print(f"GEXF exportado para abrir no Gephi: {SAIDA}")
    print("A rede contém apenas exemplos documentados nas páginas 26 e 28.")
    print("As arestas não comprovam migração, influência efetiva ou causalidade.")


if __name__ == "__main__":
    main()
