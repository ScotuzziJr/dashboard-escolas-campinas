import pandas as pd
import numpy as np

file_path = '../data/Análise - Tabela da lista das escolas - Detalhado.csv'

df = pd.read_csv(file_path, sep=',')

# columns to be removed
drop_columns_names = [
    "Restrição de Atendimento",
    "Localidade Diferenciada",
    "Categoria Administrativa",
    "Dependência Administrativa",
    "Conveniada Poder Público",
    "Regulamentação pelo Conselho de Educação",
    "Outras Ofertas Educacionais"
]

df = df.drop(columns=drop_columns_names)

# Substituir células vazias ou contendo apenas espaços por NaN
df.replace(r'^\s*$', np.nan, regex=True, inplace=True)

df.to_csv('dataset.csv', index=False, encoding='utf-8')

print(df.head())
