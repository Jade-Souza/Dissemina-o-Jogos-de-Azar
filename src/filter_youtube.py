#!/usr/bin/env python3
"""Filtra e documenta os registros do YouTube relacionados a perdas/dependência.

Uso:
    python src/filter_youtube.py data/youtube_ibict_original.tsv

O arquivo original exportado pelo monitoramento deve ser TSV (tab separado).
O script NÃO apaga registros: seleciona o filtro de busca de perdas/dependência,
cria indicadores lexicais auditáveis e exporta todos os registros candidatos (ou a
quantidade encontrada na versão do arquivo utilizada).

Importante: indicadores lexicais não comprovam que o vídeo relata prejuízo
causado por apostas. A classificação é apenas uma triagem para revisão humana.
"""
from __future__ import annotations

import argparse
import re
import unicodedata
from pathlib import Path

import pandas as pd

# Identifica o filtro de busca específico de perdas/dependência do relatório.
# Não usamos número fixo de linhas: o critério é o texto do filtro original.
IDENTIFICADORES_FILTRO = (
    "apostei tudo",
    "perdi dinheiro",
    "tive prejuizos",
    "nao consigo parar de jogar",
    "dependencia de apostas",
)

TERMOS_APOSTAS = [
    r"\baposta(?:s)?\b", r"\bapost(?:a|as|ei|ou|ando)\b", r"\bbets?\b",
    r"\bcassino(?:s)?\b", r"\btigrinho\b", r"\bfortune\s*tiger\b",
    r"\baviator\b", r"\bslots?\b", r"\bjogo(?:s)?\s+de\s+azar\b",
    r"\bplataforma\s+de\s+aposta(?:s)?\b",
]
TERMOS_DANO = [
    r"\bperd(?:i|eu|emos|er|as?)\b", r"\bperdi\s+tudo\b",
    r"\bpreju[ií]zo(?:s)?\b", r"\bendivid\w*\b", r"\bd[ií]vida(?:s)?\b",
    r"\b[nãa]o\s+consigo\s+parar\b", r"\bv[ií]cio\b", r"\bdepend[eê]ncia\b",
    r"\b[nãa]o\s+consigo\s+pagar\b", r"\bperda(?:s)?\s+financeira(?:s)?\b",
]


def normalizar(valor: object) -> str:
    texto = "" if pd.isna(valor) else str(valor)
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", texto.lower()).strip()


def contem_algum(texto: str, padroes: list[str]) -> bool:
    return any(re.search(padrao, texto, flags=re.IGNORECASE) for padrao in padroes)


def localizar_coluna(df: pd.DataFrame, nome: str) -> str:
    mapa = {normalizar(c): c for c in df.columns}
    chave = normalizar(nome)
    if chave not in mapa:
        raise ValueError(f"Coluna obrigatória ausente: {nome!r}. Colunas encontradas: {list(df.columns)}")
    return mapa[chave]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("arquivo", type=Path, help="Exportação original do IBICT em TSV")
    parser.add_argument("--saida", type=Path, default=Path("outputs/youtube"), help="Pasta de saída")
    args = parser.parse_args()

    if not args.arquivo.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {args.arquivo}")

    # Algumas exportações do IBICT incluem uma linha de metadados antes do cabeçalho.
    # Localizamos o cabeçalho real pelo nome das colunas, sem presumir quantas linhas
    # de metadados existem (ou que sempre exista uma linha extra).
    colunas_esperadas = {
        normalizar("Filtro da busca"),
        normalizar("Título"),
        normalizar("Descrição"),
        normalizar("Descrição Pai"),
    }
    linha_cabecalho = None
    with args.arquivo.open("r", encoding="utf-8-sig", errors="replace") as arquivo:
        for indice, linha in enumerate(arquivo):
            colunas = {normalizar(c) for c in linha.rstrip("\\r\\n").split("\\t")}
            if colunas_esperadas.issubset(colunas):
                linha_cabecalho = indice
                break

    if linha_cabecalho is None:
        raise ValueError(
            "Não foi possível localizar o cabeçalho do TSV. Verifique se o arquivo "
            "está separado por tabulações e contém as colunas: Filtro da busca, "
            "Título, Descrição e Descrição Pai."
        )

    # dtype=str preserva IDs e links; skiprows descarta apenas as linhas anteriores
    # ao cabeçalho encontrado, inclusive a linha de metadados quando existir.
    df = pd.read_csv(
        args.arquivo,
        sep="\\t",
        skiprows=linha_cabecalho,
        dtype=str,
        keep_default_na=False,
        low_memory=False,
    )
    col_filtro = localizar_coluna(df, "Filtro da busca")
    col_titulo = localizar_coluna(df, "Título")
    col_descricao = localizar_coluna(df, "Descrição")
    col_descricao_pai = localizar_coluna(df, "Descrição Pai")

    filtros_norm = df[col_filtro].map(normalizar)
    mascara = filtros_norm.map(lambda f: all(normalizar(t) in f for t in IDENTIFICADORES_FILTRO))
    candidatos = df.loc[mascara].copy()

    # Analisa título + descrição + descrição pai; mantém cada campo original intacto.
    texto = (
        candidatos[col_titulo].map(normalizar) + " " +
        candidatos[col_descricao].map(normalizar) + " " +
        candidatos[col_descricao_pai].map(normalizar)
    )
    candidatos["indicador_termo_apostas"] = texto.map(lambda t: contem_algum(t, TERMOS_APOSTAS))
    candidatos["indicador_termo_dano"] = texto.map(lambda t: contem_algum(t, TERMOS_DANO))

    def classificar(linha: pd.Series) -> str:
        aposta = bool(linha["indicador_termo_apostas"])
        dano = bool(linha["indicador_termo_dano"])
        if aposta and dano:
            return "Evidência lexical de apostas e dano (revisão manual necessária)"
        if aposta:
            return "Termo de apostas encontrado, sem termo de dano no texto"
        if dano:
            return "Termo de dano encontrado, sem termo de apostas no texto"
        return "Sem evidência lexical nos campos analisados"

    candidatos["triagem_lexical"] = candidatos.apply(classificar, axis=1)
    candidatos["criterio_selecao"] = "Filtro da busca contém os termos identificadores do filtro de perdas/dependência"
    candidatos["observacao_metodologica"] = (
        "Triagem automática por título/descrição/descrição pai; não comprova o conteúdo audiovisual "
        "nem causalidade entre apostas e dano. Exige validação humana."
    )

    args.saida.mkdir(parents=True, exist_ok=True)
    caminho_csv = args.saida / "youtube_perdas_dependencia_triagem.csv"
    caminho_xlsx = args.saida / "youtube_perdas_dependencia_triagem.xlsx"
    caminho_resumo = args.saida / "youtube_perdas_dependencia_resumo.txt"
    candidatos.to_csv(caminho_csv, index=False, encoding="utf-8-sig")

    resumo = candidatos["triagem_lexical"].value_counts(dropna=False).to_dict()
    total_filtros = int(mascara.sum())
    total_links = candidatos[localizar_coluna(candidatos, "Link ocorrência")].nunique() if total_filtros else 0
    with pd.ExcelWriter(caminho_xlsx, engine="openpyxl") as writer:
        candidatos.to_excel(writer, sheet_name="Candidatos", index=False)
        pd.DataFrame([{"indicador": k, "quantidade": v} for k, v in resumo.items()]).to_excel(
            writer, sheet_name="Resumo", index=False
        )
        pd.DataFrame([
            {"etapa": "Registros no arquivo original", "quantidade": len(df)},
            {"etapa": "Registros selecionados pelo filtro de perdas/dependência", "quantidade": total_filtros},
            {"etapa": "Links de ocorrência distintos entre selecionados", "quantidade": total_links},
        ]).to_excel(writer, sheet_name="Rastreabilidade", index=False)

    linhas = [
        "RELATÓRIO DE FILTRAGEM DO YOUTUBE - IBICT",
        f"Arquivo de entrada: {args.arquivo}",
        f"Total de registros originais: {len(df)}",
        f"Registros selecionados pelo filtro de perdas/dependência: {total_filtros}",
        f"Links de ocorrência distintos: {total_links}",
        "",
        "Classificação lexical (não é validação do vídeo):",
    ]
    linhas += [f"- {k}: {v}" for k, v in resumo.items()]
    linhas += [
        "",
        "Critério: coluna 'Filtro da busca' contém os identificadores do filtro de perdas/dependência.",
        "Campos examinados: Título, Descrição e Descrição Pai.",
        "Os indicadores registram presença de termos; não comprovam relato, contexto ou causalidade.",
        "A revisão humana deve ser registrada separadamente antes de usar os casos como evidência.",
    ]
    caminho_resumo.write_text("\n".join(linhas), encoding="utf-8")

    print("\n".join(linhas))
    print("\nArquivos gerados:")
    print(caminho_csv)
    print(caminho_xlsx)
    print(caminho_resumo)


if __name__ == "__main__":
    main()
