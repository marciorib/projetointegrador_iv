
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np
from datetime import datetime

# --------------------------------
# Configuração da página
# --------------------------------
st.set_page_config(page_title="Previsão SPTrans", layout="wide")

st.title("🧠 Previsão de Atividade de Ônibus - SPTrans")

st.markdown("""
Nesta seção aplicamos **aprendizado de máquina (Machine Learning)** para prever o número estimado 
de ônibus ativos ao longo do dia, com base em dados históricos de operação.
""")

# --------------------------------
# Carregar e preparar dados
# --------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("onibus_todos.csv", usecols=["codigo_linha", "hora_coleta"])
    df["hora_coleta"] = pd.to_datetime(df["hora_coleta"], errors="coerce")
    df = df.dropna(subset=["hora_coleta"])
    df["hora"] = df["hora_coleta"].dt.hour
    df = df.groupby("hora").size().reset_index(name="quantidade")
    return df

df = load_data()

# --------------------------------
# Exibição de dados
# --------------------------------
st.subheader("📊 Dados de Treinamento")
st.dataframe(df)

# --------------------------------
# Modelo preditivo
# --------------------------------
X = df[["hora"]]  # variável independente
y = df["quantidade"]  # variável alvo

# Dividir treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Fazer previsões
y_pred = modelo.predict(X_test)

# Avaliação
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

st.subheader("📈 Avaliação do Modelo")
col1, col2 = st.columns(2)
col1.metric("Erro Médio Absoluto (MAE)", f"{mae:.2f}")
col2.metric("Coeficiente de Determinação (R²)", f"{r2:.2f}")

# --------------------------------
# Previsão para 24h do dia
# --------------------------------
horas = np.arange(0, 24).reshape(-1, 1)
previsoes = modelo.predict(horas)
df_prev = pd.DataFrame({"Hora": horas.flatten(), "Previsão": previsoes})

# Plotar resultados
st.subheader("🔮 Previsão de Quantidade de Ônibus por Hora")
fig = px.line(df_prev, x="Hora", y="Previsão",
              title="Previsão de Atividade de Ônibus ao Longo do Dia",
              markers=True)
fig.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117", font=dict(color="white"))
st.plotly_chart(fig, use_container_width=True)

# --------------------------------
# Interpretação
# --------------------------------
st.markdown("""
### 🧐 Interpretação dos Resultados

O modelo de **Regressão Linear** identifica tendências no comportamento da frota ao longo do dia,
indicando os **horários de maior e menor atividade operacional**.

- 📌 **Picos de operação** normalmente aparecem nos horários de **início e fim de expediente (6h–9h e 17h–20h)**;
- 🕓 O modelo é ajustável e pode ser ampliado para considerar **dias da semana, linhas específicas** e **condições climáticas**;
- ⚙️ A métrica **R²** indica o quanto o modelo explica da variação dos dados — valores próximos de 1.0 representam alta precisão.

""")

st.success("✅ Modelo treinado e previsão gerada com sucesso!")
