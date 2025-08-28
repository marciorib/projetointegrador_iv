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
# Função para carregar dados
# -------------------------------
@st.cache_data
def load_data(caminho_csv, n_amostra=10000):
    df = pd.read_csv(caminho_csv)

    # Garantir colunas mínimas
    for col in ["hora_coleta", "codigo_linha", "prefixo", "latitude", "longitude"]:
        if col not in df.columns:
            df[col] = pd.NA

    # Converter hora_coleta em datetime
    df["hora_coleta"] = pd.to_datetime(df["hora_coleta"], errors="coerce")

    # Amostragem se dataset grande
    if len(df) > n_amostra:
        df = df.sample(n=n_amostra, random_state=42)

    return df

df = load_data("onibus_todos.csv")

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
# Mapa com tooltip e trajetos previstos
# -------------------------------
st.subheader("🗺️ Localização e Trajetos dos Ônibus")
if not df_filtrado.empty and df_filtrado[["latitude", "longitude"]].notna().all(axis=None):
    # Cores por linha
    linhas_unicas = df_filtrado["codigo_linha"].dropna().unique()
    cores = random.choices(list(mcolors.CSS4_COLORS.values()), k=len(linhas_unicas))
    cor_map = dict(zip(linhas_unicas, cores))
    df_filtrado["cor"] = df_filtrado["codigo_linha"].map(cor_map).fillna("#21c4ff")
    df_filtrado["rgba"] = df_filtrado["cor"].apply(lambda x: hex_to_rgba(x))

    # Camada ScatterplotLayer (ônibus)
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_filtrado,
        get_position=["longitude", "latitude"],
        get_color="rgba",
        get_radius=70,
        pickable=True
    )

    # Criar trajetos previstos: conectar pontos consecutivos do mesmo prefixo
    trajetos = []
    for prefixo, df_bus in df_filtrado.groupby("prefixo"):
        df_sorted = df_bus.sort_values("hora_coleta")
        coords = df_sorted[["longitude", "latitude"]].values
        for i in range(len(coords)-1):
            trajetos.append({
                "from_lon": coords[i][0], "from_lat": coords[i][1],
                "to_lon": coords[i+1][0], "to_lat": coords[i+1][1],
                "cor": cor_map.get(df_sorted["codigo_linha"].iloc[i], "#21c4ff")
            })
    df_trajetos = pd.DataFrame(trajetos)
    if not df_trajetos.empty:
        trajetos_layer = pdk.Layer(
            "LineLayer",
            data=df_trajetos,
            get_source_position=["from_lon", "from_lat"],
            get_target_position=["to_lon", "to_lat"],
            get_color=[180, 180, 180],
            get_width=3
        )
        layers = [scatter_layer, trajetos_layer]
    else:
        layers = [scatter_layer]

    # Tooltip interativo
    tooltip = {
        "html": "<b>Linha:</b> {codigo_linha} <br/> <b>Prefixo:</b> {prefixo} <br/> <b>Hora:</b> {hora_coleta}",
        "style": {"color": "white"}
    }

    # Deck com camadas e tooltip
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

    # Legenda escondida
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
    st.info("Coluna 'hora_coleta' ausente ou com formato inválido.")

