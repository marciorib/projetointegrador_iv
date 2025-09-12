import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
import warnings
from datetime import datetime
import matplotlib.colors as mcolors
import random

# -------------------------------
# Configuração da página
# -------------------------------
st.set_page_config(page_title="Dashboard SPTrans", layout="wide")
warnings.filterwarnings("ignore")

# -------------------------------
# CSS customizado
# -------------------------------
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; font-family: "Segoe UI", sans-serif; }
    h1, h2, h3 { color: #61dafb; font-weight: 600; }
    [data-testid="stMetricValue"] { font-size: 28px; color: #21c4ff; }
    [data-testid="stMetricDelta"] { color: #f0f0f0 !important; }
    section[data-testid="stSidebar"] { background-color: #161a23; }
    .ag-theme-balham { border-radius: 12px; overflow: hidden; }
    button[kind="primary"] { background-color: #21c4ff !important; color: black !important; border-radius: 8px !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# Função para carregar dados (robusta para diferentes nomes de colunas)
# -------------------------------
@st.cache_data
def load_data(caminho_csv, n_amostra=10000):
    df = pd.read_csv(caminho_csv)

    # Detectar automaticamente a coluna de hora
    possiveis_colunas_hora = ["hora_coleta", "hora", "horario", "data_hora", "dataHora"]
    col_hora = None
    for c in possiveis_colunas_hora:
        if c in df.columns:
            col_hora = c
            break

    if col_hora:
        df["hora_coleta"] = pd.to_datetime(df[col_hora], errors="coerce")
    else:
        df["hora_coleta"] = pd.NaT  # cria a coluna vazia se não encontrar

    # Garantir colunas mínimas
    for col in ["codigo_linha", "prefixo", "latitude", "longitude"]:
        if col not in df.columns:
            df[col] = pd.NA

    # Amostragem se dataset grande
    if len(df) > n_amostra:
        df = df.sample(n=n_amostra, random_state=42)

    return df

df = load_data("onibus_todos.csv")

# -------------------------------
# Exibir preview dos dados
# -------------------------------
st.subheader("Pré-visualização dos dados carregados")
st.write(df.head())  # 🔎 mostra primeiras linhas da base

# -------------------------------
# Sidebar - Filtros
# -------------------------------
st.sidebar.header("🛠️ Filtros")
linhas = st.sidebar.multiselect(
    "Escolha a(s) linha(s):",
    options=df["codigo_linha"].dropna().unique(),
    default=df["codigo_linha"].dropna().unique()
)

df_filtrado = df[df["codigo_linha"].isin(linhas)] if linhas else df.copy()

# Filtro: Prefixo
prefixos = st.sidebar.multiselect(
    "Escolha o(s) ônibus (prefixo):",
    options=df_filtrado["prefixo"].dropna().unique(),
    default=[]
)
if prefixos:
    df_filtrado = df_filtrado[df_filtrado["prefixo"].isin(prefixos)]

# Checkbox: mostrar trajetos
mostrar_trajeto = st.sidebar.checkbox("Mostrar trajeto da(s) linha(s) selecionada(s)", value=False)

# Slider temporal: hora do dia
if pd.api.types.is_datetime64_any_dtype(df["hora_coleta"]):
    horas_disponiveis = df["hora_coleta"].dt.hour.dropna().unique()
    hora_selecionada = st.sidebar.slider(
        "Selecione a hora do dia:",
        min_value=int(horas_disponiveis.min()),
        max_value=int(horas_disponiveis.max()),
        value=int(horas_disponiveis.min())
    )
    df_filtrado = df_filtrado[df_filtrado["hora_coleta"].dt.hour == hora_selecionada]

# -------------------------------
# Função segura para exibir datas
# -------------------------------
def formatar_data_segura(data):
    if pd.isna(data):
        return "N/A"
    if isinstance(data, (pd.Timestamp, datetime)):
        return data.strftime("%d/%m/%Y %H:%M:%S")
    return str(data)

# -------------------------------
# Função para converter hex em RGBA
# -------------------------------
def hex_to_rgba(hex_color, alpha=180):
    hex_color = hex_color.lstrip("#")
    return [int(hex_color[0:2],16), int(hex_color[2:4],16), int(hex_color[4:6],16), alpha]

# -------------------------------
# Layout - Título e Cards
# -------------------------------
st.title("📊 Dashboard SPTrans - Ônibus em Tempo Real")
col1, col2, col3 = st.columns(3)
col1.metric("🚌 Total de ônibus ativos", len(df_filtrado["prefixo"].dropna().unique()))
col2.metric("📋 Linhas selecionadas", len(linhas))
col3.metric("⏱️ Última coleta", formatar_data_segura(df_filtrado["hora_coleta"].max()))

# -------------------------------
# Mapa com tooltip, trajetos e destaque de ônibus
# -------------------------------
st.subheader("🗺️ Localização e Trajetos dos Ônibus")
if not df_filtrado.empty and df_filtrado[["latitude", "longitude"]].notna().all(axis=None):
    # Cores por linha
    linhas_unicas = df_filtrado["codigo_linha"].dropna().unique()
    cores = random.choices(list(mcolors.CSS4_COLORS.values()), k=len(linhas_unicas))
    cor_map = dict(zip(linhas_unicas, cores))
    df_filtrado["cor"] = df_filtrado["codigo_linha"].map(cor_map).fillna("#21c4ff")
    df_filtrado["rgba"] = df_filtrado["cor"].apply(lambda x: hex_to_rgba(x))

    # Se prefixos foram selecionados → destaque
    if prefixos:
        df_filtrado["tamanho"] = df_filtrado["prefixo"].apply(lambda x: 150 if x in prefixos else 70)
        df_filtrado["rgba"] = df_filtrado.apply(
            lambda row: [255, 255, 0, 220] if row["prefixo"] in prefixos else row["rgba"], axis=1
        )
    else:
        df_filtrado["tamanho"] = 70

    # Camada ScatterplotLayer (ônibus)
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_filtrado,
        get_position=["longitude", "latitude"],
        get_color="rgba",
        get_radius="tamanho",
        pickable=True
    )

    layers = [scatter_layer]

    # Se checkbox estiver marcado, mostrar trajetos
    if mostrar_trajeto:
        trajetos = []
        for linha in linhas:
            df_linha = df[df["codigo_linha"] == linha].sort_values("hora_coleta")
            for prefixo, grupo in df_linha.groupby("prefixo"):
                coords = grupo[["longitude", "latitude"]].dropna().values.tolist()
                if len(coords) > 1:
                    trajetos.append({"path": coords, "linha": linha})

        if trajetos:
            path_layer = pdk.Layer(
                "PathLayer",
                data=trajetos,
                get_path="path",
                get_color=[0, 150, 255],  # azul
                width_scale=3,
                width_min_pixels=2,
            )
            layers.append(path_layer)

    # Tooltip interativo
    tooltip = {
        "html": "<b>Linha:</b> {codigo_linha} <br/> <b>Prefixo:</b> {prefixo} <br/> <b>Hora:</b> {hora_coleta}",
        "style": {"color": "white"}
    }

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=pdk.ViewState(
            latitude=df_filtrado["latitude"].mean(),
            longitude=df_filtrado["longitude"].mean(),
            zoom=11,
            pitch=0,
        ),
        layers=layers,
        tooltip=tooltip
    ))

    # Legenda
    with st.expander("📖 Mostrar Legenda das Linhas"):
        legenda_df = pd.DataFrame({"Linha": linhas_unicas, "Cor": [cor_map[l] for l in linhas_unicas]})
        legenda_df["Cor"] = legenda_df["Cor"].apply(
            lambda x: f'<div style="width:20px;height:20px;background-color:{x};display:inline-block;margin-right:5px;"></div>{x}'
        )
        st.markdown(legenda_df.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.warning("Nenhum ônibus ativo ou dados de localização ausentes para os filtros selecionados.")

# -------------------------------
# Gráfico de horário
# -------------------------------
st.subheader("📈 Ônibus por Horário")
if not df_filtrado.empty and pd.api.types.is_datetime64_any_dtype(df_filtrado["hora_coleta"]):
    df_valid = df_filtrado.dropna(subset=["hora_coleta"])
    if not df_valid.empty:
        df_hora = df_valid.groupby(df_valid["hora_coleta"].dt.hour).size().reset_index(name="quantidade")
        fig = px.bar(
            df_hora, x="hora_coleta", y="quantidade",
            labels={"hora_coleta": "Hora do dia", "quantidade": "Qtde de ônibus"},
            title="Distribuição de ônibus ao longo do dia",
            color_discrete_sequence=["#21c4ff"]
        )
        fig.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font=dict(color="white"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem dados suficientes para gerar o gráfico de horários.")
else:
    st.info("Coluna de horário ausente ou com formato inválido no CSV.")
