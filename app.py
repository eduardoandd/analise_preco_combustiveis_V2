import dash
from dash import html,dcc,Output,Input,State
import pandas as pd
import plotly.express as px
import unicodedata
import plotly.graph_objects as go

#TRANSFORMAR O RETORNO DA FUNÇÃO df_generate_uf_year_product em um dicionario e depois converter para dataframe
#ADICIONAR novamente o filtro MAX E MIN


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
products_list= df['PRODUTO'].drop_duplicates()
year_list=df['MÊS'].dt.year.drop_duplicates()
year_list.max()

option_list = ['Brasil','Estados']

app = dash.Dash(__name__)

app.layout = html.Div(id='div1',
    children=[
        dcc.Store(id='store'),
        html.H1('Análise de preço dos combustiveis'),
        
        html.Label('Estados:'),
        dcc.Dropdown([{'label': uf, 'value':uf} for uf in uf_list],id='dp-uf'),
        html.Label('Produtos: '),
        dcc.Dropdown([{'label': product, 'value':product} for product in products_list], id='dp-product'),
        html.Label('Filtros: '),
        dcc.Checklist( [{'label':option, 'value':option} for option in option_list],id='check-option'),
        
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
    Input('dp-product', 'value'),
    Input('check-option', 'value'),
) 
def df_generate_uf_year_product(uf,year,product,option): 
    df_filtered= df[['PRODUTO','ESTADO','MÊS','PREÇO MÉDIO REVENDA']]
    
    
    df_=df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)]
    final_df=df_.groupby('ESTADO', as_index=False)['PREÇO MÉDIO REVENDA'].mean()
    final_df['ESTADO(COLOR)']=final_df['ESTADO']
    final_df[(final_df['PREÇO MÉDIO REVENDA']==final_df['PREÇO MÉDIO REVENDA'].max())]
    fig=px.bar(final_df, x=final_df.columns[0],y=final_df.columns[1],color=final_df.columns[2])
    
    if not option:
        
        return fig
    
    if 'Brasil' in option:
        # product ='GASOLINA COMUM'
        # year=2008
        
        df_=df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)]
        
        final_df=df_.groupby('ESTADO', as_index=False)['PREÇO MÉDIO REVENDA'].mean()
        final_df['ESTADO(COLOR)']=final_df['ESTADO']
        final_df[(final_df['PREÇO MÉDIO REVENDA']==final_df['PREÇO MÉDIO REVENDA'].max())]
        
        fig=px.bar(final_df, x=final_df.columns[0],y=final_df.columns[1],color=final_df.columns[2])
        
        return fig
    
    elif 'Estados' in option:
        month_name = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
             7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
        
        df_=df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year) & (df_filtered['ESTADO']==uf)]
        df_['MÊS']=df_['MÊS'].dt.month
        df_['MÊS NOME'] =  df_['MÊS'].map(month_name)
        
        final_df = df_[['MÊS','PREÇO MÉDIO REVENDA','MÊS NOME']]
        
        fig=px.bar(final_df, x=final_df.columns[0],y=final_df.columns[1],color=final_df.columns[2])

        return fig
    
    
        
        
    
    
 
# @app.callback(
#     Output('graph-uf','figure'),
#     Input('store','data'),

# )    
# def option_graph(df):
    
#     #FORMATO PADRÃO (X[0],Y[1], COLOR[3])
#     df_ = pd.DataFrame(df)
    
#     fig = 
        
#     return fig





if __name__ == '__main__':
    app.run_server(debug=True,port=8064)