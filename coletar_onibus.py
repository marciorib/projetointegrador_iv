import requests
import pandas as pd
from datetime import datetime

# === CONFIGURAÇÕES ===
TOKEN = "1cf54ff69bbdf159a0ce16af8a6cdc3d4428075aa741862514aab4ea0c92c4df"   # seu token válido
NUMERO_LINHA = "8000"      # troque pela linha que quiser

# === AUTENTICAÇÃO ===
session = requests.Session()
auth_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={TOKEN}"
auth_response = session.post(auth_url)

if auth_response.status_code == 200 and auth_response.json() is True:
    print("✅ Autenticado com sucesso!")
else:
    print("❌ Erro na autenticação.")
    exit()

# === BUSCAR CÓDIGO DA LINHA ===
linha_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca={NUMERO_LINHA}"
linha_data = session.get(linha_url).json()

if not linha_data:
    print("❌ Linha não encontrada.")
    exit()

codigo_linha = linha_data[0]["cl"]
nome_linha = linha_data[0]["lt"]

print(f"📍 Linha encontrada: {nome_linha} (código: {codigo_linha})")

# === PEGAR POSIÇÕES ===
posicoes_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao?codigoLinha={codigo_linha}"
posicoes = session.get(posicoes_url).json()

if "vs" not in posicoes or not posicoes["vs"]:
    print("⚠️ Nenhum ônibus encontrado agora.")
    exit()

dados = []
for onibus in posicoes["vs"]:
    dados.append({
        "prefixo": onibus["p"],
        "latitude": onibus["py"],
        "longitude": onibus["px"],
        "hora_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

df = pd.DataFrame(dados)

# === SALVAR CSV ===
arquivo_csv = f"onibus_linha_{nome_linha}.csv"
df.to_csv(arquivo_csv, index=False, encoding="utf-8-sig")

print(f"✅ Dados salvos em {arquivo_csv}")
print(df.head())
