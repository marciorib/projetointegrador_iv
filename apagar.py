import pandas as pd

df = pd.read_csv("onibus_todos.csv", nrows=5)  # pega só as 5 primeiras linhas
print(df.columns)
