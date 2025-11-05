# Dashboard SPTrans - Resumo

## 1. Erro identificado

* `AttributeError: 'str' object has no attribute 'strftime'` na métrica "Última coleta".
* O problema ocorre porque `ultima_coleta` pode ser uma string, mas `.strftime()` só funciona com objetos datetime.

## 2. Correção aplicada

* Criada a função `formatar_data_segura(data)`:

  * Converte strings para datetime quando possível.
  * Formata datas como `"%d/%m/%Y %H:%M:%S"`.
  * Retorna `"N/A"` para valores nulos.
  * Mantém strings que não podem ser convertidas.
* A métrica de "Última coleta" foi substituída por `col3.metric("Última coleta", formatar_data_segura(ultima_coleta))`.

## 3. Código atualizado (trecho principal)

```python
# Última coleta formatada
ultima_coleta = df_filtrado["hora_coleta"].max()
col3.metric("Última coleta", formatar_data_segura(ultima_coleta))

# Função de formatação segura
def formatar_data_segura(data):
    if pd.isnull(data):
        return "N/A"
    if isinstance(data, str):
        try:
            data = pd.to_datetime(data)
        except Exception:
            return data
    if isinstance(data, (pd.Timestamp, datetime)):
        return data.strftime("%d/%m/%Y %H:%M:%S")
    return str(data)
```

## 4. Próximos passos

* Testar o dashboard com diferentes CSVs.
* Atualizar o repositório no GitHub.
* Opcional: refatorar o dashboard para aplicar formatação segura em todas as métricas e gráficos.
