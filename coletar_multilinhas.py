
'''Diferenças principais

você pode definir várias linhas na lista LINHAS = ["8000", "7013", "4112"].

Todos os registros vão para um único CSV chamado onibus_multilinhas.csv.

O arquivo terá uma coluna extra "linha" para identificar de qual linha o ônibus é.'''

'''Exemplo de saida no CSV

linha,prefixo,latitude,longitude,hora_coleta
8000,12345,-23.56,-46.64,2025-08-26 21:15:00
7013,23456,-23.54,-46.62,2025-08-26 21:15:00
4112,34567,-23.55,-46.60,2025-08-26 21:15:00
'''

'''import requests
import pandas as pd
from datetime import datetime
import time
import os

# === CONFIGURAÇÕES ===
TOKEN = "1cf54ff69bbdf159a0ce16af8a6cdc3d4428075aa741862514aab4ea0c92c4df"   # coloque aqui seu token da SPTrans
LINHAS = ["8000", "7013", "4112"]   # lista das linhas que você quer monitorar
INTERVALO = 60             # intervalo em segundos entre coletas

# === AUTENTICAÇÃO ===
session = requests.Session()
auth_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={TOKEN}"
auth_response = session.post(auth_url)

if auth_response.status_code == 200 and auth_response.json() is True:
    print("✅ Autenticado com sucesso!")
else:
    print("❌ Erro na autenticação.")
    exit()

arquivo_csv = "onibus_multilinhas.csv"
print(f"📍 Coletando dados das linhas {', '.join(LINHAS)}")
print(f"📂 Salvando em {arquivo_csv} a cada {INTERVALO} segundos...\n")

# === LOOP CONTÍNUO ===
while True:
    try:
        registros = []

        for numero_linha in LINHAS:
            # buscar código da linha
            linha_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca={numero_linha}"
            linha_data = session.get(linha_url).json()

            if not linha_data:
                print(f"❌ Linha {numero_linha} não encontrada.")
                continue

            codigo_linha = linha_data[0]["cl"]
            nome_linha = linha_data[0]["lt"]

            # buscar posições em tempo real
            posicoes_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao?codigoLinha={codigo_linha}"
            posicoes = session.get(posicoes_url).json()

            if "vs" not in posicoes or not posicoes["vs"]:
                print(f"⚠️ Nenhum ônibus encontrado para a linha {nome_linha}.")
                continue

            for onibus in posicoes["vs"]:
                registros.append({
                    "linha": nome_linha,
                    "prefixo": onibus["p"],
                    "latitude": onibus["py"],
                    "longitude": onibus["px"],
                    "hora_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        if registros:
            df = pd.DataFrame(registros)

            # Se o arquivo já existe, acrescenta os novos dados
            if os.path.exists(arquivo_csv):
                df.to_csv(arquivo_csv, mode="a", header=False, index=False, encoding="utf-8-sig")
            else:
                df.to_csv(arquivo_csv, index=False, encoding="utf-8-sig")

            print(f"✅ {len(df)} registros salvos às {datetime.now().strftime('%H:%M:%S')}")

        else:
            print("⚠️ Nenhum ônibus ativo em nenhuma linha agora.")

        time.sleep(INTERVALO)

    except KeyboardInterrupt:
        print("\n🛑 Coleta interrompida pelo usuário.")
        break
    except Exception as e:
        print(f"❌ Erro: {e}")
        time.sleep(INTERVALO)'''




'''Então vamos montar o coletor contínuo de múltiplas linhas que garante a criação do CSV.'''


'''
import requests
import pandas as pd
from datetime import datetime
import time
import os

# === CONFIGURAÇÕES ===
TOKEN = "1cf54ff69bbdf159a0ce16af8a6cdc3d4428075aa741862514aab4ea0c92c4df"   # substitua pelo seu token
LINHAS = ["178T-10", "6262-10", "8038-10", "846M-10", "809H-10", "809T-10", "N832-11", "N838-11", "847J-10", "957T-10", "957T-10", "8060-10", "178T-10", "846M-10", "958P-10", "6262-10", "7282-10", "N833-11", "917H-10", "875P-10", "7013-10"]   # adicione as linhas que quiser
INTERVALO = 60             # tempo em segundos entre coletas
ARQUIVO_CSV = "onibus_multilinhas.csv"

# === AUTENTICAÇÃO ===
session = requests.Session()
auth_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={TOKEN}"
auth_response = session.post(auth_url)

if auth_response.status_code == 200 and auth_response.json() is True:
    print("✅ Autenticado com sucesso!")
else:
    print("❌ Erro na autenticação. Verifique seu token.")
    exit()

print(f"📍 Coletando dados das linhas: {', '.join(LINHAS)}")
print(f"📂 Salvando em {ARQUIVO_CSV} a cada {INTERVALO} segundos...\n")

# === LOOP DE COLETA ===
while True:
    try:
        registros = []

        for numero_linha in LINHAS:
            # Buscar dados da linha
            linha_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca={numero_linha}"
            linha_data = session.get(linha_url).json()

            if not linha_data:
                print(f"❌ Linha {numero_linha} não encontrada.")
                continue

            codigo_linha = linha_data[0]["cl"]
            nome_linha = linha_data[0]["lt"]

            # Buscar posições em tempo real
            posicoes_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Posicao?codigoLinha={codigo_linha}"
            posicoes = session.get(posicoes_url).json()

            if "vs" not in posicoes or not posicoes["vs"]:
                print(f"⚠️ Nenhum ônibus ativo na linha {nome_linha}.")
                continue

            for onibus in posicoes["vs"]:
                registros.append({
                    "linha": nome_linha,
                    "prefixo": onibus["p"],
                    "latitude": onibus["py"],
                    "longitude": onibus["px"],
                    "hora_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        if registros:
            df = pd.DataFrame(registros)

            # Se o arquivo já existe, acrescenta dados; se não, cria
            if os.path.exists(ARQUIVO_CSV):
                df.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False, encoding="utf-8-sig")
            else:
                df.to_csv(ARQUIVO_CSV, index=False, encoding="utf-8-sig")

            print(f"✅ {len(df)} registros salvos às {datetime.now().strftime('%H:%M:%S')}")
        else:
            print("⚠️ Nenhum registro encontrado em nenhuma linha agora.")

        time.sleep(INTERVALO)

    except KeyboardInterrupt:
        print("\n🛑 Coleta interrompida pelo usuário.")
        break
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        time.sleep(INTERVALO)

'''

'''O que esse script faz

Autentica na API SPTrans.

A cada minuto (INTERVALO = 60), baixa todos os ônibus ativos em SP.

Salva no CSV onibus_todos.csv com os campos:


codigo_linha,id_linha,sentido,prefixo,latitude,longitude,hora_coleta
Mantém rodando até você parar com CTRL+C.

'''
import requests
import pandas as pd
from datetime import datetime
import time
import os

# === CONFIGURAÇÕES ===
TOKEN = "1cf54ff69bbdf159a0ce16af8a6cdc3d4428075aa741862514aab4ea0c92c4df"  # Coloque aqui o token fornecido pela sptrans
INTERVALO = 60            # tempo em segundos entre coletas
ARQUIVO_CSV = "onibus_todos.csv"  # onibus pra caceta, analisar intervalo

# === AUTENTICAÇÃO ===
session = requests.Session()
auth_url = f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={TOKEN}"
auth_response = session.post(auth_url)

if auth_response.status_code == 200 and auth_response.json() is True:
    print("✅ Autenticado com sucesso!")
else:
    print("❌ Erro na autenticação. Verifique seu token.")
    exit()

print(f"📍 Coletando dados de TODOS os ônibus em circulação em SP")
print(f"📂 Salvando em {ARQUIVO_CSV} a cada {INTERVALO} segundos...\n")

# === LOOP DE COLETA ===
while True:
    try:
        registros = []

        # Endpoint de todos os ônibus ativos
        posicoes_url = "http://api.olhovivo.sptrans.com.br/v2.1/Posicao"
        posicoes = session.get(posicoes_url).json()

        if "l" not in posicoes or not posicoes["l"]:
            print("⚠️ Nenhum ônibus encontrado agora.")
        else:
            for linha in posicoes["l"]:
                codigo_linha = linha["c"]
                nome_linha = linha["cl"]
                sentido_ida = linha["sl"]

                for onibus in linha["vs"]:
                    registros.append({
                        "codigo_linha": codigo_linha,
                        "id_linha": nome_linha,
                        "sentido": sentido_ida,
                        "prefixo": onibus["p"],
                        "latitude": onibus["py"],
                        "longitude": onibus["px"],
                        "hora_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })

            df = pd.DataFrame(registros)

            # Se o arquivo já existe, acrescenta dados; se não, cria
            if os.path.exists(ARQUIVO_CSV):
                df.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False, encoding="utf-8-sig")
            else:
                df.to_csv(ARQUIVO_CSV, index=False, encoding="utf-8-sig")

            print(f"✅ {len(df)} registros salvos às {datetime.now().strftime('%H:%M:%S')}")

        time.sleep(INTERVALO)

    except KeyboardInterrupt:
        print("\n🛑 Coleta interrompida pelo usuário.")
        break
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        time.sleep(INTERVALO)
