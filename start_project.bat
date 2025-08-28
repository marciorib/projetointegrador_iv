

echo script automatizador para rodar a coleta em segundo plano enquanto você abre o dashboard. Assim você terá sempre dados fresquinhos no onibus_todos.csv enquanto visualiza no navegador.

echo Dê um duplo clique nele → ele vai abrir dois terminais:
echo Um rodando o coletor (alimentando o CSV).
echo Outro com o dashboard no navegador (http://localhost:8501).


@echo off
echo ==============================
echo 🚍 Iniciando Projeto SPTrans
echo ==============================

:: Ativa o ambiente virtual, se existir
if exist venv (
    call venv\Scripts\activate
)

:: Inicia o coletor em segundo plano
start cmd /k "python coletar_multilinhas.py"

:: Aguarda 5 segundos para começar a coleta
timeout /t 5 > nul

:: Inicia o dashboard
streamlit run dashboard.py
