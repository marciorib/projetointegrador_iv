import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
from datetime import datetime
from geopy.geocoders import Nominatim
import time
import warnings

warnings.filterwarnings("ignore")

# ------------------------------
# Configuração da página
# ------------------------------
st.set_page_config(page_title="Dashboard SPTrans", layout="wide", page_icon="🚌")

# ------------------------------
# Estilo visual
# ------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: #ffffff;
    font-family: "Segoe UI", sans-serif;
}
h1, h2, h3 {
    color: #21c4ff;
}
[data-testid="stMetricValue"] {
    font-size: 28px;
    color: #00bfff;
}
.stButton>button {
    background-color: #21c4ff;
    color: black;
    font-weight: 600;
    border-radius: 10px;
    padding: 0.5em 1em;
}
.stButton>button:hover {
    background-color: #15a7db;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Carregamento dos dados
# ------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("onibus_todos.csv", usecols=["codigo_linha", "prefixo", "latitude", "longitude", "hora_coleta"])
    df["hora_coleta"] = pd.to_datetime(df["hora_coleta"], errors="coerce")
    df = df.dropna(subset=["latitude", "longitude", "hora_coleta"])
    df["hora"] = df["hora_coleta"].dt.hour
    if len(df) > 5000:
        df = df.sample(5000, random_state=42)
    return df

df = load_data()

# ------------------------------
# Cabeçalho
# ------------------------------
st.title("🗺️ Dashboard SPTrans - Ônibus em Tempo Real")
st.markdown("### _Análise e Visualização Interativa das Linhas de Ônibus de São Paulo_")
st.markdown("---")

# ------------------------------
# Métricas principais
# ------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("🚌 Ônibus ativos", len(df["prefixo"].unique()))
col2.metric("🚏 Linhas monitoradas", len(df["codigo_linha"].unique()))
col3.metric("🕒 Última coleta", df["hora_coleta"].max().strftime("%d/%m/%Y %H:%M:%S"))

st.markdown("---")

# ------------------------------
# 🔎 Busca por bairro ou rua
# ------------------------------
geolocator = Nominatim(user_agent="sptrans_dashboard")

with st.expander("📍 Buscar bairro ou rua (opcional)"):
    local_input = st.text_input("Digite o nome de um bairro ou rua de São Paulo:")
    search_coords = None
    marker_data = pd.DataFrame()

    if local_input:
        try:
            location = geolocator.geocode(f"{local_input}, São Paulo, Brasil", timeout=10)
            if location:
                search_coords = (location.latitude, location.longitude)
                st.success(f"📌 Local encontrado: {location.address}")

                marker_data = pd.DataFrame([{
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "local": location.address
                }])
            else:
                st.warning("⚠️ Local não encontrado. Tente um nome mais específico.")
        except Exception as e:
            st.error(f"Erro ao buscar o local: {e}")

# ------------------------------
# Filtro de linha
# ------------------------------
with st.expander("🧭 Filtros de Linhas (opcional)"):
    linhas = st.multiselect(
        "Selecione uma ou mais linhas para visualizar:",
        options=sorted(df["codigo_linha"].dropna().unique()),
        default=[]
    )

# ------------------------------
# Filtragem
# ------------------------------
if linhas:
    df_filtrado = df[df["codigo_linha"].isin(linhas)].copy()
else:
    df_filtrado = df.copy()

# ------------------------------
# Controle de Animação Temporal
# ------------------------------
st.subheader("⏯️ Simulação Temporal de Movimentação dos Ônibus")

horas_disponiveis = sorted(df_filtrado["hora"].unique())
hora_inicial = st.select_slider(
    "Selecione o horário inicial para simulação:",
    options=horas_disponiveis,
    value=min(horas_disponiveis)
)

col_play, col_stop = st.columns([1, 1])
play = col_play.button("▶️ Iniciar Animação")
stop = col_stop.button("⏸️ Pausar")

# ------------------------------
# Função para exibir o mapa
# ------------------------------
def exibir_mapa(df_mapa, marker_data=None, center_coords=(-23.55, -46.63), zoom=11):
    layers = []

    # Camada de ônibus
    df_mapa["rgba"] = df_mapa.apply(lambda x: [33, 196, 255, 160], axis=1)
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_mapa,
        get_position=["longitude", "latitude"],
        get_color="rgba",
        get_radius=60,
        pickable=True
    )
    layers.append(scatter_layer)

    # Marcador do local pesquisado
    if marker_data is not None and not marker_data.empty:
        marker_layer = pdk.Layer(
            "ScatterplotLayer",
            data=marker_data,
            get_position=["longitude", "latitude"],
            get_color=[255, 0, 0, 240],
            get_radius=150,
            pickable=True
        )
        layers.append(marker_layer)

    tooltip = {
        "html": """
        <b>Linha:</b> {codigo_linha}<br/>
        <b>Prefixo:</b> {prefixo}<br/>
        <b>Hora:</b> {hora_coleta}<br/>
        <b>Local:</b> {local}
        """,
        "style": {"color": "white"}
    }

    view_state = pdk.ViewState(
        latitude=center_coords[0],
        longitude=center_coords[1],
        zoom=zoom
    )

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/navigation-night-v1",
        initial_view_state=view_state,
        layers=layers,
        tooltip=tooltip
    ))

# ------------------------------
# Exibir mapa com animação
# ------------------------------
if play:
    st.info("🎬 Simulação iniciada...")
    for h in horas_disponiveis:
        df_hora = df_filtrado[df_filtrado["hora"] == h]
        st.subheader(f"🕐 Exibindo movimentação - {h:02d}:00")
        exibir_mapa(df_hora, marker_data, search_coords or (-23.55, -46.63), zoom=13 if search_coords else 11)
        time.sleep(1.5)
else:
    df_atual = df_filtrado[df_filtrado["hora"] == hora_inicial]
    st.subheader(f"🕐 Visualização Estática - {hora_inicial:02d}:00")
    exibir_mapa(df_atual, marker_data, search_coords or (-23.55, -46.63), zoom=13 if search_coords else 11)

st.markdown("---")

# ------------------------------
# Gráfico de ônibus por hora
# ------------------------------
st.subheader("📊 Distribuição de Ônibus por Horário")

if not df_filtrado.empty:
    df_hora = df_filtrado.groupby(df_filtrado["hora"]).size().reset_index(name="quantidade")
    fig = px.line(
        df_hora, x="hora", y="quantidade",
        labels={"hora": "Hora do Dia", "quantidade": "Qtde de Ônibus"},
        title="Distribuição de Ônibus ao Longo do Dia",
        markers=True
    )
    fig.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Sem dados suficientes para gerar o gráfico de horários.")

# ------------------------------
# Rodapé
# ------------------------------
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #cccccc;'>
    <p>📍 <b>UNIVESP – Universidade Virtual do Estado de São Paulo</b></p>
    <p>👨‍💻 Projeto Integrador IV – Engenharia de Computação e Ciência de Dados</p>
    <p>🧩 Grupo 07 – Polo Bauru | Orientador: Prof. Vinício Marcelo Pereira</p>
    <p>© 2025 – Todos os direitos reservados</p>
</div>
""", unsafe_allow_html=True)
