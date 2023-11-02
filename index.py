import dash
from dash import html,dcc,Output,Input,State
import pandas as pd
import plotly.express as px
import unicodedata
import plotly.graph_objects as go
import pdb
import numpy as np
import dash_bootstrap_components as dbc
import plotly.io as pio

#INGESÃO DE DADOS
df1=pd.read_excel('2001.xlsx')
df2=pd.read_excel('2013.xlsx')  
df1.columns = df2.columns

#REMOVENDOS OS ACENTOS DAS COLUNAS
for i in range(len(df1)):
    linha= df1.iloc[i,1]
    linha_sem_acentos = unicodedata.normalize('NFD', linha).encode('ascii', 'ignore').decode('utf-8')
    df1.iloc[i, 1] = linha_sem_acentos  
        
   
df= pd.concat([df1,df2])

#VAR AUX. 
uf_list= df['ESTADO'].drop_duplicates().tolist()
products_list= df['PRODUTO'].drop_duplicates()
year_list=df['MÊS'].dt.year.drop_duplicates()
option_list = ['Brasil','Estados']
filter_list = ['MAX','MIN']

#========= Layout =============

app = dash.Dash(
    external_stylesheets=[dbc.themes.MINTY]
)

app.layout = html.Div(id='div1',
    children=[
        
        dbc.Row([
            
            #MENU LATERAL
            dbc.Col([
                html.H1('Análise de preço dos combustiveis'),
                html.Hr(),
                
                html.Label('Estados:'),
                dcc.Dropdown([{'label': uf, 'value':uf} for uf in uf_list],id='dp-uf'),
                
                html.Label('Produtos: '),
                dcc.Dropdown([{'label': product, 'value':product} for product in products_list], id='dp-product'),
                
                html.Label('Filtros: '),
                dcc.Checklist( [{'label':option, 'value':option} for option in option_list],id='check-option', inputStyle={'margin-right':'5px'}),
                dcc.Checklist( [{'label':option, 'value':option} for option in filter_list],id='check-filter', inputStyle={'margin-right':'5px'}),
                
                html.Label('Ano', style={'margin-top':'8px'}),
                dcc.Slider(
                    min=2001,
                    max=2023,
                    marks=None,
                    value=2001,
                    step=1,
                    id='sd-year',
                    tooltip={"placement": "bottom", "always_visible": True}    
                ),
                

            ],sm=2, style= {'padding':'25px 33px 0px'}),
            
            dbc.Col([
                dbc.Row([
                    dbc.Col([dcc.Graph(id='graph-comparative'),],sm=4),
                    dbc.Col([dcc.Graph(id='graph-region'),],sm=4),
                    dbc.Col([dcc.Graph(id='graph-max-min'),],sm=4),
                ]),
                dbc.Row([
                    dcc.Graph(id='graph-uf'),
                    
                ])
                
            ],sm=10)
            
        ]),
])

# @app.callback(
#     Output('graph-uf', 'figure'),
#     Input('dp-uf', 'value'),
#     Input('sd-year', 'value'),
#     Input('dp-product', 'value'),
#     Input('check-option', 'value'),
#     Input('check-filter', 'value'),
# ) 
# def df_generate_uf_year_product(uf,year,product,option,filter): 
#     # df_filtered= df[['PRODUTO','ESTADO','MÊS','PREÇO MÉDIO REVENDA']]
#     # #filter = ['MAX','MIN']

#     # #BRASIL
#     # df_br=df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)]
#     # final_df_br=df_br.groupby('ESTADO', as_index=False)['PREÇO MÉDIO REVENDA'].mean()
#     # final_df_br['ESTADO(COLOR)']=final_df_br['ESTADO']
#     # fig_br=px.bar(final_df_br, x=final_df_br.columns[0],y=final_df_br.columns[1],color=final_df_br.columns[2])
    
    
#     # #ESTADO
#     # month_name = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
#     #          7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
    
#     # # product ='GASOLINA COMUM'
#     # # year=2008
#     # # uf='SERGIPE'
        
#     # df_uf=df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year) & (df_filtered['ESTADO']==uf)]
#     # df_uf['MÊS']=df_uf['MÊS'].dt.month
#     # df_uf['MÊS NOME'] =  df_uf['MÊS'].map(month_name)
    
#     # final_df_uf = df_uf[['MÊS','PREÇO MÉDIO REVENDA','MÊS NOME']]
    
#     # fig_uf=px.bar(final_df_uf, x=final_df_uf.columns[0],y=final_df_uf.columns[1],color=final_df_uf.columns[2])
    
#     #pdb.set_trace()
#     if not option:
        
#         if not filter:
            
#             # fig_uf.update_layout(
#             #     xaxis_title='Estados',
#             #     yaxis_title='Preços'
#             # )
            
#             return fig_uf

#         elif len(filter) ==1:    
#             if 'MAX' in filter:
#                 df_max=final_df_uf[(final_df_uf['PREÇO MÉDIO REVENDA']==final_df_uf['PREÇO MÉDIO REVENDA'].max())]
                
#                 color =  {'MÊS NOME': '#EF553B'}
                
#                 return px.bar(df_max, x='MÊS NOME',y='PREÇO MÉDIO REVENDA', color='MÊS NOME', color_discrete_map=color)
            
#             elif 'MIN' in filter:
#                 df_min=final_df_uf[(final_df_uf['PREÇO MÉDIO REVENDA']==final_df_uf['PREÇO MÉDIO REVENDA'].min())]
                
#                 return px.bar(df_min, x='MÊS NOME',y='PREÇO MÉDIO REVENDA', color='MÊS NOME')
    
#         elif len(filter) > 1:
            
#             df_max=final_df_uf[(final_df_uf['PREÇO MÉDIO REVENDA']==final_df_uf['PREÇO MÉDIO REVENDA'].max())]
#             df_min=final_df_uf[(final_df_uf['PREÇO MÉDIO REVENDA']==final_df_uf['PREÇO MÉDIO REVENDA'].min())]
            
            
            
#             final_df_min_max_uf= pd.concat([df_max,df_min])
            
#             max = final_df_min_max_uf['PREÇO MÉDIO REVENDA'].max()  
#             final_df_min_max_uf['FILTRO']=np.where(final_df_min_max_uf['PREÇO MÉDIO REVENDA'] ==max,'MAX','MIN')
            
#             color =  {'MAX': '#EF553B', 'MIN': '#636EFA'}
#             fig_max_min= px.bar(final_df_min_max_uf, x='MÊS NOME',y='PREÇO MÉDIO REVENDA',  color='FILTRO', color_discrete_map=color)
            
#             return fig_max_min
        
#         else:
#             return fig_uf
        
#     if 'Brasil' in option:
#         # product ='GASOLINA COMUM'
#         # year=2008
        
#         if not filter:
#             return fig_br
        
#         elif len(filter)==1:
#             if 'MAX' in filter:
#                 df_max=final_df_br[(final_df_br['PREÇO MÉDIO REVENDA']==final_df_br['PREÇO MÉDIO REVENDA'].max())]
                
#                 color =  {'MÊS NOME': '#EF553B'}
                
#                 return px.bar(df_max, x='ESTADO',y='PREÇO MÉDIO REVENDA', color='ESTADO' , color_discrete_map=color)
            
#             elif 'MIN' in filter:
#                 df_min=final_df_br[(final_df_br['PREÇO MÉDIO REVENDA']==final_df_br['PREÇO MÉDIO REVENDA'].min())]
                
#                 return px.bar(df_min, x='ESTADO',y='PREÇO MÉDIO REVENDA', color='ESTADO')
            
#         elif len(filter) == 2:
#             df_max=final_df_br[(final_df_br['PREÇO MÉDIO REVENDA']==final_df_br['PREÇO MÉDIO REVENDA'].max())]
#             df_min=final_df_br[(final_df_br['PREÇO MÉDIO REVENDA']==final_df_br['PREÇO MÉDIO REVENDA'].min())]
            
#             final_df_min_max_br= pd.concat([df_max,df_min])
            
#             max = final_df_min_max_br['PREÇO MÉDIO REVENDA'].max()  
#             final_df_min_max_br['FILTRO']=np.where(final_df_min_max_br['PREÇO MÉDIO REVENDA'] ==max,'MAX','MIN')
            
#             color =  {'MAX': '#EF553B', 'MIN': '#636EFA'}
#             fig_max_min= px.bar(final_df_min_max_br, x='ESTADO',y='PREÇO MÉDIO REVENDA',  color='FILTRO', color_discrete_map=color,template='plotly_dark')
            
#             return fig_max_min
        
#         else:
#             return fig_br
        
#     elif 'Estados' in option:
        
#         if not filter:
#             return fig_uf

#         elif len(filter) ==1:    
#             if 'MAX' in filter:
#                 df_max=final_df_uf[(final_df_uf['PREÇO MÉDIO REVENDA']==final_df_uf['PREÇO MÉDIO REVENDA'].max())]
                
#                 color =  {'MÊS NOME': '#EF553B'}
                
#                 return px.bar(df_max, x='MÊS NOME',y='PREÇO MÉDIO REVENDA', color='MÊS NOME',color_discrete_map=color)
            
#             elif 'MIN' in filter:
#                 df_min=final_df_uf[(final_df_uf['PREÇO MÉDIO REVENDA']==final_df_uf['PREÇO MÉDIO REVENDA'].min())]
                
#                 return px.bar(df_min, x='MÊS NOME',y='PREÇO MÉDIO REVENDA', color='MÊS NOME')
    
#         elif len(filter) > 1:
            
#             df_max=final_df_uf[(final_df_uf['PREÇO MÉDIO REVENDA']==final_df_uf['PREÇO MÉDIO REVENDA'].max())]
#             df_min=final_df_uf[(final_df_uf['PREÇO MÉDIO REVENDA']==final_df_uf['PREÇO MÉDIO REVENDA'].min())]
            
#             final_df_min_max_uf= pd.concat([df_max,df_min])
            
#             max = final_df_min_max_uf['PREÇO MÉDIO REVENDA'].max()  
#             final_df_min_max_uf['FILTRO']=np.where(final_df_min_max_uf['PREÇO MÉDIO REVENDA'] ==max,'MAX','MIN')
            
#             color =  {'MAX': '#EF553B', 'MIN': '#636EFA'}
            
#             fig_max_min= px.bar(final_df_min_max_uf, x='MÊS NOME',y='PREÇO MÉDIO REVENDA', color='FILTRO', color_discrete_map=color)
            
#             return fig_max_min
        
#         else:
#             return fig_uf
        
@app.callback(
    Output('graph-uf', 'figure'),
    Output('graph-comparative','figure'),
    Output('graph-region','figure'),
    Output('graph-max-min','figure'),
    
    Input('dp-uf', 'value'),
    Input('dp-product', 'value'),
    Input('sd-year', 'value'),
    Input('check-option', 'value'),
)    
def graph_select(uf,product,year,option):
    
    #ESTADO
    var_graph_uf=graph_uf(uf,product,year)
    var_graph_region = graph_region(product,year)
    var_graph_uf_x_br=graph_uf_x_br(product,uf,year)
    var_graph_max_min=graph_max_min(product,uf,year)
    
    #BRASIL
    var_graph_br = graph_br(product,year)
    var_graph_max_min_br=graph_max_min_br(product,year)
    var_graph_br_top3_cheap=graph_br_top3_cheap(product,year)
    
    if not option:
        return var_graph_uf,var_graph_uf_x_br,var_graph_region,var_graph_max_min
    
    elif 'Brasil' in option:
        
        return var_graph_br,var_graph_br_top3_cheap,var_graph_region,var_graph_max_min_br
        
    
    else:
        return None
    

#ESTADO    
def graph_uf(uf,product,year):
    
    #VAR AUX
    # product ='GASOLINA COMUM'
    # year=2001
    # uf='SERGIPE'
    
    month_name = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
    
    #============================================================#
    
    df_filtered= df[['PRODUTO','ESTADO','MÊS','PREÇO MÉDIO REVENDA']]
    
    final_df=df_filtered[(df_filtered['ESTADO']==uf) & (df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)] 
    final_df['MÊS NÚMERO']= final_df['MÊS'].dt.month
    final_df['MÊS NOME']= final_df['MÊS NÚMERO'].map(month_name)
    
    return px.bar(final_df, y='PREÇO MÉDIO REVENDA',x='MÊS NÚMERO',color='MÊS NOME')
    
def graph_uf_x_br(product,uf,year):
    
    # product = 'GASOLINA COMUM'
    # uf='AMAZONAS'
    # year=2008
    
    df_filtered = df[['PRODUTO','REGIÃO','PREÇO MÉDIO REVENDA','MÊS','ESTADO']]
    
    df_uf=df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['ESTADO']==uf) & (df_filtered['MÊS'].dt.year==year)].groupby(['ESTADO','PRODUTO','MÊS'],as_index=False)['PREÇO MÉDIO REVENDA'].mean()
    
    df_br = df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)].groupby(['PRODUTO','MÊS'],as_index=False)['PREÇO MÉDIO REVENDA'].mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_br['MÊS'].dt.month,y=df_br['PREÇO MÉDIO REVENDA'], mode='lines+markers', name='Brasil'))
    fig.add_trace(go.Scatter(x=df_uf['MÊS'].dt.month,y=df_uf['PREÇO MÉDIO REVENDA'], mode='lines', name=uf))
    
    fig.update_layout(margin=dict(l=0,r=0,t=20,b=20),height=300)

    return fig

def graph_max_min(product,uf,year):
    
    df_filtered= df[['PRODUTO','ESTADO','MÊS','PREÇO MÉDIO REVENDA']]
    
    # product = 'GASOLINA COMUM'
    # uf='AMAZONAS'
    # year=2008
    
    final_df=df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['ESTADO']==uf) & (df_filtered['MÊS'].dt.year==year)].groupby(['PRODUTO','ESTADO','MÊS'],as_index=False)['PREÇO MÉDIO REVENDA'].mean()
    
    month_name = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
    
    final_df['MÊS_'] =final_df['MÊS'].dt.month
    final_df['MÊS NOME'] = final_df['MÊS_'].map(month_name)
    
    
    df_max=final_df[(final_df['PREÇO MÉDIO REVENDA']==final_df['PREÇO MÉDIO REVENDA'].max())]
    df_min=final_df[(final_df['PREÇO MÉDIO REVENDA']==final_df['PREÇO MÉDIO REVENDA'].min())]
    
    fig = go.Figure(
        data = [
            go.Bar(x=df_max['MÊS NOME'], y=df_max['PREÇO MÉDIO REVENDA'], name='Max'),
            go.Bar(x=df_min['MÊS NOME'], y=df_min['PREÇO MÉDIO REVENDA'], name='Min'),
        ]
    )
    
    fig.update_layout(margin=dict(l=0,r=0,t=20,b=20),height=300)
    
    return fig

 
#BRASIL
def graph_br(product,year):
      
    #VAR AUX
    # product ='GASOLINA COMUM'
    # year=2001
    # uf='SERGIPE'
    
    df_filtered= df[['PRODUTO','ESTADO','MÊS','PREÇO MÉDIO REVENDA']]

    final_df = df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)].groupby(['ESTADO'],as_index=False)['PREÇO MÉDIO REVENDA'].mean()
    
    return px.bar(final_df,y='PREÇO MÉDIO REVENDA',x='ESTADO', color='ESTADO')

def graph_br_top3_cheap(product,year):
    
    # product = 'GASOLINA COMUM'
    # year=2015
    
    df_filtered= df[['PRODUTO','ESTADO','MÊS','PREÇO MÉDIO REVENDA']]
    
    df_=df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)]
    
    top_3=df_.groupby('ESTADO')['PREÇO MÉDIO REVENDA'].mean().sort_values(ascending=True).head(3)
    
    ufs=top_3.index.to_list()
    
    list_dict = []
    
    for uf in ufs:      
    
        df_dict=df_filtered[(df_filtered['ESTADO']==uf) & (df_filtered['MÊS'].dt.year==year) & (df_filtered['PRODUTO']==product)].groupby(['ESTADO','MÊS'],as_index=False)['PREÇO MÉDIO REVENDA'].mean()
        df_dict['MONTH'] = df_dict['MÊS'].dt.month
        
        dict_df=df_dict.to_dict()
        
        list_dict.append(dict_df)
        
    uf_1=pd.DataFrame(list_dict[0])
    uf_2=pd.DataFrame(list_dict[1])
    uf_3=pd.DataFrame(list_dict[2])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=uf_1['MONTH'],y=uf_1['PREÇO MÉDIO REVENDA'], mode='lines+markers', name=uf_1.iloc[1,0]))
    fig.add_trace(go.Scatter(x=uf_2['MONTH'],y=uf_2['PREÇO MÉDIO REVENDA'], mode='lines', name=uf_2.iloc[1,0]))
    fig.add_trace(go.Scatter(x=uf_3['MONTH'],y=uf_3['PREÇO MÉDIO REVENDA'], mode='markers', name=uf_3.iloc[1,0]))
    
    fig.update_layout(margin=dict(l=0,r=0,t=20,b=20),height=300)
    
    return fig

def graph_region(product,year):
    df_filtered = df[['PRODUTO','REGIÃO','PREÇO MÉDIO REVENDA','MÊS','ESTADO']]
                
    df_= df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)]
            
    final_df=df_.groupby('REGIÃO',as_index=False)['PREÇO MÉDIO REVENDA'].mean()
        
    fig = px.bar(final_df, x='PREÇO MÉDIO REVENDA', y='REGIÃO', color='REGIÃO', orientation='h', barmode='group')
    
    fig.update_layout(margin=dict(l=0,r=0,t=20,b=20),height=300)
    
    return fig

def graph_max_min_br(product,year):
    
    df_filtered= df[['PRODUTO','ESTADO','MÊS','PREÇO MÉDIO REVENDA']]

    final_df = df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)].groupby(['ESTADO'],as_index=False)['PREÇO MÉDIO REVENDA'].mean()
    
    df_max = final_df[(final_df['PREÇO MÉDIO REVENDA']==final_df['PREÇO MÉDIO REVENDA'].max())]
    
    df_min = final_df[(final_df['PREÇO MÉDIO REVENDA']==final_df['PREÇO MÉDIO REVENDA'].min())]
    
    fig = go.Figure(
        data=[
            go.Bar(x=df_max['ESTADO'],y=df_max['PREÇO MÉDIO REVENDA'], name='Max', marker=dict(color='red')),
            go.Bar(x=df_min['ESTADO'],y=df_min['PREÇO MÉDIO REVENDA'], name='Min', marker=dict(color='blue'))
        ]
    )
    
    fig.update_layout(margin=dict(l=0,r=0,t=20,b=20),height=300)
    
    return fig



if __name__ == '__main__':
    app.run_server(debug=True,port=8099)