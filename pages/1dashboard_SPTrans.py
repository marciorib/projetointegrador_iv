
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import warnings
from datetime import datetime
import matplotlib.cm as cm
import numpy as np

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

    # Detectar automaticamente a coluna de hora
    possiveis_colunas_hora = ["hora_coleta", "hora", "horario", "data_hora", "dataHora"]
    col_hora = next((c for c in possiveis_colunas_hora if c in df.columns), None)
    df["hora_coleta"] = pd.to_datetime(df[col_hora], errors="coerce") if col_hora else pd.NaT

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
# Funções auxiliares
# -------------------------------
def formatar_data_segura(data):
    if pd.isna(data):
        return "N/A"
    if isinstance(data, (pd.Timestamp, datetime)):
        return data.strftime("%d/%m/%Y %H:%M:%S")
    return str(data)

def gerar_cores_linhas(linhas_unicas):
    cmap = cm.get_cmap('tab20', len(linhas_unicas))
    return {linha: [int(255*r), int(255*g), int(255*b), 180]
            for linha, (r, g, b, _) in zip(linhas_unicas, cmap(range(len(linhas_unicas))))}

# -------------------------------
# Sidebar - Filtros principais
# -------------------------------
st.sidebar.header("🛠️ Filtros")

mostrar_trajeto = st.sidebar.checkbox("Mostrar trajetos", value=True)

linhas_disponiveis = df["codigo_linha"].dropna().unique()
linhas_selecionadas = st.sidebar.multiselect(
    "Escolha a(s) linha(s):",
    options=linhas_disponiveis,
    default=linhas_disponiveis
)

df_filtrado = df[df["codigo_linha"].isin(linhas_selecionadas)] if linhas_selecionadas else df.copy()

# Filtro por hora
if pd.api.types.is_datetime64_any_dtype(df["hora_coleta"]):
    horas_disp = df["hora_coleta"].dt.hour.dropna().unique()
    if len(horas_disp) > 0:
        hora_sel = st.sidebar.slider(
            "Selecione a hora do dia:",
            min_value=int(horas_disp.min()),
            max_value=int(horas_disp.max()),
            value=int(horas_disp.min())
        )
        df_filtrado = df_filtrado[df_filtrado["hora_coleta"].dt.hour == hora_sel]

# -------------------------------
# Cabeçalho e Métricas
# -------------------------------
st.title("📊 Dashboard SPTrans - Ônibus em Tempo Real")

col1, col2, col3 = st.columns(3)
col1.metric("🚌 Ônibus ativos", len(df_filtrado["prefixo"].dropna().unique()))
col2.metric("📋 Linhas selecionadas", len(linhas_selecionadas))
col3.metric("⏱️ Última coleta", formatar_data_segura(df_filtrado["hora_coleta"].max()))

# -------------------------------
# Legenda e filtro interativo
# -------------------------------
st.subheader("🎨 Legenda e Filtro de Linhas")

linhas_unicas = df_filtrado["codigo_linha"].dropna().unique()
cor_map = gerar_cores_linhas(linhas_unicas)

with st.expander(f"🎨 Mostrar legenda das linhas ({len(linhas_unicas)} disponíveis)"):
    if len(linhas_unicas) > 0:
        termo_busca = st.text_input("🔎 Pesquisar linha:", "").strip().lower()
        linhas_filtradas = [l for l in linhas_unicas if termo_busca in str(l).lower()]

        linhas_visiveis = st.multiselect(
            "Filtrar linhas no mapa:",
            options=linhas_filtradas,
            default=linhas_filtradas
        )

        df_filtrado = df_filtrado[df_filtrado["codigo_linha"].isin(linhas_visiveis)]

        num_colunas = 4
        linhas_legenda = [(linha, cor_map[linha]) for linha in linhas_visiveis if linha in cor_map]
        linhas_html = "<table style='width:100%; text-align:left; border-spacing:10px;'>"
        for i in range(0, len(linhas_legenda), num_colunas):
            linhas_html += "<tr>"
            for linha, cor in linhas_legenda[i:i + num_colunas]:
                rgba = f"rgba({cor[0]},{cor[1]},{cor[2]},1)"
                linhas_html += f"<td style='padding:5px;'><div style='display:flex;align-items:center;'><div style='width:20px;height:20px;background:{rgba};margin-right:8px;border-radius:4px;'></div>{linha}</div></td>"
            linhas_html += "</tr>"
        linhas_html += "</table>"
        st.markdown(linhas_html, unsafe_allow_html=True)
    else:
        st.info("Nenhuma linha disponível para exibir na legenda.")

# -------------------------------
# Dados e Mapa Interativo
# -------------------------------
st.subheader("🗺️ Mapa Interativo dos Ônibus")

if not df_filtrado.empty:
    # Converter colunas para tipos nativos
    df_filtrado["latitude"] = pd.to_numeric(df_filtrado["latitude"], errors="coerce").astype(float)
    df_filtrado["longitude"] = pd.to_numeric(df_filtrado["longitude"], errors="coerce").astype(float)
    df_filtrado["hora_coleta_str"] = df_filtrado["hora_coleta"].apply(formatar_data_segura)
    df_filtrado["rgba"] = df_filtrado["codigo_linha"].map(cor_map).apply(lambda c: list(map(int, c)) if c else [33,196,255,180])

    df_mapa = df_filtrado.dropna(subset=["latitude", "longitude"])

    # 🔹 ScatterplotLayer (ônibus)
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_mapa.to_dict(orient="records"),
        get_position='[longitude, latitude]',
        get_color='rgba',
        get_radius=70,
        pickable=True
    )

    layers = [scatter_layer]

    # 🔹 PathLayer (trajetos)
    if mostrar_trajeto:
        trajetos = []
        for (linha, prefixo), grupo in df_mapa.groupby(["codigo_linha", "prefixo"]):
            grupo = grupo.sort_values("hora_coleta")
            coords = grupo[["longitude", "latitude"]].dropna().values.tolist()
            coords = [[float(lon), float(lat)] for lon, lat in coords]
            if len(coords) > 1:
                trajetos.append({
                    "path": coords,
                    "linha": str(linha),
                    "prefixo": str(prefixo),
                    "cor": [int(x) for x in cor_map.get(linha, [0,150,255,180])]
                })

        if trajetos:
            path_layer = pdk.Layer(
                "PathLayer",
                data=trajetos,
                get_path="path",
                get_color="cor",
                width_scale=1.5,
                width_min_pixels=1.2,
                rounded=True,
                pickable=False
            )
            layers.append(path_layer)

    # 🔹 Configuração do mapa
    view_state = pdk.ViewState(
        latitude=float(df_mapa["latitude"].mean()),
        longitude=float(df_mapa["longitude"].mean()),
        zoom=12 if len(linhas_unicas) == 1 else 11,
        pitch=0
    )

    tooltip = {
        "html": "<b>Linha:</b> {codigo_linha}<br><b>Prefixo:</b> {prefixo}<br><b>Hora:</b> {hora_coleta_str}",
        "style": {"color": "white"}
    }

    try:
        deck = pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v10",
            initial_view_state=view_state,
            layers=layers,
            tooltip=tooltip
        )
        st.pydeck_chart(deck)
    except Exception as e:
        st.error(f"Erro ao renderizar mapa: {e}")

else:
    st.warning("Nenhum dado disponível para exibição no mapa.")

# -------------------------------
# Gráfico de Horário
# -------------------------------
st.subheader("📈 Distribuição de Ônibus por Horário")
if not df_filtrado.empty and pd.api.types.is_datetime64_any_dtype(df_filtrado["hora_coleta"]):
    df_hora = df_filtrado.groupby(df_filtrado["hora_coleta"].dt.hour).size().reset_index(name="quantidade")
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


#------------------------------------------------------------------------------------------------------------------------------
