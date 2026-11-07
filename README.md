# Disseminação dos Jogos de Azar Online no Brasil

Projeto acadêmico que investiga a disseminação dos jogos de azar online no Brasil por meio da Teoria dos Grafos e da análise de dados.

## Objetivo

Analisar relações entre participantes e canais de exposição a jogos de azar online, aplicando estruturas e algoritmos de grafos. As análises são mantidas separadas quando representam fenômenos diferentes, para evitar misturar relações que não possuem o mesmo significado.

## Estrutura atual

- `main.py`: executa a análise principal da pesquisa.
- `src/graph_builder.py`: carrega a planilha da pesquisa e constrói o grafo bipartido.
- `src/bfs.py`: implementação da busca em largura (BFS).
- `src/dfs.py`: implementação da busca em profundidade (DFS).
- `src/metrics.py`: cálculo das métricas estruturais do grafo.
- `src/visualization.py`: geração dos gráficos estatísticos.
- `data/dados_originais.xlsx`: dados da pesquisa por questionário.
- `outputs/grafo_apostas.gexf`: grafo exportado para visualização no Gephi.

## Requisitos

Python 3.10 ou superior.

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executar a análise principal

Na raiz do repositório:

```bash
python main.py
```

A execução carrega os dados, constrói o grafo bipartido, executa BFS e DFS, calcula métricas e exporta o grafo em formato GEXF.

## Visualização no Gephi

A visualização e a organização espacial do grafo são realizadas no **Gephi**, não pelo código Python.

1. Execute `python main.py`.
2. Abra o Gephi.
3. Importe `outputs/grafo_apostas.gexf`.
4. Escolha o algoritmo de layout e configure cores, tamanhos e rótulos para a visualização final.

O arquivo GEXF contém a estrutura e os atributos do grafo. A disposição visual pode ser alterada no Gephi sem modificar os dados originais.

## Cuidados metodológicos

- A pesquisa por questionário utiliza uma amostra por conveniência. Seus resultados descrevem os participantes respondentes e não devem ser apresentados como estimativas representativas de toda a população brasileira.
- As arestas do grafo bipartido representam respostas de exposição informadas pelos participantes. Elas não comprovam, isoladamente, influência causal ou caminhos reais de disseminação.
- Resultados de bases externas, como registros de plataformas e canais públicos, devem ser analisados separadamente quando suas unidades de análise e significados de aresta forem diferentes.
- Quantidades e relações devem ser reportadas conforme os dados efetivamente disponíveis e os critérios de coleta documentados.

## Reprodutibilidade

Mantenha os arquivos de dados utilizados na análise em `data/` e registre a origem, o período de coleta, os filtros aplicados e as limitações de cada base. Arquivos brutos grandes ou dados que não possam ser redistribuídos não devem ser adicionados ao repositório sem verificar as condições de uso e publicação.
