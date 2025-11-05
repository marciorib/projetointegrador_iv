# 

'''aproveitando aquele script que já temos que coleta posições de ônibus e salva em CSV e adaptá-lo para treinar um modelo simples.

⚠️ Importante: os dados que temos atualmente (prefixo, latitude, longitude, hora_coleta) ainda não incluem o tempo até chegar em uma parada (que seria a variável alvo do modelo).
Pra demonstrar o pipeline de ML, vamos simular esse tempo_chegada_min a partir do horário (pra vermos funcionando). Depois, quando enriquecer o CSV 
(por exemplo com API /Previsao da SPTrans), basta substituir essa coluna simulada.

'''



import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# === Ler o CSV salvo com os dados dos ônibus ===
arquivo_csv = "onibus_linha_8000.csv"  # altere para o nome do seu arquivo
df = pd.read_csv(arquivo_csv)

print("📂 Dados carregados do CSV:")
print(df.head())

# === Pré-processamento ===
# Extrair hora e dia da semana da coluna "hora_coleta"
df["hora_coleta"] = pd.to_datetime(df["hora_coleta"])
df["hora_dia"] = df["hora_coleta"].dt.hour
df["dia_semana"] = df["hora_coleta"].dt.dayofweek  # 0=Segunda ... 6=Domingo

# ⚠️ Simulação: vamos criar uma coluna "tempo_chegada_min" só para testar ML
# No seu caso, substitua isso pelo campo real da API /Previsao
df["tempo_chegada_min"] = np.random.randint(2, 30, size=len(df))

# === Features (X) e Target (y) ===
X = df[["latitude", "longitude", "hora_dia", "dia_semana"]]
y = df["tempo_chegada_min"]

# === Separar treino/teste ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === Treinar modelo ===
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# === Avaliar ===
y_pred = modelo.predict(X_test)

print("\n📊 Resultados do modelo:")
print(f"MAE (erro absoluto médio): {mean_absolute_error(y_test, y_pred):.2f} minutos")
print(f"R² (qualidade do ajuste): {r2_score(y_test, y_pred):.2f}")

# === Fazer uma previsão simulada ===
amostra = pd.DataFrame({
    "latitude": [df.iloc[0]["latitude"]],
    "longitude": [df.iloc[0]["longitude"]],
    "hora_dia": [df.iloc[0]["hora_dia"]],
    "dia_semana": [df.iloc[0]["dia_semana"]]
})

previsao = modelo.predict(amostra)[0]
print(f"\n🚌 Tempo estimado de chegada (simulado): {previsao:.1f} minutos")



'''Como fica o fluxo

Você roda o coletor e salva os dados em CSV.

Este script lê o CSV, processa o campo hora_coleta.

Adiciona (por enquanto) um tempo_chegada_min simulado.

Treina e avalia o modelo.

Faz uma previsão de chegada. belê?'''