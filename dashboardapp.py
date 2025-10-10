import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import warnings
from datetime import datetime
import matplotlib.cm as cm

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

    # Tentar identificar automaticamente a coluna de hora
    possiveis_colunas_hora = ["hora_coleta", "hora", "horario", "data_hora", "dataHora"]
    col_hora = next((c for c in possiveis_colunas_hora if c in df.columns), None)
    df["hora_coleta"] = pd.to_datetime(df[col_hora], errors="coerce") if col_hora else pd.NaT

    # Garantir colunas mínimas
    for col in ["codigo_linha", "prefixo", "latitude", "longitude"]:
        if col not in df.columns:
            df[col] = pd.NA

    # Amostragem se dataset for muito grande
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

# Checkbox e slider
mostrar_trajeto = st.sidebar.checkbox("Mostrar trajetos", value=True)

if pd.api.types.is_datetime64_any_dtype(df["hora_coleta"]):
    horas_disp = df["hora_coleta"].dt.hour.dropna().unique()
    hora_sel = st.sidebar.slider(
        "Selecione a hora do dia:",
        min_value=int(horas_disp.min()),
        max_value=int(horas_disp.max()),
        value=int(horas_disp.min())
    )
    df_filtrado = df_filtrado[df_filtrado["hora_coleta"].dt.hour == hora_sel]

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
    return {linha: [int(255*r), int(255*g), int(255*b), 180] for linha, (r, g, b, _) in zip(linhas_unicas, cmap(range(len(linhas_unicas))))}

# -------------------------------
# Layout - Cabeçalho e Métricas
# -------------------------------
st.title("📊 Dashboard SPTrans - Ônibus em Tempo Real")

col1, col2, col3 = st.columns(3)
col1.metric("🚌 Ônibus ativos", len(df_filtrado["prefixo"].dropna().unique()))
col2.metric("📋 Linhas selecionadas", len(linhas))
col3.metric("⏱️ Última coleta", formatar_data_segura(df_filtrado["hora_coleta"].max()))

# -------------------------------
# Dados e Mapa Interativo
# -------------------------------
with st.expander("📋 Mostrar dados detalhados"):
    st.dataframe(
        df_filtrado[["codigo_linha", "prefixo", "latitude", "longitude", "hora_coleta"]]
        .sort_values("hora_coleta")
        .reset_index(drop=True),
        use_container_width=True
    )

st.subheader("🗺️ Mapa Interativo dos Ônibus")

if not df_filtrado.empty and df_filtrado[["latitude", "longitude"]].notna().all(axis=None):
    linhas_unicas = df_filtrado["codigo_linha"].dropna().unique()
    cor_map = gerar_cores_linhas(linhas_unicas)
    df_filtrado["rgba"] = df_filtrado["codigo_linha"].map(cor_map)

    # 🟢 Layer de pontos (ônibus)
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_filtrado,
        get_position=["longitude", "latitude"],
        get_color="rgba",
        get_radius=70,
        pickable=True
    )

    layers = [scatter_layer]

    # 🔵 Layer de trajetos — agora um por ônibus (prefixo)
    if mostrar_trajeto:
        trajetos = []
        for (linha, prefixo), grupo in df_filtrado.groupby(["codigo_linha", "prefixo"]):
            grupo = grupo.sort_values("hora_coleta")
            coords = grupo[["longitude", "latitude"]].dropna().values.tolist()
            if len(coords) > 1:
                trajetos.append({
                    "path": coords,
                    "linha": linha,
                    "prefixo": prefixo,
                    "cor": cor_map.get(linha, [0, 150, 255, 180])
                })

        if trajetos:
            path_layer = pdk.Layer(
                "PathLayer",
                data=trajetos,
                get_path="path",
                get_color="cor",
                width_scale=1.5,
                width_min_pixels=1.5,
                rounded=True,
                pickable=False
            )
            layers.append(path_layer)

    # 🎯 Zoom dinâmico
    if len(linhas_unicas) == 1:
        zoom_data = df_filtrado[df_filtrado["codigo_linha"] == linhas_unicas[0]]
    else:
        zoom_data = df_filtrado

    view_state = pdk.ViewState(
        latitude=zoom_data["latitude"].mean(),
        longitude=zoom_data["longitude"].mean(),
        zoom=12 if len(linhas_unicas) == 1 else 11,
        pitch=0
    )

    tooltip = {
        "html": "<b>Linha:</b> {codigo_linha}<br><b>Prefixo:</b> {prefixo}<br><b>Hora:</b> {hora_coleta}",
        "style": {"color": "white"}
    }

    # 🗺️ Renderização do mapa
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=view_state,
        layers=layers,
        tooltip=tooltip
    ))

    # -------------------------------
    # Legenda Oculta (em tabela com 4 colunas)
    # -------------------------------
    with st.expander("🎨 Mostrar legenda das linhas"):
        if cor_map:
            num_colunas = 4
            linhas_legenda = list(cor_map.items())
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
