# projetointegrador_iv
# 📊 Dashboard SPTrans - Projeto Integrador IV

Este projeto apresenta um **dashboard interativo** desenvolvido em **Python + Streamlit** para visualização em tempo real dos ônibus de São Paulo (SPTrans).

## 🚀 Funcionalidades

- **Filtros interativos** na barra lateral:
  - Seleção de **linhas**.
  - Seleção de **ônibus individuais (prefixos)**.
  - Checkbox para **mostrar ou ocultar trajetos**.
  - **Slider temporal** para escolher a hora do dia e ver apenas os ônibus daquele período.
- **Mapa interativo** com PyDeck:
  - Pontos dos ônibus em cores diferentes por linha.
  - Destaque em **amarelo** para prefixos selecionados.
  - Trajetos em **azul** quando ativado na sidebar.
- **Estatísticas principais**:
  - Total de ônibus ativos.
  - Quantidade de linhas selecionadas.
  - Última coleta registrada.
- **Gráfico por horário** (Plotly):
  - Distribuição dos ônibus ao longo do dia.
- **Tabela interativa** com AgGrid (em breve será adicionada).

---

## 🛠️ Tecnologias utilizadas

- [Python 3.11+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [PyDeck](https://deckgl.readthedocs.io/)
- [Plotly Express](https://plotly.com/python/plotly-express/)
- [st-aggrid](https://pypi.org/project/streamlit-aggrid/)

---

## 📂 Estrutura do projeto

- **projetointegrador_iv/**:
│── dashboardapp.py # Código principal do dashboard

│── onibus_todos.csv # Base de dados com posições dos ônibus

│── README.md # Este arquivo

---

## ▶️ Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/marciorib/projetointegrador_iv.git
   cd projetointegrador_iv

2. Crie um ambiente virtual
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac

3. Instale as dependencias
pip install -r requirements.txt

4. Execute o dashboardapp:
streamlit run dashboardapp.py

5. Acesse no navegador
http://localhost:8501

---

📌 Próximos passos  12/09/2025

Implementar animação temporal (play/pause) para simular movimentação dos ônibus ao longo do dia.

Melhorar a tabela interativa com AgGrid (filtros e ordenação).

Publicar o dashboard online via Streamlit Cloud ou Railway.
