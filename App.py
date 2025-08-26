# 📌 Código do Dashboard (Streamlit)




import requests
import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import datetime

# === CONFIGURAÇÕES ===
TOKEN = "SUA_CHAVE_AQUI"  # coloque seu token da SPTrans aqui
NUMERO_LINHA = "8000"     # exemplo: linha 8000

# === FUNÇÃO PARA AUTENTICAÇÃO ===
def autenticar(session, token):
    url = f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={token}"
    resp = session.post(url)
    return resp.status_code == 200 and resp.json() is True

# === FUNÇÃO PARA PEGAR POSIÇÕES DOS ÔNIBUS ===
def get_posicoes(session, numero_linha):
    # buscar código interno da linha
    linha_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca={numero_linha}"
    linha_data = session.get(linha_url).json()
    if not linha_data:
        return None, None

    codigo_linha = linha_data[0]["cl"]
    nome_linha = linha_data[0]["lt"]

    # buscar posições em tempo real
    posicoes_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao?codigoLinha={codigo_linha}"
    posicoes = session.get(posicoes_url).json()

    if "vs" not in posicoes or not posicoes["vs"]:
        return nome_linha, None

    # montar dataframe
    dados = []
    for onibus in posicoes["vs"]:
        dados.append({
            "prefixo": onibus["p"],
            "latitude": onibus["py"],
            "longitude": onibus["px"],
            "hora_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    df = pd.DataFrame(dados)
    return nome_linha, df

# === DASHBOARD STREAMLIT ===
st.set_page_config(page_title="SPTrans em Tempo Real", layout="wide")

st.title("🚌 Monitoramento de Ônibus em Tempo Real - SPTrans")

# Sessão de autenticação
session = requests.Session()
if not autenticar(session, TOKEN):
    st.error("❌ Erro na autenticação. Verifique seu token da SPTrans.")
    st.stop()

# Entrada da linha
linha_input = st.text_input("Digite o número da linha:", NUMERO_LINHA)

if st.button("🔎 Buscar ônibus"):
    nome_linha, df = get_posicoes(session, linha_input)

    if nome_linha is None:
        st.warning("Linha não encontrada.")
    elif df is None:
        st.warning(f"Nenhum ônibus em operação para a linha {linha_input}.")
    else:
        st.success(f"Linha {nome_linha} - {len(df)} ônibus encontrados")

        # Mostrar tabela
        st.dataframe(df)

        # Mostrar no mapa (Pydeck)
        st.subheader("Mapa dos ônibus em tempo real")
        view_state = pdk.ViewState(
            latitude=df["latitude"].mean(),
            longitude=df["longitude"].mean(),
            zoom=12
        )

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position="[longitude, latitude]",
            get_color="[200, 30, 0, 160]",
            get_radius=80,
            pickable=True
        )

        r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "Ônibus {prefixo}"})
        st.pydeck_chart(r)






# 📌 Como rodar

#Instale as dependências:
#pip install streamlit requests pandas pydeck

#Rode o dashboard:
#streamlit run app.py


#No navegador vai abrir em:
#👉 http://localhost:8501

#Lá você digita o número da linha (ex: 8000) e verá:
#Uma tabela com prefixo, latitude, longitude e horário de coleta.
#Um mapa interativo mostrando os ônibus em tempo real.
#👉 Esse protótipo já é suficiente para você mostrar a parte de IoT (dados em tempo real) e interface de visualização no seu projeto.