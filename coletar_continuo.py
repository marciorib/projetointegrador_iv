
'''isso vai deixar seus dados bem mais úteis para o machine learning depois.
Vamos transformar o coletor em algo contínuo que grava dados a cada X minutos no mesmo CSV, criando um histórico.'''

'''Como funciona

Se conecta à API da SPTrans.

A cada INTERVALO segundos (ex.: 60), pega as posições dos ônibus.

Acrescenta no mesmo arquivo CSV (onibus_linha_8000.csv).

Vai criando um histórico com hora da coleta + posição de cada ônibus.

Você pode interromper a qualquer momento com CTRL+C.'''

import requests
import pandas as pd
from datetime import datetime
import time
import os

# === CONFIGURAÇÕES ===
TOKEN = "SEU_TOKEN_AQUI"   # coloque aqui seu token da SPTrans
NUMERO_LINHA = "8000"      # número da linha de ônibus
INTERVALO = 60             # intervalo em segundos entre coletas (ex: 60s)

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

arquivo_csv = f"onibus_linha_{nome_linha}.csv"
print(f"📍 Coletando dados da linha {nome_linha} (código {codigo_linha})")
print(f"📂 Salvando em {arquivo_csv} a cada {INTERVALO} segundos...\n")

# === LOOP CONTÍNUO ===
while True:
    try:
        posicoes_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao?codigoLinha={codigo_linha}"
        posicoes = session.get(posicoes_url).json()

        if "vs" not in posicoes or not posicoes["vs"]:
            print("⚠️ Nenhum ônibus encontrado agora.")
        else:
            dados = []
            for onibus in posicoes["vs"]:
                dados.append({
                    "prefixo": onibus["p"],
                    "latitude": onibus["py"],
                    "longitude": onibus["px"],
                    "hora_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            df = pd.DataFrame(dados)

            # Se o arquivo já existe, acrescenta os novos dados
            if os.path.exists(arquivo_csv):
                df.to_csv(arquivo_csv, mode="a", header=False, index=False, encoding="utf-8-sig")
            else:
                df.to_csv(arquivo_csv, index=False, encoding="utf-8-sig")

            print(f"✅ {len(df)} ônibus registrados às {datetime.now().strftime('%H:%M:%S')}")

        time.sleep(INTERVALO)

    except KeyboardInterrupt:
        print("\n🛑 Coleta interrompida pelo usuário.")
        break
    except Exception as e:
        print(f"❌ Erro: {e}")
        time.sleep(INTERVALO)
