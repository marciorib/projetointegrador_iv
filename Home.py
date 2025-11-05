import streamlit as st
from pathlib import Path
import os
from PIL import Image

# ------------------------------
# Configurações da página
# ------------------------------
st.set_page_config(
    page_title="Dashboard SPTrans - UNIVESP",
    layout="wide",
    page_icon="🚌"
)

# ------------------------------
# CSS personalizado
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
p {
    font-size: 18px;
}
.stButton>button {
    background-color: #21c4ff;
    color: black;
    font-weight: 600;
    border-radius: 10px;
    padding: 0.6em 1.2em;
}
.stButton>button:hover {
    background-color: #15a7db;
    color: white;
}
img {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Diretórios e imagens
# ------------------------------
BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "img"

LOGO_PATH = IMG_DIR / "Univesp_logo_png_rgb.png"
SCREEN_MAP = IMG_DIR / "screenshot_mapa.png"
SCREEN_CHART = IMG_DIR / "screenshot_grafico.png"

# ------------------------------
# Função de exibição segura de imagem
# ------------------------------
def mostrar_imagem_segura(caminho, legenda):
    """Exibe imagem se existir, caso contrário mostra aviso elegante."""
    if os.path.exists(caminho):
        st.image(str(caminho), caption=legenda, use_container_width=True)
    else:
        st.warning(f"⚠️ Imagem '{Path(caminho).name}' não encontrada na pasta 'img'.")

# ------------------------------
# Cabeçalho da Home
# ------------------------------
col1, col2 = st.columns([1, 4])

with col1:
    if os.path.exists(LOGO_PATH):
        st.image(str(LOGO_PATH), width=150)
    else:
        st.warning("⚠️ Logotipo da UNIVESP não encontrado.")

with col2:
    st.title("🚌 Dashboard SPTrans - Projeto Integrador IV")
    st.markdown("### _Análise e Visualização de Dados do Transporte Público Urbano de São Paulo_")

st.markdown("---")

# ------------------------------
# Descrição do projeto
# ------------------------------
st.markdown("""
## 🎯 Objetivo do Projeto
O **Dashboard SPTrans** tem como finalidade analisar e visualizar dados do transporte público urbano
de São Paulo em tempo real, utilizando **Ciência de Dados**, **Machine Learning** e **Visualização Interativa**.

A plataforma foi desenvolvida com **Python + Streamlit**, permitindo que usuários explorem:
- A localização e movimentação dos ônibus;
- Linhas em operação e seus trajetos;
- Previsões de quantidade de veículos ativos por hora (via Aprendizado de Máquina);
- Simulação temporal da movimentação ao longo do dia.
""")

# ------------------------------
# Imagens principais
# ------------------------------
st.markdown("---")
st.markdown("## 🗺️ Visualização do Mapa Interativo")
mostrar_imagem_segura(SCREEN_MAP, "Mapa Interativo - Distribuição da Frota")

st.markdown("## 📊 Gráfico de Distribuição de Ônibus")
mostrar_imagem_segura(SCREEN_CHART, "Gráfico - Distribuição de Ônibus ao Longo do Dia")

st.markdown("---")

# ------------------------------
# Botão para acessar o Dashboard
# ------------------------------
st.markdown("## 🚀 Acesse o Dashboard Completo")

if st.button("Acessar Dashboard SPTrans"):
    js = "window.open('http://localhost:8501/dashboard_SPTrans', '_self')"
    st.markdown(f"<script>{js}</script>", unsafe_allow_html=True)

st.info("🔹 Clique no botão acima para abrir o Dashboard principal.")

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
