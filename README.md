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

Este projeto foi desenvolvido como parte do **Projeto Integrador IV da UNIVESP** e tem como objetivo **analisar e visualizar dados do transporte público urbano de São Paulo** usando **Ciência de Dados**, **Aprendizado de Máquina** e **Dashboards Interativos**.

A aplicação foi construída em **Python + Streamlit**, permitindo explorar de forma intuitiva:

✅ Localização e movimentação dos ônibus;  
✅ Linhas em operação e seus trajetos;  
✅ Previsão da quantidade de veículos ativos por hora (via *Machine Learning*).

---

## 🚀 **Principais Funcionalidades**

| Função | Descrição |
|--------|------------|
| 🗺️ **Mapa Interativo** | Visualização em tempo real da frota, com filtros por linha e horário |
| ⏯️ **Animação Temporal** | Simula a movimentação dos ônibus ao longo do dia (play/pause) |
| 🤖 **Previsão de Demanda** | Modelo de regressão linear estima a quantidade de ônibus ativos |
| 📊 **Gráficos Interativos** | Visualização de padrões de operação com Plotly |
| 💡 **Interface Multi-Página** | Navegação entre “Home”, “Dashboard” e “Previsão” |

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
```bash
git clone https://github.com/marciorib/projetointegrador_iv.git
cd projetointegrador_iv

---
##Criar ambiente Visual

python -m venv venv
venv\Scripts\activate

##Instalar dependências

pip install -r requirements.txt

##Executar o sistema
---

streamlit run Home.py
➡️ Acesse no navegador: http://localhost:8501







---
## 🗂️ **Estrutura do Projeto**

projetointegrador_iv/
│
├── Home.py                         # Página inicial
├── dashboardapp.py                 # Versão anterior (histórico)
├── pages/
│   ├── 1_Dashboard_SPTrans.py      # Mapa interativo e controle temporal
│   ├── 2_Previsao_SPTrans.py       # Página de previsão com IA
│
├── onibus_todos.csv                # Base de dados SPTrans
├── requirements.txt                # Dependências do projeto
├── img/
│   └── Univesp_logo_jpg_cmyk-487x287.jpg
├── Relatorio_Final_PI-IV_Grupo07.docx
└── README.md

---

##🤖 **Modelo de Machine Learning**

O projeto implementa um modelo de Regressão Linear com o pacote scikit-learn para prever o número de ônibus ativos por hora.

Etapas:

Leitura e preparação dos dados (hora_coleta, codigo_linha);

Treinamento e validação do modelo;

Avaliação por métricas (MAE e R²);

Exibição dos resultados em gráficos interativos.

📈 O modelo demonstrou bom desempenho, capturando os horários de pico e reduzida atividade da frota.

## 📊 Resultados

Dashboard funcional e responsivo.

Previsões coerentes com horários de maior e menor fluxo.

Visualização temporal com animação e gráficos interativos.

<div align="center">

---

📸 **Capturas de Tela (adicione suas imagens na pasta /img)**
Tela	Descrição

	Página inicial do sistema

	Mapa interativo com animação temporal

	Gráfico de previsão de atividade dos ônibus
</div>

---

##👨‍💻 **Equipe de Desenvolvimento**

👥 Grupo 07 – Turma 01 – Polo Bauru
👨‍🏫 Orientador: Prof. Vinício Marcelo Pereira
🏫 Universidade Virtual do Estado de São Paulo – UNIVESP

---

##📚 **Referências**

SPTRANS – Dados Abertos

Streamlit – Build data apps in Python

Scikit-learn – Machine Learning in Python

Pandas – Data Analysis Library

## 🪪 Licença

Este projeto é de uso acadêmico e foi desenvolvido exclusivamente para fins educacionais no contexto do
Projeto Integrador IV – UNIVESP (2025).
Todos os direitos reservados aos autores.

<div align="center">

✨ Desenvolvido com 💙 por alunos da UNIVESP
📍 Engenharia de Computação & Ciência de Dados – Turma 01 (2025)



</div> ```