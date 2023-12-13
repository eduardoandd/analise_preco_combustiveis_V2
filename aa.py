import pandas as pd
import plotly.graph_objects as go

# Exemplo de dados
product = 'GASOLINA COMUM'
year = 2001
uf = 'SERGIPE'
theme = True  # ou False

# Exemplo de template_theme1 e template_theme2
template_theme1 = "light_template"
template_theme2 = "dark_template"

# Exemplo de DataFrame df
# Substitua isso pelo seu DataFrame real
df = pd.DataFrame({
    'PRODUTO': ['GASOLINA COMUM'] * 6,
    'ESTADO': ['SERGIPE'] * 6,
    'MÊS': pd.to_datetime(['2001-01-01', '2001-02-01', '2002-01-01', '2002-02-01', '2003-01-01', '2003-02-01']),
    'PREÇO MÉDIO REVENDA': [2.5, 2.6, 2.3, 2.4, 2.7, 2.8],
    'MÊS NÚMERO': [1, 2, 1, 2, 1, 2],
    'MÊS NOME': ['Janeiro', 'Fevereiro', 'Janeiro', 'Fevereiro', 'Janeiro', 'Fevereiro'],
})

template = template_theme1 if theme else template_theme2

df_filtered = df[['PRODUTO', 'ESTADO', 'MÊS', 'PREÇO MÉDIO REVENDA', 'MÊS NÚMERO', 'MÊS NOME']]

final_df = df_filtered[(df_filtered['ESTADO'] == uf) & (df_filtered['PRODUTO'] == product) & (df_filtered['MÊS'].dt.year == year)]

df_min_max = final_df.groupby('MÊS NOME', as_index=False)['PREÇO MÉDIO REVENDA'].min().sort_values(by='PREÇO MÉDIO REVENDA', ascending=True)

# Calculando a variação percentual em relação ao mesmo período do ano anterior
df_min_max['Variação Percentual'] = df_min_max['PREÇO MÉDIO REVENDA'].pct_change() * 100

fig_indicator_min = go.Figure(
    go.Indicator(
        mode='number+delta',
        title={'text': f'<span style="font-size:90%">{df_min_max["MÊS NOME"].iloc[0]} - MÊS MAIS BARATO</span>'},
        value=df_min_max['PREÇO MÉDIO REVENDA'].iloc[0],
        number={'prefix': 'R$'},
        delta={'relative': True,
               'valueformat': '.1f%',  # ou '.1%' se quiser uma casa decimal
               'reference': df_min_max['Variação Percentual'].iloc[0]}
    )
)

fig_indicator_min.update_layout(template=template)

# Exibindo a figura
fig_indicator_min.show()
