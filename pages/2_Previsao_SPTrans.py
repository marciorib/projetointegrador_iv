
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

# ------------------------------
# Configuração da página
# ------------------------------
st.set_page_config(page_title="Previsão SPTrans", layout="wide", page_icon="🤖")

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
# Título
# ------------------------------
st.title("🤖 Previsão de Atividade da Frota SPTrans")
st.markdown("### _Módulo de Aprendizado de Máquina – Projeto Integrador IV (UNIVESP)_")
st.markdown("---")

# ------------------------------
# Função para carregar os dados
# ------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("onibus_todos.csv", usecols=["hora_coleta", "codigo_linha", "prefixo"])
    df["hora_coleta"] = pd.to_datetime(df["hora_coleta"], errors="coerce")
    df = df.dropna(subset=["hora_coleta"])
    df["hora"] = df["hora_coleta"].dt.hour
    return df

df = load_data()

# ------------------------------
# Análise dos dados
# ------------------------------
st.subheader("📊 Distribuição de Ônibus por Hora (dados históricos)")
df_hora = df.groupby("hora").size().reset_index(name="quantidade")

fig = px.bar(
    df_hora, x="hora", y="quantidade",
    labels={"hora": "Hora do Dia", "quantidade": "Qtde de Ônibus"},
    title="Distribuição Histórica de Ônibus ao Longo do Dia",
    color_discrete_sequence=["#21c4ff"]
)
fig.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font=dict(color="white"))
st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# Modelo de Aprendizado de Máquina
# ------------------------------
st.subheader("🧠 Modelo de Regressão Linear")

# Variáveis de entrada e saída
X = df_hora[["hora"]]
y = df_hora["quantidade"]

# Divisão treino/teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinamento
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Predições
y_pred = modelo.predict(X_test)

# Métricas
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

col1, col2 = st.columns(2)
col1.metric("📉 Erro Médio Absoluto (MAE)", f"{mae:.2f}")
col2.metric("📈 R² (Coeficiente de Determinação)", f"{r2:.2f}")

st.markdown("---")

# ------------------------------
# Visualização da regressão
# ------------------------------
st.subheader("📈 Visualização do Modelo de Regressão Linear")

df_pred = pd.DataFrame({"hora": range(0, 24)})
df_pred["predito"] = modelo.predict(df_pred[["hora"]])

fig_pred = px.line(
    df_pred, x="hora", y="predito",
    labels={"hora": "Hora do Dia", "predito": "Qtde Prevista de Ônibus"},
    title="Previsão de Ônibus Ativos ao Longo do Dia",
    markers=True
)
fig_pred.add_bar(x=df_hora["hora"], y=df_hora["quantidade"], name="Histórico", opacity=0.5)
fig_pred.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font=dict(color="white"))
st.plotly_chart(fig_pred, use_container_width=True)

# ------------------------------
# Previsão interativa
# ------------------------------
st.markdown("---")
st.subheader("🎯 Faça uma Previsão Manual")

hora_usuario = st.slider("Selecione a hora do dia (0 a 23)", 0, 23, 12)
predicao = modelo.predict(np.array([[hora_usuario]]))[0]
st.success(f"🕒 Previsão: aproximadamente **{predicao:.0f} ônibus ativos** às **{hora_usuario}:00h**.")

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
