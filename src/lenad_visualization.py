"""
Geração dos gráficos estatísticos do LENAD III.

Entrada padrão:
    data/base_estruturada_LENAD_III.xlsx

Saídas:
    outputs/lenad_*.pdf

O módulo utiliza exclusivamente estatísticas agregadas publicadas no Caderno
Temático do LENAD III e transcritas para a planilha estruturada. Não estima
relações individuais, não calcula causalidade e não trata o PGSI como
diagnóstico clínico.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "base_estruturada_LENAD_III.xlsx"
DEFAULT_OUTPUT = ROOT / "outputs"


def carregar_dados(caminho: Path) -> dict[str, pd.DataFrame]:
    """Lê e valida as abas necessárias da planilha estruturada."""
    if not caminho.exists():
        raise FileNotFoundError(
            f"Planilha não encontrada: {caminho}\n"
            "Coloque base_estruturada_LENAD_III.xlsx na pasta data/ "
            "ou informe o caminho com --entrada."
        )

    xls = pd.ExcelFile(caminho)
    abas = {
        "PGSI_Apostadores",
        "Itens_PGSI",
        "Estratos",
        "Bets_vs_nao_Bets",
    }
    faltantes = abas.difference(xls.sheet_names)
    if faltantes:
        raise ValueError(
            "A planilha não contém as abas esperadas: "
            + ", ".join(sorted(faltantes))
        )

    return {nome: pd.read_excel(caminho, sheet_name=nome) for nome in abas}


def salvar_figura(figura: plt.Figure, pasta: Path, nome: str) -> None:
    """Salva cada gráfico exclusivamente em PDF."""
    pasta.mkdir(parents=True, exist_ok=True)
    figura.savefig(pasta / f"{nome}.pdf", format="pdf", bbox_inches="tight")
    plt.close(figura)


def grafico_classificacao_pgsi(dados: dict[str, pd.DataFrame], pasta: Path) -> None:
    """Distribuição das categorias PGSI entre apostadores no último ano."""
    df = dados["PGSI_Apostadores"].copy()
    df = df[~df["categoria"].str.contains("risco ou problemático", case=False)]
    df = df.sort_values("percentual_pct", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 5.8))
    ax.barh(df["categoria"], df["percentual_pct"])
    ax.errorbar(
        df["percentual_pct"],
        df["categoria"],
        xerr=[
            df["percentual_pct"] - df["ic95_inferior_pct"],
            df["ic95_superior_pct"] - df["percentual_pct"],
        ],
        fmt="none",
        ecolor="black",
        elinewidth=1.2,
        capsize=4,
        zorder=5,
    )
    for y, (valor, limite_superior) in enumerate(zip(df["percentual_pct"], df["ic95_superior_pct"])):
        ax.text(limite_superior + 1.0, y, f"{valor:.1f}%", va="center")
    ax.set(
        title="Classificação PGSI entre apostadores no último ano",
        xlabel="Participantes (%)",
        ylabel="Categoria PGSI",
        xlim=(0, max(df["ic95_superior_pct"]) + 12),
    )
    ax.text(
        0, -0.22, "Base: N=684 apostadores no último ano. IC95% conforme relatório.",
        transform=ax.transAxes, fontsize=9,
    )
    fig.tight_layout()
    salvar_figura(fig, pasta, "lenad_01_classificacao_pgsi")


def grafico_itens_pgsi(dados: dict[str, pd.DataFrame], pasta: Path) -> None:
    """Percentual que respondeu 'às vezes' ou 'maioria/quase sempre'."""
    df = dados["Itens_PGSI"].copy()
    # A soma é uma operação aritmética das duas categorias publicadas.
    # Não representa uma nova estimativa independente nem coocorrência.
    df["positivo_calculado"] = (
        df["as_vezes_pct"] + df["maioria_ou_quase_sempre_pct"]
    )
    df = df.sort_values("positivo_calculado", ascending=True)

    fig, ax = plt.subplots(figsize=(11, 8))
    ax.barh(df["indicador_pergunta"], df["positivo_calculado"])
    for y, valor in enumerate(df["positivo_calculado"]):
        ax.text(valor + 0.5, y, f"{valor:.1f}%", va="center")
    ax.set(
        title="Indicadores relacionados a problemas com apostas (PGSI)",
        xlabel="Respostas positivas — soma calculada (%)",
        ylabel="Indicador do questionário",
        xlim=(0, max(df["positivo_calculado"]) + 7),
    )
    ax.tick_params(axis="y", labelsize=8)
    ax.text(
        0, -0.17,
        "Base: N=684. Soma de 'às vezes' + 'maioria/quase sempre'; cálculo próprio a partir das categorias publicadas.",
        transform=ax.transAxes, fontsize=8,
    )
    fig.tight_layout()
    salvar_figura(fig, pasta, "lenad_02_indicadores_pgsi")


def grafico_sexo_idade(dados: dict[str, pd.DataFrame], pasta: Path) -> None:
    """Compara prevalências publicadas por sexo e faixa etária."""
    df = dados["Estratos"].copy()
    df = df[df["variavel_estratificacao"].isin(["Sexo", "Faixa etária"])].copy()
    df = df.sort_values(
        ["variavel_estratificacao", "percentual_risco_ou_problematico_pct"]
    )

    rotulos = [
        f"{linha.variavel_estratificacao}: {linha.grupo}"
        for linha in df.itertuples()
    ]
    valores = df["percentual_risco_ou_problematico_pct"].tolist()
    inferiores = df["ic95_inferior_pct"].tolist()
    superiores = df["ic95_superior_pct"].tolist()

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.barh(rotulos, valores)
    ax.errorbar(
        valores,
        rotulos,
        xerr=[
            [v - lo for v, lo in zip(valores, inferiores)],
            [hi - v for v, hi in zip(valores, superiores)],
        ],
        fmt="none",
        ecolor="black",
        elinewidth=1.2,
        capsize=4,
        zorder=5,
    )
    for y, (valor, limite_superior) in enumerate(zip(valores, superiores)):
        ax.text(limite_superior + 1.2, y, f"{valor:.1f}%", va="center")
    ax.set(
        title="Apostadores em risco ou jogo problemático, por sexo e idade",
        xlabel="Prevalência dentro de cada grupo (%)",
        ylabel="Grupo",
        xlim=(0, max(superiores) + 15),
    )
    ax.text(
        0, -0.20,
        "Base total: N=684 apostadores recentes. O relatório não informa o n específico de cada subgrupo; IC95% publicados.",
        transform=ax.transAxes, fontsize=8,
    )
    fig.tight_layout()
    salvar_figura(fig, pasta, "lenad_03_risco_sexo_idade")


def grafico_bets(dados: dict[str, pd.DataFrame], pasta: Path) -> None:
    """Prevalência de risco entre usuários e não usuários de Bets."""
    df = dados["Bets_vs_nao_Bets"].copy()
    df = df.sort_values("percentual_risco_ou_problematico_pct", ascending=True)

    valores = df["percentual_risco_ou_problematico_pct"].tolist()
    inferiores = df["ic95_inferior_pct"].tolist()
    superiores = df["ic95_superior_pct"].tolist()
    rotulos = df["grupo"].tolist()

    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.barh(rotulos, valores)
    ax.errorbar(
        valores,
        rotulos,
        xerr=[
            [v - lo for v, lo in zip(valores, inferiores)],
            [hi - v for v, hi in zip(valores, superiores)],
        ],
        fmt="none",
        ecolor="black",
        elinewidth=1.2,
        capsize=4,
        zorder=5,
    )
    for y, (valor, limite_superior) in enumerate(zip(valores, superiores)):
        ax.text(limite_superior + 1.2, y, f"{valor:.1f}%", va="center")
    ax.set(
        title="Risco ou jogo problemático segundo uso de plataformas Bets",
        xlabel="Prevalência dentro de cada grupo (%)",
        ylabel="Grupo",
        xlim=(0, max(superiores) + 15),
    )
    ax.text(
        0, -0.22,
        "Base total: N=684 apostadores recentes. n por grupo não discriminado no relatório; associação p<0,05, sem inferência causal. IC95% publicados.",
        transform=ax.transAxes, fontsize=8,
    )
    fig.tight_layout()
    salvar_figura(fig, pasta, "lenad_04_risco_uso_bets")


def grafico_regioes(dados: dict[str, pd.DataFrame], pasta: Path) -> None:
    """Prevalência por macrorregião, com intervalos de confiança."""
    df = dados["Estratos"].copy()
    df = df[df["variavel_estratificacao"] == "Macrorregião"].copy()
    df = df.sort_values("percentual_risco_ou_problematico_pct", ascending=True)

    valores = df["percentual_risco_ou_problematico_pct"].tolist()
    inferiores = df["ic95_inferior_pct"].tolist()
    superiores = df["ic95_superior_pct"].tolist()
    rotulos = df["grupo"].tolist()

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.barh(rotulos, valores)
    ax.errorbar(
        valores,
        rotulos,
        xerr=[
            [v - lo for v, lo in zip(valores, inferiores)],
            [hi - v for v, hi in zip(valores, superiores)],
        ],
        fmt="none",
        ecolor="black",
        elinewidth=1.2,
        capsize=4,
        zorder=5,
    )
    for y, (valor, limite_superior) in enumerate(zip(valores, superiores)):
        ax.text(limite_superior + 1.2, y, f"{valor:.1f}%", va="center")
    ax.set(
        title="Risco ou jogo problemático por macrorregião",
        xlabel="Prevalência dentro de cada grupo (%)",
        ylabel="Macrorregião",
        xlim=(0, max(superiores) + 15),
    )
    ax.text(
        0, -0.20,
        "Base total: N=684 apostadores recentes. n por região não discriminado no relatório. IC95% do Norte amplo; interpretar com cautela.",
        transform=ax.transAxes, fontsize=8,
    )
    fig.tight_layout()
    salvar_figura(fig, pasta, "lenad_05_risco_regiao")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera cinco gráficos estatísticos a partir da planilha estruturada do LENAD III."
    )
    parser.add_argument(
        "--entrada",
        type=Path,
        default=DEFAULT_INPUT,
        help="Caminho da planilha XLSX estruturada.",
    )
    parser.add_argument(
        "--saida",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Pasta onde os gráficos serão salvos.",
    )
    args = parser.parse_args()

    dados = carregar_dados(args.entrada)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})

    grafico_classificacao_pgsi(dados, args.saida)
    grafico_itens_pgsi(dados, args.saida)
    grafico_sexo_idade(dados, args.saida)
    grafico_bets(dados, args.saida)
    grafico_regioes(dados, args.saida)

    print(f"Cinco gráficos gerados em: {args.saida.resolve()}")
    print("Formato: somente PDF.")


if __name__ == "__main__":
    main()
