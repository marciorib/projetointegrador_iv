import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.colors as mcolors
import random
import time
from datetime import datetime

# --------------------------------
# Configuração da página
# --------------------------------
st.set_page_config(page_title="Dashboard SPTrans", layout="wide")

st.title("📊 Dashboard SPTrans - Ônibus em Tempo Real com Animação Temporal")

# --------------------------------
# Carregar dados
# --------------------------------
@st.cache_data
def load_data():
    colunas = ["codigo_linha", "prefixo", "latitude", "longitude", "hora_coleta"]
    df = pd.read_csv("onibus_todos.csv", usecols=colunas)

    # Converter hora_coleta para datetime
    df["hora_coleta"] = pd.to_datetime(df["hora_coleta"], errors="coerce")

    # Remover linhas sem coordenadas
    df = df.dropna(subset=["latitude", "longitude", "hora_coleta", "codigo_linha"])

    # Converter código de linha para string (evita erro de tipo)
    df["codigo_linha"] = df["codigo_linha"].astype(str)
    df = df[df["codigo_linha"].str.lower() != "nan"]

    return df

df = load_data()

# --------------------------------
# Sidebar - Filtros
# --------------------------------
st.sidebar.header("🛠️ Filtros")

# Opções de linhas disponíveis
opcoes_linhas = sorted(df["codigo_linha"].unique())

linhas = st.sidebar.multiselect(
    "Escolha a(s) linha(s):",
    options=opcoes_linhas,
    default=opcoes_linhas[:5]
)

df_filtrado = df[df["codigo_linha"].isin(linhas)]

# --------------------------------
# Animação temporal
# --------------------------------
st.sidebar.subheader("⏱️ Animação Temporal")

# Slider de hora
hora = st.sidebar.slider("Selecione o horário", 0, 23, 8)

# Botão de animação automática
animar = st.sidebar.button("▶️ Reproduzir animação (24h)")

# Filtrar dados pela hora selecionada
df_hora = df_filtrado[df_filtrado["hora_coleta"].dt.hour == hora]

# --------------------------------
# Exibição do mapa
# --------------------------------
st.subheader(f"🗺️ Localização dos ônibus às {hora:02d}:00")

if not df_hora.empty:
    # Gerar cores únicas por linha
    linhas_unicas = df_hora["codigo_linha"].unique()
    cores = random.choices(list(mcolors.TABLEAU_COLORS.values()), k=len(linhas_unicas))
    cor_map = dict(zip(linhas_unicas, cores))

    # Criar coluna de cor RGBA
    df_hora["cor_rgba"] = df_hora["codigo_linha"].map(
        lambda x: list(mcolors.to_rgba(cor_map.get(x, "#21c4ff"), alpha=0.8))
    )

    # Camada de pontos
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_hora,
        get_position=["longitude", "latitude"],
        get_fill_color="cor_rgba",
        get_radius=60,
        pickable=True,
    )

    tooltip = {
        "html": "<b>Linha:</b> {codigo_linha}<br/><b>Prefixo:</b> {prefixo}<br/><b>Hora:</b> {hora_coleta}",
        "style": {"color": "white"},
    }

    # Renderizar mapa
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v10",
            initial_view_state=pdk.ViewState(
                latitude=df_hora["latitude"].mean(),
                longitude=df_hora["longitude"].mean(),
                zoom=11,
            ),
            layers=[scatter_layer],
            tooltip=tooltip,
        )
    )

else:
    st.info("Nenhum ônibus ativo neste horário.")

# --------------------------------
# Animação automática
# --------------------------------
if animar:
    st.sidebar.write("⏯️ Animação em andamento...")
    placeholder = st.empty()

    for h in range(0, 24):
        df_h = df_filtrado[df_filtrado["hora_coleta"].dt.hour == h]
        if df_h.empty:
            continue

        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_h,
            get_position=["longitude", "latitude"],
            get_fill_color="[255, 140, 0, 160]",
            get_radius=60,
        )

        placeholder.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/dark-v10",
                initial_view_state=pdk.ViewState(
                    latitude=df_h["latitude"].mean(),
                    longitude=df_h["longitude"].mean(),
                    zoom=11,
                ),
                layers=[scatter_layer],
            )
        )

        st.sidebar.write(f"⏰ {h:02d}:00")
        time.sleep(0.5)

    st.sidebar.success("✅ Animação concluída!")

# --------------------------------
# Gráfico de distribuição por hora
# --------------------------------
st.subheader("📈 Distribuição de Ônibus por Horário")

if not df_filtrado.empty:
    df_horas = (
        df_filtrado.groupby(df_filtrado["hora_coleta"].dt.hour)
        .size()
        .reset_index(name="quantidade")
    )

    import plotly.express as px

    fig = px.bar(
        df_horas,
        x="hora_coleta",
        y="quantidade",
        labels={"hora_coleta": "Hora do Dia", "quantidade": "Qtde de Ônibus"},
        title="Distribuição de Ônibus ao Longo do Dia",
        color_discrete_sequence=["#21c4ff"],
    )
    fig.update_layout(
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font=dict(color="white"),
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Nenhum dado disponível para gerar o gráfico de horários.")
