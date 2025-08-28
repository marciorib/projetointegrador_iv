import requests

# Seu token da SPTrans
TOKEN = "1cf54ff69bbdf159a0ce16af8a6cdc3d4428075aa741862514aab4ea0c92c4df"

# URL de autenticação
url = f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={TOKEN}"

# Faz a requisição
response = requests.post(url)

# Mostra o resultado
if response.status_code == 200:
    if response.json() is True:
        print("✅ Autenticado com sucesso! Seu token está válido.")
    else:
        print("⚠️ Requisição feita, mas não autenticou. Verifique o token.")
else:
    print(f"❌ Erro na conexão. Status code: {response.status_code}")
