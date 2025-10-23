
<div align="center">

# 🚌 **Dashboard SPTrans**  
### _Análise e Visualização de Dados do Transporte Público Urbano de São Paulo_  

📍 **UNIVESP – Projeto Integrador IV – Turma 01 - Grupo 07**  
💻 **Curso:** Engenharia de Computação e Ciência de Dados  
🏫 **Polo:** Bauru  
👨‍🏫 **Tutor:** Vinício Marcelo Pereira  
📅 **Ano:** 2025  

---

</div>

## 🧩 **Descrição do Projeto**

O **Dashboard SPTrans** foi desenvolvido como parte do **Projeto Integrador IV da UNIVESP**, com o objetivo de **analisar, visualizar e prever a movimentação da frota de ônibus da cidade de São Paulo**.  

A solução aplica conceitos de **Ciência de Dados**, **Aprendizado de Máquina** e **Visualização Interativa**, permitindo ao usuário explorar a operação do transporte público em tempo real e prever o comportamento da frota em diferentes horários do dia.

A aplicação foi construída em **Python + Streamlit**, oferecendo uma experiência visual simples e dinâmica.

---

## 🚀 **Principais Funcionalidades**

| Função | Descrição |
|--------|------------|
| 🗺️ **Mapa Interativo** | Visualização em tempo real da frota, com filtros por linha e hora. Mostra trajetos apenas quando uma linha é selecionada. |
| ⏯️ **Animação Temporal (em desenvolvimento)** | Recurso previsto para simular a movimentação dos ônibus ao longo do dia. |
| 🤖 **Previsão de Demanda** | Modelo de Regressão Linear estima a quantidade de ônibus ativos por hora. |
| 📊 **Gráficos Interativos** | Análises e comparações com o uso de gráficos dinâmicos (Plotly). |
| 💡 **Interface Multi-Página** | Navegação entre **Home**, **Dashboard** e **Previsão**. |

---

## 🧠 **Tecnologias Utilizadas**

| Categoria | Ferramenta |
|------------|------------|
| 💻 Linguagem | Python 3.11 |
| 🌐 Framework Web | Streamlit |
| 📊 Análise de Dados | Pandas, NumPy |
| 🎨 Visualização | Plotly, PyDeck |
| 🤖 Machine Learning | Scikit-learn |
| 🧰 Outras | Matplotlib, CSS |
| 🔄 Versionamento | Git e GitHub |

---

## ⚙️ **Como Executar o Projeto**

### 1️⃣ Clonar o repositório

bash
git clone https://github.com/marciorib/projetointegrador_iv.git
cd projetointegrador_iv
2️⃣ Criar o ambiente virtual (opcional)
bash
Copiar código
python -m venv venv
venv\Scripts\activate
3️⃣ Instalar as dependências
bash
Copiar código
pip install -r requirements.txt
4️⃣ Executar o sistema
bash
Copiar código
streamlit run Home.py
➡️ Acesse no navegador: http://localhost:8501

## 🗂️ **Estrutura do Projeto**


projetointegrador_iv/
│
├── Home.py                         # Página inicial do sistema
├── pages/
│   ├── 1_Dashboard_SPTrans.py      # Mapa interativo e métricas principais
│   ├── 2_Previsao_SPTrans.py       # Módulo de Machine Learning
│
├── onibus_todos.csv                # Base de dados com coletas SPTrans
├── requirements.txt                # Dependências do projeto
├── img/
│   ├── Univesp_logo_png_rgb.png
│   ├── screenshot_home.jpg
│   ├── screenshot_mapa.png
│   ├── screenshot_grafico.png
│   ├── screenshot_previsao.jpg
│
├── Relatorio_Final_PI-IV_Grupo07.docx
└── README.md


## 🗺️ **Módulo: Dashboard Interativo**
O Dashboard SPTrans utiliza o pacote PyDeck para renderizar um mapa dinâmico de São Paulo, com marcadores que representam a posição dos ônibus coletados.

Recursos principais:

Filtros de seleção por linha (menu expansível)
Visualização de trajetos apenas quando uma única linha é escolhida
Métricas de operação atualizadas automaticamente
Gráfico temporal com distribuição de veículos por hora

Exemplo visual:


Mapa interativo mostrando a frota e trajetos das linhas selecionadas.

## 🤖 **Módulo: Previsão com Machine Learning**
O módulo de previsão aplica Regressão Linear (Scikit-learn) para estimar a quantidade de ônibus ativos por hora.
A base de dados é processada e o modelo é avaliado por métricas MAE e R².

Etapas do modelo:

- Preparação dos dados (hora_coleta, quantidade)
- Treinamento e validação
- Avaliação das métricas
- Visualização da curva preditiva e previsão interativa

Exemplo:


Previsão de atividade da frota ao longo do dia – Regressão Linear.

## 📈 **Resultados Obtidos**
Dashboard funcional e responsivo, compatível com tema escuro.

Visualização em mapa e gráficos de fácil interpretação.

Previsões coerentes com horários de pico e menor atividade da frota.

Layout institucional com identidade visual da UNIVESP.

👨‍💻 Equipe de Desenvolvimento
👥 Grupo 07 – Turma 01 – Polo Bauru
👨‍🏫 Orientador: Prof. Vinício Marcelo Pereira
🏫 Universidade Virtual do Estado de São Paulo – UNIVESP

## 📚 **Referências**
SPTRANS – Dados Abertos

Streamlit – Build Data Apps in Python

Scikit-learn – Machine Learning in Python

Pandas – Data Analysis Library

PyDeck – WebGL-powered maps

## 🪪 **Licença**
Este projeto é de uso acadêmico e foi desenvolvido exclusivamente para fins educacionais no contexto do
Projeto Integrador IV – UNIVESP (2025).
Todos os direitos reservados aos autores.

<div align="center">
✨ Desenvolvido com 💙 por alunos da UNIVESP
📍 Engenharia de Computação & Ciência de Dados – Turma 01 (2025)

</div>
