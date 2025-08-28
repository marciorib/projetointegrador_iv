import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
import warnings
from datetime import datetime

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
    /* Fundo geral */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
        font-family: "Segoe UI", sans-serif;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #61dafb;
        font-weight: 600;
    }

    /* Cards (métricas) */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        color: #21c4ff;
    }
    [data-testid="stMetricDelta"] {
        color: #f0f0f0 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161a23;
    }

    /* Tabela */
    .ag-theme-balham {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Botões */
    button[kind="primary"] {
        background-color: #21c4ff !important;
        color: black !important;
        border-radius: 8px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# Função para carregar dados
# -------------------------------
@st.cache_data
def load_data(caminho_csv, n_amostra=10000):
    cols = ["hora_coleta", "codigo_linha", "prefixo", "latitude", "longitude"]
    df = pd.read_csv(caminho_csv, usecols=cols)

    # Converter hora_coleta em datetime
    df["hora_coleta"] = pd.to_datetime(df["hora_coleta"], errors="coerce")

    # Amostra se for muito grande
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
    options=df["codigo_linha"].unique(),
    default=df["codigo_linha"].unique()
)

df_filtrado = df[df["codigo_linha"].isin(linhas)]

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
# Layout
# -------------------------------
st.title("📊 Dashboard SPTrans - Ônibus em Tempo Real")

# Cards
col1, col2, col3 = st.columns(3)
col1.metric("🚌 Total de ônibus ativos", len(df_filtrado["prefixo"].unique()))
col2.metric("📋 Linhas selecionadas", len(linhas))
col3.metric("⏱️ Última coleta", formatar_data_segura(df_filtrado["hora_coleta"].max()))

# -------------------------------
# Tabela
# -------------------------------
st.subheader("📋 Prévia dos Dados")
if not df_filtrado.empty:
    gb = GridOptionsBuilder.from_dataframe(df_filtrado)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    grid_options = gb.build()
    AgGrid(df_filtrado, gridOptions=grid_options, theme="balham")
else:
    st.info("Nenhum dado disponível para os filtros selecionados.")

# -------------------------------
# Mapa
# -------------------------------
st.subheader("🗺️ Localização dos Ônibus")
if not df_filtrado.empty:
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=pdk.ViewState(
            latitude=df_filtrado["latitude"].mean(),
            longitude=df_filtrado["longitude"].mean(),
            zoom=11,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df_filtrado,
                get_position='[longitude, latitude]',
                get_color='[0, 180, 255, 180]',
                get_radius=70,
                pickable=True
            )
        ]
    ))
else:
    st.warning("Nenhum ônibus ativo no momento para os filtros selecionados.")

# -------------------------------
# Gráfico
# -------------------------------
st.subheader("📈 Ônibus por Horário")
if not df_filtrado.empty and pd.api.types.is_datetime64_any_dtype(df_filtrado["hora_coleta"]):
    df_hora = (
        df_filtrado.dropna(subset=["hora_coleta"])
        .assign(hora=df_filtrado["hora_coleta"].dt.hour)
        .groupby("hora")
        .size()
        .reset_index(name="quantidade")
    )
    fig = px.bar(
        df_hora, x="hora", y="quantidade",
        labels={"hora": "Hora do dia", "quantidade": "Qtde de ônibus"},
        title="Distribuição de ônibus ao longo do dia",
        color_discrete_sequence=["#21c4ff"]
    )
    fig.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Sem dados suficientes para gerar o gráfico de horários.")

