import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard SPTrans", layout="wide")

# Título
st.title("📊 Dashboard SPTrans - Ônibus em Tempo Real")

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv("onibus_todos.csv")
    df["hora_coleta"] = pd.to_datetime(df["hora_coleta"])
    return df

df = load_data()

# Sidebar - Filtros
st.sidebar.header("Filtros")
linhas = st.sidebar.multiselect(
    "Escolha a(s) linha(s):",
    options=df["codigo_linha"].unique(),
    default=df["codigo_linha"].unique()
)

df_filtrado = df[df["codigo_linha"].isin(linhas)]

# Visualização rápida dos dados
st.subheader("📋 Prévia dos Dados")
st.dataframe(df_filtrado)

# Mapa das posições dos ônibus
st.subheader("🚌 Localização dos Ônibus")
if not df_filtrado.empty:
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/streets-v11",
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
                get_color='[200, 30, 0, 160]',
                get_radius=50,
                pickable=True
            )
        ]
    ))
else:
    st.info("Nenhum ônibus ativo na linha selecionada.")

# Estatísticas
st.subheader("📊 Estatísticas")
st.metric("Total de ônibus ativos", len(df_filtrado["prefixo"].unique()))
st.metric("Linhas selecionadas", len(linhas))
st.metric("Última coleta", df_filtrado["hora_coleta"].max() if not df_filtrado.empty else "N/A")

# Gráfico de ônibus por horário
st.subheader("⏱️ Ônibus por Horário")
if not df_filtrado.empty:
    df_hora = df_filtrado.groupby(df_filtrado["hora_coleta"].dt.hour).size().reset_index(name='quantidade')
    fig = px.bar(df_hora, x='hora_coleta', y='quantidade', labels={'hora_coleta':'Hora do dia', 'quantidade':'Qtde de ônibus'})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Nenhum dado disponível para o gráfico de horários.")
