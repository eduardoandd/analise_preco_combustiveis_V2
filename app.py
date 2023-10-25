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
products_list= df['PRODUTO'].drop_duplicates()
year_list=df['MÊS'].dt.year.drop_duplicates()
year_list.max()

option_list = ['Brasil','Estados']

filter_list = ['MAX','MIN']

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
        dcc.Checklist( [{'label':option, 'value':option} for option in filter_list],id='check-filter'),
        
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
    Input('check-filter', 'value'),
) 
def df_generate_uf_year_product(uf,year,product,option,filter): 
    df_filtered= df[['PRODUTO','ESTADO','MÊS','PREÇO MÉDIO REVENDA']]
    
    #BRASIL
    df_br=df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)]
    final_df_br=df_br.groupby('ESTADO', as_index=False)['PREÇO MÉDIO REVENDA'].mean()
    final_df_br['ESTADO(COLOR)']=final_df_br['ESTADO']
    fig_br=px.bar(final_df_br, x=final_df_br.columns[0],y=final_df_br.columns[1],color=final_df_br.columns[2])
    
    
    #ESTADO
    month_name = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
             7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
        
    df_uf=df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year) & (df_filtered['ESTADO']==uf)]
    df_uf['MÊS']=df_uf['MÊS'].dt.month
    df_uf['MÊS NOME'] =  df_uf['MÊS'].map(month_name)
    
    final_df_uf = df_uf[['MÊS','PREÇO MÉDIO REVENDA','MÊS NOME']]
    
    fig_uf=px.bar(final_df_uf, x=final_df_uf.columns[0],y=final_df_uf.columns[1],color=final_df_uf.columns[2])
    
    
    if not option:
        
        if not filter:
            return fig_uf
        
        if 'MAX' in filter:
            df_max=final_df_uf[(final_df_uf['PREÇO MÉDIO REVENDA']==final_df_uf['PREÇO MÉDIO REVENDA'].max())]
            
            return px.bar(df_max, x='MÊS',y='PREÇO MÉDIO REVENDA', color='MÊS NOME')
        
        elif 'MIN' in filter:
            df_min=final_df_uf[(final_df_uf['PREÇO MÉDIO REVENDA']==final_df_uf['PREÇO MÉDIO REVENDA'].min())]
            
            return px.bar(df_min, x='MÊS',y='PREÇO MÉDIO REVENDA', color='MÊS NOME')
        
    
    if 'Brasil' in option:
        # product ='GASOLINA COMUM'
        # year=2008
        
        
        if not filter:
            return fig_br
        
        if 'MAX' in filter:
            df_max=final_df_br[(final_df_br['PREÇO MÉDIO REVENDA']==final_df_br['PREÇO MÉDIO REVENDA'].max())]
            
            return px.bar(df_max, x='ESTADO',y='PREÇO MÉDIO REVENDA', color='ESTADO')
        
        elif 'MIN' in filter:
            df_min=final_df_br[(final_df_br['PREÇO MÉDIO REVENDA']==final_df_br['PREÇO MÉDIO REVENDA'].min())]
            
            return px.bar(df_min, x='ESTADO',y='PREÇO MÉDIO REVENDA', color='ESTADO')
            
    
    elif 'Estados' in option:
        
        if not filter:
            return fig_uf
        
        if 'MAX' in filter:
            df_max=final_df_uf[(final_df_uf['PREÇO MÉDIO REVENDA']==final_df_uf['PREÇO MÉDIO REVENDA'].max())]
            
            return px.bar(df_max, x='MÊS',y='PREÇO MÉDIO REVENDA', color='MÊS NOME')
        
        elif 'MIN' in filter:
            df_min=final_df_uf[(final_df_uf['PREÇO MÉDIO REVENDA']==final_df_uf['PREÇO MÉDIO REVENDA'].min())]
            
            return px.bar(df_min, x='MÊS',y='PREÇO MÉDIO REVENDA', color='MÊS NOME')
        
        

        
if __name__ == '__main__':
    app.run_server(debug=True,port=8065)