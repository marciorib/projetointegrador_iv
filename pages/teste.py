import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import plotly.express as px
from datetime import datetime

# -----------------------------
# Configuração da página
# -----------------------------
st.set_page_config(
    page_title="Análise Preditiva - SPTrans",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Estilo visual (modo escuro)
# -----------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
        font-family: "Segoe UI", sans-serif;
    }
    h1, h2, h3 {
        color: #61dafb;
        font-weight: 600;
    }
    .card {
        background-color: #161a23;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 0 6px rgba(33, 196, 255, 0.08);
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Cabeçalho
# -----------------------------
st.title("🤖 Análise Preditiva - SPTrans")
st.markdown(f"**Última atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")

st.markdown("---")

# -----------------------------
# Carregar os dados
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("onibus_todos.csv")
    if "hora_coleta" not in df.columns:
        st.error("O arquivo CSV precisa conter a coluna 'hora_coleta'.")
        return pd.DataFrame()
    df["hora_coleta"] = pd.to_datetime(df["hora_coleta"], errors="coerce")
    df.dropna(subset=["hora_coleta"], inplace=True)
    return df

df = load_data()

if df.empty:
    st.warning("Nenhum dado carregado. Verifique o arquivo 'onibus_todos.csv'.")
    st.stop()

# -----------------------------
# Pré-processamento dos dados
# -----------------------------
df["hora"] = df["hora_coleta"].dt.hour
df_horas = df.groupby("hora").size().reset_index(name="quantidade")

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🧮 Etapa 1: Análise dos Dados")
st.markdown("""
Os dados coletados foram agrupados por **hora do dia**, permitindo identificar padrões de volume de operação.
Esses dados servirão como base para o modelo de previsão de **quantidade de ônibus ativos por hora**.
""")
st.dataframe(df_horas)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Treinamento do modelo
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🧠 Etapa 2: Treinamento do Modelo")

# Variáveis
X = df_horas[["hora"]]
y = df_horas["quantidade"]

# Modelo de regressão linear
modelo = LinearRegression()
modelo.fit(X, y)

# Previsão
horas_futuras = np.arange(0, 24).reshape(-1, 1)
previsoes = modelo.predict(horas_futuras)

# Métricas
y_pred = modelo.predict(X)
mae = mean_absolute_error(y, y_pred)
r2 = r2_score(y, y_pred)

st.markdown(f"""
O modelo foi treinado utilizando **Regressão Linear** da biblioteca *scikit-learn*.
As métricas de desempenho indicam a qualidade do ajuste:
- **Erro Médio Absoluto (MAE):** {mae:.2f}
- **Coeficiente de Determinação (R²):** {r2:.3f}
""")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Visualização dos resultados
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 Etapa 3: Resultados e Previsões")

df_prev = pd.DataFrame({
    "Hora do dia": horas_futuras.flatten(),
    "Previsão (ônibus ativos)": previsoes
})

fig = px.line(df_prev,
              x="Hora do dia", y="Previsão (ônibus ativos)",
              title="Previsão de Operação de Ônibus por Hora",
              markers=True)
fig.add_bar(x=df_horas["hora"], y=df_horas["quantidade"],
            name="Dados Reais", opacity=0.6)
fig.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font=dict(color="white"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)")
)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Interpretação dos resultados
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📈 Interpretação dos Resultados")
st.markdown("""
O gráfico acima combina os **dados reais** (em barras) e a **tendência prevista** (linha contínua) pelo modelo.

Essa previsão pode ser utilizada para:
- Identificar **horários de pico** de circulação de ônibus;
- Apoiar o **planejamento operacional da frota**;
- Fornecer **insumos para análises de eficiência e sustentabilidade**.

Embora o modelo seja simples, ele demonstra o **potencial da aplicação de aprendizado de máquina** no contexto de mobilidade urbana.
""")
st.markdown('</div>', unsafe_allow_html=True)