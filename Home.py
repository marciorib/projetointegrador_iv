import streamlit as st
from datetime import datetime
from pathlib import Path

# ------------------------------
# Configuração da Página
# ------------------------------
st.set_page_config(
    page_title="Apresentação - Projeto Integrador IV",
    page_icon="🚌",
    layout="wide"
)

# ------------------------------
# Diretórios e imagens
# ------------------------------
BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "img"

LOGO_PATH = IMG_DIR / "Univesp_logo_png_rgb.png"
SCREEN_MAP = IMG_DIR / "screenshot_mapa.png"
SCREEN_CHART = IMG_DIR / "screenshot_grafico.png"

# ------------------------------
# Estilo customizado
# ------------------------------
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
        margin-bottom: 20px;
    }
    .tech {
        display: inline-block;
        background: #21c4ff;
        color: black;
        padding: 5px 10px;
        border-radius: 10px;
        margin-right: 5px;
        margin-bottom: 5px;
        font-size: 14px;
        font-weight: 600;
    }
    /* BOTÃO ANIMADO */
    .animated-btn {
        background: linear-gradient(135deg, #21c4ff, #00aaff);
        color: black;
        font-weight: 700;
        padding: 16px 36px;
        border: none;
        border-radius: 12px;
        cursor: pointer;
        font-size: 20px;
        box-shadow: 0px 6px 15px rgba(33,196,255,0.4);
        transition: all 0.3s ease-in-out;
        transform: perspective(500px) translateZ(0);
    }
    .animated-btn:hover {
        transform: perspective(500px) translateZ(10px);
        background: linear-gradient(135deg, #00b3f0, #009fe3);
        box-shadow: 0px 10px 25px rgba(33,196,255,0.6);
    }
    .animated-btn:active {
        transform: perspective(500px) translateZ(3px);
        box-shadow: 0px 4px 10px rgba(33,196,255,0.4);
    }
    .center {
        text-align: center;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# Cabeçalho
# ------------------------------
if LOGO_PATH.exists():
    st.image(str(LOGO_PATH), width=250)
else:
    st.warning("⚠️ Logo não encontrada em: 'img/Univesp_logo_jpg_cmyk-487x287.jpg'")

st.title("🚌 Projeto Integrador IV - Dashboard SPTrans")
st.markdown(f"**Última atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")

st.markdown("---")

# ------------------------------
# Introdução
# ------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📘 Sobre o Projeto")
st.markdown("""
O **Dashboard SPTrans** é uma aplicação interativa desenvolvida no contexto do **Projeto Integrador IV da UNIVESP**,  
com o objetivo de **monitorar, visualizar e analisar dados em tempo real** sobre a frota de ônibus da cidade de São Paulo.  
A ferramenta utiliza dados públicos da SPTrans e tecnologias de visualização para apoiar estudos sobre **mobilidade urbana**  
e **eficiência do transporte público**.
""")
st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------
# Objetivos
# ------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🎯 Objetivos")
st.markdown("""
- Consolidar e exibir dados de localização da frota em tempo real;  
- Permitir análise geográfica interativa de linhas e trajetos;  
- Oferecer indicadores sobre horários e distribuição operacional;  
- Apoiar estudos e decisões relacionadas à mobilidade urbana sustentável.  
""")
st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------
# Tecnologias
# ------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🧰 Tecnologias Utilizadas")
for tech in ["Python", "Streamlit", "Pandas", "Plotly", "Pydeck", "GitHub", "Machine Learning (em desenvolvimento)"]:
    st.markdown(f"<span class='tech'>{tech}</span>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------
# Resultados Preliminares
# ------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📊 Resultados Preliminares")
st.markdown("""
A primeira versão do dashboard apresenta:
- Visualização geográfica da frota em tempo real;  
- Filtros dinâmicos por linha, horário e trajeto;  
- Gráficos interativos sobre a operação diária.  
""")

col1, col2 = st.columns(2)
with col1:
    if SCREEN_MAP.exists():
        st.image(str(SCREEN_MAP), caption="Mapa Interativo - Distribuição da Frota", use_container_width=True)
    else:
        st.info("📍 Imagem 'screenshot_mapa.png' não encontrada na pasta 'img'.")

with col2:
    if SCREEN_CHART.exists():
        st.image(str(SCREEN_CHART), caption="Gráfico de Distribuição por Horário", use_container_width=True)
    else:
        st.info("📊 Imagem 'screenshot_grafico.png' não encontrada na pasta 'img'.")
st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------
# Equipe
# ------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("👥 Equipe do Projeto")
st.markdown("""
**Turma:** 01 – **Grupo:** 07  
**Orientador:** Prof. Vinícius Marcelo Pereira  

**Integrantes:**  
- ALEX DE ALMEIDA CRUZ, 2208970
- BÁRBARA HAYDEE PRESENTE, 2214684
- CARLOS ALBERTO MORAL JUNIOR, 2203786
- ELIANA APARECIDA RIBEIRO BUDIN, 2208956
- MARCIO ANTONIO RIBEIRO, 226928
- ROGERIO LEONEL DOS SANTOS, 2220619
- SERGIO LUIZ AUGUSTO DIAS, 2203760
  
""")
st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------
# BOTÃO ANIMADO - ACESSAR DASHBOARD
# ------------------------------
st.markdown('<div class="card center">', unsafe_allow_html=True)
st.subheader("🌐 Acesse o Dashboard Interativo")

if st.button("🚀 Acessar o Dashboard", key="btn_dashboard"):
    js = "window.location.href = '/dashboardapp';"
    st.markdown(f"<script>{js}</script>", unsafe_allow_html=True)

st.markdown("""
<p style="color:#bbbbbb;">
💡 <b>Dica:</b> Caso o botão não redirecione automaticamente,  
use o <b>menu lateral</b> e selecione  
<b>📊 Dashboard SPTrans - Ônibus em Tempo Real</b>.
</p>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
