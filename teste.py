import pandas as pd
import unicodedata
import plotly.graph_objects as go


df1=pd.read_excel('semanal-estados-2004-a-2012.xlsx',skiprows=12)
df2=pd.read_excel('semanal-estados-desde-2013.xlsx',skiprows=17)



for i in range(len(df1)):
    linha= df1.iloc[i,4]
    linha_sem_acentos = unicodedata.normalize('NFD', linha).encode('ascii', 'ignore').decode('utf-8')
    df1.iloc[i, 4] = linha_sem_acentos  
    
df_= pd.concat([df1,df2])

df_teste = df_[(df_['PRODUTO']=='GASOLINA COMUM') & (df_['ESTADO']=='ACRE') & (df_['DATA FINAL'].dt.year==2008)].groupby(['ESTADO','DATA FINAL'], as_index=False)['PREÇO MÉDIO REVENDA'].mean()


fig = go.Figure()

fig.add_trace(
    go.Scatter(x=df_teste['DATA FINAL'],y=df_teste['PREÇO MÉDIO REVENDA']))

fig.update_layout(
    title_text='Variação semanal'
)

fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons= list([
                dict(count=0,
                     label='1m',
                     step='month',
                     stepmode="backward",
                     visible=False
                )
            ])
        ),
        rangeslider=dict(
            visible=True,
        ),
        
    )
),






fig = go.Figure(go.Scatter(
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    y = [28.8, 28.5, 37, 56.8, 69.7, 79.7, 78.5, 77.8, 74.1, 62.6, 45.3, 39.9]
))

fig.update_layout(
    xaxis = dict(
        tickmode='linear',
        tick0=0.5,
        dtick=0.25
    )
)







import plotly.graph_objects as go

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

fig = go.Figure(go.Scatter(
    x = df['Date'],
    y = df['AAPL.High'],
))

fig.update_layout(
    title = 'Time Series with Custom Date-Time Format',
    xaxis_tickformat = '%d %B (%a)<br>%Y'
)


fig.show()








