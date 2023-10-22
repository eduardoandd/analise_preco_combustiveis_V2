import dash
from dash import html,dcc,Output,Input,State
import pandas as pd
import plotly.express as px
import unicodedata
import plotly.graph_objects as go



df1=pd.read_excel('2001.xlsx')
df2=pd.read_excel('2013.xlsx')
        
df1.columns = df2.columns
#REMOVENDOS OS ACENTOS DAS COLUNAS
for i in range(len(df1)):
    linha= df1.iloc[i,1]
    linha_sem_acentos = unicodedata.normalize('NFD', linha).encode('ascii', 'ignore').decode('utf-8')
    df1.iloc[i, 1] = linha_sem_acentos  
        
   
df= pd.concat([df1,df2])
 
uf_list= df['ESTADO'].drop_duplicates().tolist()
uf_list.append('Todos')
products_list= df['PRODUTO'].drop_duplicates()
year_list=df['MÊS'].dt.year.drop_duplicates()
year_list.max()


app = dash.Dash(__name__)

app.layout = html.Div(id='div1',
    children=[
        html.H1('Análise de preço dos combustiveis'),
        
        html.Label('Estados:'),
        dcc.Dropdown([{'label': uf, 'value':uf} for uf in uf_list],id='dp-uf'),
        html.Label('Produtos: '),
        dcc.Dropdown([{'label': product, 'value':product} for product in products_list], id='dp-product'),
        
        #html.Button(id='submit-button-state', children='Submit'),
        
        dcc.Graph(id='graph-uf'),
        
        html.Label('Ano'),
        dcc.Slider(
            min=2001,
            max=2023,
            marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(2001,2024)},
            value=2001,
            id='sd-year'
        )

])

@app.callback(
    Output('graph-uf', 'figure'),
    Input('dp-uf', 'value'),
    Input('sd-year', 'value'),
    Input('dp-product', 'value')
)
def df_generate_uf_year_product(uf,year,product): 
    df_filtered= df[['PRODUTO','ESTADO','MÊS','PREÇO MÉDIO REVENDA']]
    if uf == 'Todos' or '':
        
        df_=df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)]
        
        #FORMATO PADRÃO (X[0],Y[1])
        final_df=df_.groupby('ESTADO', as_index=False)['PREÇO MÉDIO REVENDA'].mean()
        
        fig=graph_generate(final_df,final_df.columns[0])
        
        return fig
    
    else:
        month_name = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
             7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
        
        df_=df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year) & (df_filtered['ESTADO']==uf)]
        df_['MÊS']=df_['MÊS'].dt.month
        df_['MÊS NOME'] =  df_['MÊS'].map(month_name)
        
        final_df = df_[['MÊS','PREÇO MÉDIO REVENDA','MÊS NOME']]

        fig=graph_generate(final_df,final_df.columns[2])
    
        return fig
    
def graph_generate(df, color):
    fig = px.bar(df, x=df.columns[0],y=df.columns[1],color=color)
    
    return fig
    
if __name__ == '__main__':
    app.run_server(debug=True,port=8058)