
'''Você tem 2 scripts separados:

aprendizagem_maquina.py  -  coletar_onibus.py → coleta da API da SPTrans e salva em CSV
(esse é o script que autentica, pega posições e cria onibus_linha_8000.csv)

tempchegbus.py → análise e previsão (ML)
(esse é o script que lê o CSV já existente e treina o modelo)

para rodar python tempchegbus.py aprendizagem_maquina.py
'''


'''Ideia do modelo

Você coleta dados da API (ônibus em circulação + horário).
Gera features como: horário do dia, dia da semana, latitude, longitude.
A variável alvo pode ser, por exemplo, o tempo de chegada em um ponto específico.
Como você ainda não coletou dados suficientes, vou simular com uma lógica simples para mostrar como montar o pipeline.
'''








import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# === Simulação de dados coletados (devemos substituir pelo CSV real da API) ===
# Suponha que nós salvamos os dados de ônibus passando em um ponto específico
np.random.seed(42)
n = 300

df = pd.DataFrame({
    "latitude": -23.55 + np.random.normal(0, 0.01, n),
    "longitude": -46.63 + np.random.normal(0, 0.01, n),
    "hora_dia": np.random.randint(0, 24, n),   # hora do dia
    "dia_semana": np.random.randint(0, 7, n),  # 0=Segunda ... 6=Domingo
    "tempo_chegada_min": np.random.randint(2, 30, n) # alvo (rótulo)
})

print("Exemplo de dataset:")
print(df.head())

# === Separar features (X) e target (y) ===
X = df[["latitude", "longitude", "hora_dia", "dia_semana"]]
y = df["tempo_chegada_min"]

# === Treinar/Testar ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = LinearRegression()
modelo.fit(X_train, y_train)

# === Avaliar ===
y_pred = modelo.predict(X_test)

print("\n📊 Resultados do modelo:")
print(f"MAE (erro absoluto médio): {mean_absolute_error(y_test, y_pred):.2f} minutos")
print(f"R² (qualidade do ajuste): {r2_score(y_test, y_pred):.2f}")

# === Testar previsão ===
amostra = pd.DataFrame({
    "latitude": [-23.55],
    "longitude": [-46.63],
    "hora_dia": [8],
    "dia_semana": [2]  # quarta-feira
})

previsao = modelo.predict(amostra)[0]
print(f"\n🚌 Tempo estimado de chegada: {previsao:.1f} minutos")




'''O que esse código faz

Cria (ou usa seu CSV) com dados coletados de ônibus.
Extrai variáveis explicativas (features) como posição e horário.
Treina um modelo de regressão linear.
Mede o erro (MAE) e a qualidade do modelo (R²).
Faz uma previsão simulada para horário/posição específicos.'''


'''Como aplicar com seus dados reais

Rodar o script de coleta da SPTrans várias vezes ao longo do dia.
Salvar os dados em CSV (com latitude, longitude, hora_coleta, prefixo, etc.).
Definir um ponto fixo (ex: terminal ou parada) e calcular o tempo até o ônibus chegar lá.
Usar esse tempo como variável alvo (y) no modelo.'''