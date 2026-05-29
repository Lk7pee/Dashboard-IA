from io import StringIO
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd
from flask import Flask, render_template
from plotly.offline import get_plotlyjs


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
STATIC_JS_DIR = BASE_DIR / "static" / "js"
STATIC_INDEX_PATH = BASE_DIR / "index.html"

URL_INVESTIMENTOS_IA = (
    "https://ourworldindata.org/grapher/"
    "private-investment-in-artificial-intelligence.csv"
    "?v=1&csvType=full&useColumnShortNames=false"
)

# O endpoint acima e a fonte por pais abaixo sao publicos da Our World in Data.
# O segundo e usado quando a serie principal nao traz todos os paises pedidos.
URL_INVESTIMENTOS_IA_PAISES = (
    "https://ourworldindata.org/grapher/"
    "private-investment-in-artificial-intelligence-cset.csv"
    "?v=1&csvType=full&useColumnShortNames=false"
)

MAPA_PAISES = {
    "World": "Global",
    "Global": "Global",
    "United States": "EUA",
    "United States of America": "EUA",
    "USA": "EUA",
    "US": "EUA",
    "China": "China",
    "United Kingdom": "Reino Unido",
    "UK": "Reino Unido",
    "Brazil": "Brasil",
}

ORDEM_PAISES_INVESTIMENTO = ["Global", "EUA", "China", "Reino Unido", "Brasil"]
CAMINHO_INVESTIMENTOS = DATA_DIR / "investimentos_ia.csv"

app = Flask(__name__)


SETORES_EXEMPLO = [
    {"setor": "Saúde", "percentual_adocao": 48},
    {"setor": "Finanças", "percentual_adocao": 67},
    {"setor": "Marketing", "percentual_adocao": 74},
    {"setor": "Tecnologia da Informação", "percentual_adocao": 82},
    {"setor": "Educação", "percentual_adocao": 39},
    {"setor": "Varejo", "percentual_adocao": 56},
    {"setor": "Jurídico", "percentual_adocao": 34},
    {"setor": "Indústria", "percentual_adocao": 51},
    {"setor": "Atendimento ao Cliente", "percentual_adocao": 69},
    {"setor": "Recursos Humanos", "percentual_adocao": 45},
]

TRAFEGO_EXEMPLO = [
    {"ano": 2021, "ferramenta": "ChatGPT", "usuarios_milhoes": 0},
    {"ano": 2021, "ferramenta": "Midjourney", "usuarios_milhoes": 1},
    {"ano": 2021, "ferramenta": "Claude", "usuarios_milhoes": 0},
    {"ano": 2021, "ferramenta": "Gemini", "usuarios_milhoes": 0},
    {"ano": 2021, "ferramenta": "Copilot", "usuarios_milhoes": 2},
    {"ano": 2022, "ferramenta": "ChatGPT", "usuarios_milhoes": 20},
    {"ano": 2022, "ferramenta": "Midjourney", "usuarios_milhoes": 5},
    {"ano": 2022, "ferramenta": "Claude", "usuarios_milhoes": 1},
    {"ano": 2022, "ferramenta": "Gemini", "usuarios_milhoes": 0},
    {"ano": 2022, "ferramenta": "Copilot", "usuarios_milhoes": 8},
    {"ano": 2023, "ferramenta": "ChatGPT", "usuarios_milhoes": 180},
    {"ano": 2023, "ferramenta": "Midjourney", "usuarios_milhoes": 18},
    {"ano": 2023, "ferramenta": "Claude", "usuarios_milhoes": 12},
    {"ano": 2023, "ferramenta": "Gemini", "usuarios_milhoes": 30},
    {"ano": 2023, "ferramenta": "Copilot", "usuarios_milhoes": 35},
    {"ano": 2024, "ferramenta": "ChatGPT", "usuarios_milhoes": 250},
    {"ano": 2024, "ferramenta": "Midjourney", "usuarios_milhoes": 25},
    {"ano": 2024, "ferramenta": "Claude", "usuarios_milhoes": 35},
    {"ano": 2024, "ferramenta": "Gemini", "usuarios_milhoes": 80},
    {"ano": 2024, "ferramenta": "Copilot", "usuarios_milhoes": 75},
    {"ano": 2025, "ferramenta": "ChatGPT", "usuarios_milhoes": 320},
    {"ano": 2025, "ferramenta": "Midjourney", "usuarios_milhoes": 32},
    {"ano": 2025, "ferramenta": "Claude", "usuarios_milhoes": 60},
    {"ano": 2025, "ferramenta": "Gemini", "usuarios_milhoes": 130},
    {"ano": 2025, "ferramenta": "Copilot", "usuarios_milhoes": 110},
]


DATASETS_EXEMPLO = {
    "setores_adocao_ia.csv": {
        "rows": SETORES_EXEMPLO,
        "columns": ["setor", "percentual_adocao"],
    },
    "trafego_ferramentas_ia.csv": {
        "rows": TRAFEGO_EXEMPLO,
        "columns": ["ano", "ferramenta", "usuarios_milhoes"],
    },
}


def salvar_csv_exemplo(nome_arquivo):
    """Cria CSVs de exemplo apenas para dados que continuam simulados."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    info = DATASETS_EXEMPLO[nome_arquivo]
    caminho = DATA_DIR / nome_arquivo
    pd.DataFrame(info["rows"], columns=info["columns"]).to_csv(
        caminho, index=False, encoding="utf-8"
    )
    return caminho


def garantir_csvs_exemplo():
    """Garante os CSVs simulados de setores e ferramentas, sem simular investimento."""
    for nome_arquivo in DATASETS_EXEMPLO:
        caminho = DATA_DIR / nome_arquivo
        if not caminho.exists():
            salvar_csv_exemplo(nome_arquivo)


def garantir_plotly_local():
    """Salva o Plotly em arquivo local para nao depender de CDN ou internet."""
    STATIC_JS_DIR.mkdir(parents=True, exist_ok=True)
    caminho_plotly = STATIC_JS_DIR / "plotly.min.js"
    if not caminho_plotly.exists():
        caminho_plotly.write_text(get_plotlyjs(), encoding="utf-8")


def carregar_csv_exemplo(nome_arquivo):
    """Le um CSV local de exemplo e recria o arquivo se ele estiver invalido."""
    info = DATASETS_EXEMPLO[nome_arquivo]
    caminho = DATA_DIR / nome_arquivo

    try:
        df = pd.read_csv(caminho, encoding="utf-8")
    except (FileNotFoundError, pd.errors.EmptyDataError, UnicodeDecodeError):
        caminho = salvar_csv_exemplo(nome_arquivo)
        df = pd.read_csv(caminho, encoding="utf-8")

    colunas_obrigatorias = set(info["columns"])
    if not colunas_obrigatorias.issubset(df.columns):
        caminho = salvar_csv_exemplo(nome_arquivo)
        df = pd.read_csv(caminho, encoding="utf-8")

    return df


def ler_csv_remoto_owid(url):
    """Baixa um CSV da Our World in Data com cabecalho simples de navegador."""
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 dashboard-academico-ia",
            "Accept": "text/csv,*/*;q=0.9",
        },
    )
    with urlopen(request, timeout=30) as resposta:
        conteudo = resposta.read().decode("utf-8")
    return pd.read_csv(StringIO(conteudo))


def identificar_coluna(df, nomes_possiveis):
    """Procura uma coluna por nomes comuns, ignorando diferencas de maiusculas."""
    mapa_colunas = {col.strip().lower(): col for col in df.columns}
    for nome in nomes_possiveis:
        coluna = mapa_colunas.get(nome.lower())
        if coluna:
            return coluna
    raise ValueError(f"Nao foi encontrada nenhuma coluna entre: {nomes_possiveis}")


def identificar_coluna_valor(df, coluna_pais, coluna_ano):
    """Identifica automaticamente a primeira coluna numerica de valor."""
    colunas_ignoradas = {coluna_pais, coluna_ano, "Code"}
    candidatas = [col for col in df.columns if col not in colunas_ignoradas]

    for coluna in candidatas:
        valores = pd.to_numeric(df[coluna], errors="coerce")
        if valores.notna().any():
            return coluna

    raise ValueError("Nao foi encontrada uma coluna numerica de valor no CSV.")


def tratar_investimentos_owid(df):
    """Filtra, renomeia e converte o dataset de investimentos para o formato local."""
    df = df.copy()
    df.columns = [col.strip() for col in df.columns]

    coluna_pais = identificar_coluna(df, ["Entity", "Country", "pais", "país"])
    coluna_ano = identificar_coluna(df, ["Year", "ano"])
    coluna_valor = identificar_coluna_valor(df, coluna_pais, coluna_ano)

    df = df[df[coluna_pais].isin(MAPA_PAISES.keys())].copy()
    df["pais"] = df[coluna_pais].map(MAPA_PAISES)
    df["ano"] = pd.to_numeric(df[coluna_ano], errors="coerce")
    df[coluna_valor] = pd.to_numeric(df[coluna_valor], errors="coerce")

    # A OWID publica os valores em dolares; o dashboard exibe em bilhoes.
    df["investimento_bilhoes"] = (df[coluna_valor] / 1_000_000_000).round(2)
    df_final = df[["ano", "pais", "investimento_bilhoes"]].dropna(
        subset=["ano", "pais", "investimento_bilhoes"]
    )
    df_final["ano"] = df_final["ano"].astype(int)
    df_final = df_final[df_final["pais"].isin(ORDEM_PAISES_INVESTIMENTO)]

    df_final["pais"] = pd.Categorical(
        df_final["pais"], categories=ORDEM_PAISES_INVESTIMENTO, ordered=True
    )
    df_final = df_final.sort_values(["ano", "pais"]).reset_index(drop=True)
    df_final["pais"] = df_final["pais"].astype(str)

    return df_final


def baixar_e_atualizar_investimentos_ia():
    """Baixa dados reais de investimento em IA e atualiza data/investimentos_ia.csv."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    erros = []

    for url in [URL_INVESTIMENTOS_IA, URL_INVESTIMENTOS_IA_PAISES]:
        try:
            df_bruto = ler_csv_remoto_owid(url)
            df_final = tratar_investimentos_owid(df_bruto)
            paises_encontrados = set(df_final["pais"].dropna().unique())

            if set(ORDEM_PAISES_INVESTIMENTO).issubset(paises_encontrados):
                df_final.to_csv(CAMINHO_INVESTIMENTOS, index=False, encoding="utf-8")
                return df_final

            faltantes = sorted(set(ORDEM_PAISES_INVESTIMENTO) - paises_encontrados)
            erros.append(f"A fonte {url} nao trouxe estes paises: {', '.join(faltantes)}")
        except Exception as erro:
            erros.append(f"{url}: {erro}")

    print("Erro ao baixar os dados reais de investimento em IA:", " | ".join(erros))

    if CAMINHO_INVESTIMENTOS.exists():
        print("Usando arquivo local existente:", CAMINHO_INVESTIMENTOS)
        return pd.read_csv(CAMINHO_INVESTIMENTOS, encoding="utf-8")

    raise Exception(
        "Nao foi possivel baixar os dados reais e o arquivo local "
        "data/investimentos_ia.csv nao existe."
    )


def limpar_investimentos(df):
    """Normaliza o CSV de investimento antes dos calculos do dashboard."""
    df = df.copy()
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce")
    df["investimento_bilhoes"] = pd.to_numeric(
        df["investimento_bilhoes"], errors="coerce"
    )
    df = df.dropna(subset=["ano", "pais", "investimento_bilhoes"])
    df["ano"] = df["ano"].astype(int)
    df["pais"] = df["pais"].replace(MAPA_PAISES)
    df = df[df["pais"].isin(ORDEM_PAISES_INVESTIMENTO)]
    return df.sort_values(["ano", "pais"]).reset_index(drop=True)


def formatar_bilhoes(valor):
    """Formata valores monetarios dos cards."""
    return f"US$ {valor:.2f} bi"


def ultimo_registro_pais(investimentos, pais):
    """Retorna a linha mais recente de um pais ou None quando nao ha dados."""
    dados_pais = investimentos[investimentos["pais"] == pais].sort_values("ano")
    if dados_pais.empty:
        return None
    return dados_pais.iloc[-1]


def montar_cards_investimento(investimentos, erro_investimentos=None):
    """Cria os cards de investimento exigidos para o topo do dashboard."""
    if investimentos.empty:
        mensagem = erro_investimentos or "Sem dados reais de investimento disponíveis."
        return [
            {
                "label": "Investimento em IA",
                "value": "Indisponível",
                "detail": mensagem,
            }
        ]

    global_recente = ultimo_registro_pais(investimentos, "Global")
    ano_referencia = (
        int(global_recente["ano"]) if global_recente is not None else int(investimentos["ano"].max())
    )

    paises_no_ano = investimentos[
        (investimentos["ano"] == ano_referencia) & (investimentos["pais"] != "Global")
    ]
    if paises_no_ano.empty:
        lider = None
    else:
        lider = paises_no_ano.loc[paises_no_ano["investimento_bilhoes"].idxmax()]

    cards = []
    if global_recente is not None:
        cards.append(
            {
                "label": "Investimento global mais recente",
                "value": formatar_bilhoes(global_recente["investimento_bilhoes"]),
                "detail": f"Global em {int(global_recente['ano'])}",
            }
        )
    else:
        cards.append(
            {
                "label": "Investimento global mais recente",
                "value": "Sem dados",
                "detail": "A fonte nao trouxe valor global.",
            }
        )

    if lider is not None:
        cards.append(
            {
                "label": "País com maior investimento",
                "value": lider["pais"],
                "detail": f"{formatar_bilhoes(lider['investimento_bilhoes'])} em {ano_referencia}",
            }
        )
    else:
        cards.append(
            {
                "label": "País com maior investimento",
                "value": "Sem dados",
                "detail": f"Nenhum país com valor em {ano_referencia}.",
            }
        )

    for pais in ["EUA", "China", "Reino Unido", "Brasil"]:
        registro = ultimo_registro_pais(investimentos, pais)
        if registro is None:
            cards.append(
                {
                    "label": pais,
                    "value": "Sem dados",
                    "detail": f"{pais}: sem dados disponíveis na fonte",
                }
            )
            continue

        ano = int(registro["ano"])
        detalhe = f"{pais} em {ano}"
        if pais == "Brasil" and ano != ano_referencia:
            detalhe = f"Brasil em {ano}; fonte sem valor para {ano_referencia}"

        cards.append(
            {
                "label": f"Investimento mais recente - {pais}",
                "value": formatar_bilhoes(registro["investimento_bilhoes"]),
                "detail": detalhe,
            }
        )

    return cards


def obter_linha_mais_recente(df, coluna_grupo, grupo):
    """Retorna a linha mais recente de um grupo em qualquer dataset."""
    dados_grupo = df[df[coluna_grupo] == grupo].sort_values("ano")
    if dados_grupo.empty:
        return None
    return dados_grupo.iloc[-1]


def montar_cards_bsc(investimentos, setores, trafego, erro_investimentos=None):
    """Monta os cards no formato de Balanced Scorecard para a tela principal."""
    if investimentos.empty:
        return [
            {
                "perspective": "Financeira",
                "objective": "Monitorar capital privado em IA",
                "kpi": "Investimento privado global",
                "value": "Indisponível",
                "goal": "Fonte real não carregada",
                "trend": erro_investimentos or "Sem dados reais disponíveis",
                "accent": "green",
            }
        ]

    global_recente = ultimo_registro_pais(investimentos, "Global")
    global_anterior = (
        investimentos[investimentos["pais"] == "Global"].sort_values("ano").iloc[-2]
        if len(investimentos[investimentos["pais"] == "Global"]) > 1
        else None
    )
    crescimento_global = 0
    if global_recente is not None and global_anterior is not None:
        crescimento_global = (
            (global_recente["investimento_bilhoes"] - global_anterior["investimento_bilhoes"])
            / global_anterior["investimento_bilhoes"]
            * 100
        )

    setor_lider = setores.loc[setores["percentual_adocao"].idxmax()]
    ferramenta_final = (
        trafego.sort_values("ano")
        .groupby("ferramenta")["usuarios_milhoes"]
        .last()
        .sort_values(ascending=False)
    )
    ferramenta_lider = ferramenta_final.index[0]
    usuarios_lider = ferramenta_final.iloc[0]

    eua_recente = ultimo_registro_pais(investimentos, "EUA")
    concentracao_eua = 0
    if global_recente is not None and eua_recente is not None and global_recente["investimento_bilhoes"]:
        concentracao_eua = (
            eua_recente["investimento_bilhoes"] / global_recente["investimento_bilhoes"] * 100
        )

    return [
        {
            "perspective": "Financeira",
            "objective": "Monitorar o capital privado global em IA",
            "kpi": "Investimento privado global",
            "value": formatar_bilhoes(global_recente["investimento_bilhoes"]),
            "goal": f"Ano-base: {int(global_recente['ano'])}",
            "trend": f"Variação anual: {crescimento_global:.1f}%",
            "accent": "green",
        },
        {
            "perspective": "Mercado",
            "objective": "Identificar os setores que adotam IA mais rápido",
            "kpi": f"Setor líder: {setor_lider['setor']}",
            "value": f"{setor_lider['percentual_adocao']:.0f}%",
            "goal": "Referência: setores do CSV local",
            "trend": "Adoção empresarial em expansão",
            "accent": "blue",
        },
        {
            "perspective": "Processos",
            "objective": "Avaliar concentração internacional dos investimentos",
            "kpi": "Participação dos EUA no total global",
            "value": f"{concentracao_eua:.1f}%",
            "goal": f"Base: Global x EUA em {int(global_recente['ano'])}",
            "trend": "Capital concentrado em poucos mercados",
            "accent": "purple",
        },
        {
            "perspective": "Aprendizado",
            "objective": "Acompanhar escala de uso das ferramentas de IA",
            "kpi": f"Ferramenta líder: {ferramenta_lider}",
            "value": f"{usuarios_lider:.0f} mi",
            "goal": "Usuários em milhões",
            "trend": "Uso crescente em trabalho e estudo",
            "accent": "teal",
        },
    ]


def montar_indicadores_operacionais(investimentos):
    """Compara o ultimo valor real com a media historica de cada pais."""
    indicadores = []
    for pais in ORDEM_PAISES_INVESTIMENTO:
        grupo = investimentos[investimentos["pais"] == pais].sort_values("ano")
        if grupo.empty:
            continue

        ultimo = grupo.iloc[-1]
        indicadores.append(
            {
                "pais": pais,
                "ano": int(ultimo["ano"]),
                "realizado": round(float(ultimo["investimento_bilhoes"]), 2),
                "media_historica": round(float(grupo["investimento_bilhoes"].mean()), 2),
            }
        )
    return indicadores


def montar_resumo_bsc(cards_bsc):
    """Cria linhas da tabela de resumo estrategico exibida abaixo dos graficos."""
    return [
        {
            "perspective": card["perspective"],
            "objective": card["objective"],
            "kpi": card["kpi"],
            "target": card["goal"],
            "result": card["value"],
        }
        for card in cards_bsc
    ]


def preparar_dados():
    """Carrega, limpa e organiza os dados usados pelo HTML e JavaScript."""
    garantir_csvs_exemplo()

    erro_investimentos = None
    try:
        investimentos = baixar_e_atualizar_investimentos_ia()
        investimentos = limpar_investimentos(investimentos)
    except Exception as erro:
        erro_investimentos = str(erro)
        investimentos = pd.DataFrame(
            columns=["ano", "pais", "investimento_bilhoes"]
        )

    setores = carregar_csv_exemplo("setores_adocao_ia.csv")
    trafego = carregar_csv_exemplo("trafego_ferramentas_ia.csv")

    setores["percentual_adocao"] = pd.to_numeric(
        setores["percentual_adocao"], errors="coerce"
    )
    setores = setores.dropna(subset=["setor", "percentual_adocao"])

    trafego["ano"] = pd.to_numeric(trafego["ano"], errors="coerce")
    trafego["usuarios_milhoes"] = pd.to_numeric(
        trafego["usuarios_milhoes"], errors="coerce"
    )
    trafego = trafego.dropna(subset=["ano", "ferramenta", "usuarios_milhoes"])
    trafego["ano"] = trafego["ano"].astype(int)

    cards = montar_cards_bsc(investimentos, setores, trafego, erro_investimentos)
    resumo_bsc = montar_resumo_bsc(cards)
    indicadores_operacionais = montar_indicadores_operacionais(investimentos)
    media_adocao = float(setores["percentual_adocao"].mean()) if not setores.empty else 0

    investimento_paises = {}
    for pais in ORDEM_PAISES_INVESTIMENTO:
        grupo = investimentos[investimentos["pais"] == pais].sort_values("ano")
        if grupo.empty:
            continue
        investimento_paises[pais] = {
            "anos": grupo["ano"].astype(int).tolist(),
            "valores": grupo["investimento_bilhoes"].round(2).tolist(),
        }

    setores_ordenados = setores.sort_values("percentual_adocao", ascending=True)

    trafego_series = {}
    for ferramenta, grupo in trafego.groupby("ferramenta"):
        grupo = grupo.sort_values("ano")
        trafego_series[ferramenta] = {
            "anos": grupo["ano"].astype(int).tolist(),
            "valores": grupo["usuarios_milhoes"].round(2).tolist(),
        }

    dados_dashboard = {
        "investimentos": {
            "paises": investimento_paises,
            "ordem": [pais for pais in ORDEM_PAISES_INVESTIMENTO if pais in investimento_paises],
            "erro": erro_investimentos,
            "indicadores": indicadores_operacionais,
        },
        "setores": {
            "nomes": setores_ordenados["setor"].tolist(),
            "percentuais": setores_ordenados["percentual_adocao"].round(2).tolist(),
            "media": round(media_adocao, 2),
        },
        "trafego": trafego_series,
        "bsc": resumo_bsc,
    }

    return cards, dados_dashboard


def gerar_index_estatico(cards=None, dados_dashboard=None):
    """Gera index.html estatico para GitHub Pages ou abertura direta por clique."""
    garantir_plotly_local()
    if cards is None or dados_dashboard is None:
        cards, dados_dashboard = preparar_dados()

    with app.app_context():
        html = render_template(
            "index.html",
            cards=cards,
            dashboard_data=dados_dashboard,
            static_mode=True,
        )

    STATIC_INDEX_PATH.write_text(html, encoding="utf-8")
    return STATIC_INDEX_PATH


@app.route("/")
def index():
    """Rota principal do dashboard Flask."""
    garantir_plotly_local()
    cards, dados_dashboard = preparar_dados()
    gerar_index_estatico(cards, dados_dashboard)
    return render_template(
        "index.html",
        cards=cards,
        dashboard_data=dados_dashboard,
        static_mode=False,
    )


if __name__ == "__main__":
    garantir_csvs_exemplo()
    garantir_plotly_local()
    gerar_index_estatico()
    app.run(debug=True, host="127.0.0.1", port=5000)
