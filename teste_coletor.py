import requests
import pandas as pd
from datetime import datetime

TOKEN = "1cf54ff69bbdf159a0ce16af8a6cdc3d4428075aa741862514aab4ea0c92c4df"   # coloque seu token
NUMERO_LINHA = "8000"

session = requests.Session()
auth_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={TOKEN}"
if session.post(auth_url).json() is not True:
    print("❌ Erro na autenticação")
    exit()

linha_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca={NUMERO_LINHA}"
linha_data = session.get(linha_url).json()
codigo_linha = linha_data[0]["cl"]

posicoes_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao?codigoLinha={codigo_linha}"
posicoes = session.get(posicoes_url).json()

if "vs" not in posicoes or not posicoes["vs"]:
    print("⚠️ Nenhum ônibus encontrado")
else:
    dados = [{"prefixo": o["p"], "lat": o["py"], "lon": o["px"], "hora": datetime.now()} for o in posicoes["vs"]]
    df = pd.DataFrame(dados)
    df.to_csv(f"onibus_linha_{NUMERO_LINHA}.csv", index=False)
    print("✅ CSV criado com sucesso!")
    print(df)
