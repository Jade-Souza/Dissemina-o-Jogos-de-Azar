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


## Análise estatística do LENAD III

As consequências e os indicadores relacionados a problemas com apostas do LENAD III são analisados por estatística descritiva e gráficos, sem forçar esses dados para uma estrutura de grafo ou árvore.

- `src/lenad_visualization.py`: gera cinco gráficos estatísticos a partir da planilha estruturada do LENAD III.
- `data/base_estruturada_LENAD_III.xlsx`: arquivo de entrada esperado pelo script (deve conter as abas `PGSI_Apostadores`, `Itens_PGSI`, `Estratos` e `Bets_vs_nao_Bets`).
- Os gráficos são salvos exclusivamente em PDF na pasta `outputs/`.

Para executar, coloque a planilha estruturada em `data/base_estruturada_LENAD_III.xlsx` e rode, na raiz do repositório:

```bash
python src/lenad_visualization.py
```

Também é possível indicar outros caminhos:

```bash
python src/lenad_visualization.py --entrada caminho/da/planilha.xlsx --saida outputs
```

### Gráficos gerados

1. Classificação PGSI entre apostadores no último ano (N=684).
2. Indicadores individuais do PGSI; o percentual positivo é a soma aritmética das categorias publicadas "às vezes" e "maioria/quase sempre".
3. Prevalência de risco ou jogo problemático por sexo e faixa etária.
4. Comparação entre usuários de plataformas Bets e apostadores de outras modalidades.
5. Prevalência por macrorregião, com intervalos de confiança.

### Cuidados na interpretação do LENAD III

- O PGSI é um instrumento de rastreamento/classificação, não um diagnóstico clínico.
- Os denominadores variam entre tabelas e devem ser apresentados junto aos resultados.
- Os itens PGSI podem se sobrepor: não se deve somar seus percentuais para estimar pessoas únicas.
- A soma das duas frequências positivas nos itens PGSI é um cálculo derivado das categorias publicadas, não uma estimativa independente.
- As associações observadas não demonstram causalidade.
- A estimativa regional do Norte possui intervalo de confiança amplo e deve ser interpretada com cautela.
- A análise utiliza resultados agregados publicados; não permite correlações individuais ou cruzamentos entre variáveis que não estejam disponíveis nos microdados.
