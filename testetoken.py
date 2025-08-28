

import requests

TOKEN = "1cf54ff69bbdf159a0ce16af8a6cdc3d4428075aa741862514aab4ea0c92c4df"  # substitua pelo seu token atual

session = requests.Session()
url = f"http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token={TOKEN}"

res = session.post(url)
print("Status code:", res.status_code)
print("Resposta:", res.text)
