
#montar um mini protótipo em Python que:
#Autentica na API da SPTrans.
#Busca uma linha de ônibus pelo número.
#Captura a posição em tempo real dos ônibus dessa linha.
#Salva os dados em um CSV para você analisar depois.

# codigo (abaixo)

#O que esse script faz ---------------------------------------------------

#Faz login com seu token da SPTrans.
#Procura a linha de ônibus (exemplo: 8000).
#Pega todos os ônibus em circulação dessa linha, com prefixo, latitude, longitude.
#Marca a hora da coleta.
#Salva em CSV (exemplo: onibus_linha_8000.csv).

#A partir daqui você pode:  ----------------------------------------------------

#Rodar o script várias vezes ao longo do dia e ir acumulando dados.
#Usar esses CSVs para treinar um modelo de ML (previsão de chegada, análise de atrasos, etc.).
#Criar uma interface com Streamlit mostrando os ônibus num mapa interativo.



import requests
import pandas as pd
from datetime import datetime

# === CONFIGURAÇÕES ===
TOKEN = "SUA_CHAVE_AQUI"  # coloque aqui o token que você pega no site da SPTrans
NUMERO_LINHA = "8000"     # exemplo de linha de ônibus

# === AUTENTICAÇÃO ===
session = requests.Session()
auth_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={TOKEN}"
auth_response = session.post(auth_url)

if auth_response.status_code == 200 and auth_response.json() is True:
    print("✅ Autenticado com sucesso!")
else:
    print("❌ Erro na autenticação, verifique seu token.")
    exit()

# === BUSCAR INFORMAÇÕES DA LINHA ===
linha_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca={NUMERO_LINHA}"
linha_data = session.get(linha_url).json()

if not linha_data:
    print("❌ Linha não encontrada.")
    exit()

codigo_linha = linha_data[0]["cl"]  # código interno da linha
nome_linha = linha_data[0]["lt"]    # número da linha
print(f"📍 Linha encontrada: {nome_linha} (código: {codigo_linha})")

# === CAPTURAR POSIÇÃO DOS ÔNIBUS ===
posicoes_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao?codigoLinha={codigo_linha}"
posicoes = session.get(posicoes_url).json()

if "vs" not in posicoes or not posicoes["vs"]:
    print("⚠️ Nenhum ônibus encontrado em operação no momento.")
    exit()

# Criar DataFrame com as informações dos ônibus
dados = []
for onibus in posicoes["vs"]:
    dados.append({
        "prefixo": onibus["p"],    # número do veículo
        "latitude": onibus["py"],
        "longitude": onibus["px"],
        "hora_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

df = pd.DataFrame(dados)

# === SALVAR EM CSV ===
arquivo_csv = f"onibus_linha_{nome_linha}.csv"
df.to_csv(arquivo_csv, index=False, encoding="utf-8-sig")

print(f"✅ Dados salvos em {arquivo_csv}")
print(df.head())
