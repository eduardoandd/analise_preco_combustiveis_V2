import dash
from dash import html,dcc,Output,Input,State
import pandas as pd
import plotly.express as px
import unicodedata
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.io as pio
from dash_bootstrap_templates import ThemeSwitchAIO
from dash import html,dcc,Input,Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import ThemeSwitchAIO
import dash

# #INGESTÃO DE DADOS
df1=pd.read_excel('2001.xlsx')
df2=pd.read_excel('2013.xlsx')  
df1.columns = df2.columns

#REMOVENDOS OS ACENTOS DAS LINHAS
for i in range(len(df1)):
    linha= df1.iloc[i,1]
    linha_sem_acentos = unicodedata.normalize('NFD', linha).encode('ascii', 'ignore').decode('utf-8')
    df1.iloc[i, 1] = linha_sem_acentos  
           
df= pd.concat([df1,df2])

month_name = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
df['MÊS NÚMERO']= df['MÊS'].dt.month
df['MÊS NOME']= df['MÊS NÚMERO'].map(month_name)



# df1_semanal=pd.read_excel('semanal-estados-2004-a-2012.xlsx',skiprows=12)
# df2_semanal=pd.read_excel('semanal-estados-desde-2013.xlsx',skiprows=17)

# #REMOVENDOS OS ACENTOS DAS LINHAS
# for i in range(len(df1)):
#     linha= df1_semanal.iloc[i,4]
#     linha_sem_acentos = unicodedata.normalize('NFD', linha).encode('ascii', 'ignore').decode('utf-8')
#     df1_semanal.iloc[i, 4] = linha_sem_acentos  
    
# df_semanal= pd.concat([df1_semanal,df2_semanal])


# #VAR AUX. 
uf_list= df['ESTADO'].drop_duplicates().tolist()
products_list= df['PRODUTO'].drop_duplicates()
year_list=df['MÊS'].dt.year.drop_duplicates()
option_list = ['Brasil','Estados']
filter_list = ['MAX','MIN']

template_theme1='flatly'
template_theme2='darkly'
url_theme1=dbc.themes.FLATLY
url_theme2=dbc.themes.DARKLY
tab_card = {'height': '100%'}
main_config = {
    'hovermode': 'x unified',
    "margin": {"l":10,"r":10,"t":10,"b":10}
}

#========= Layout =============

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = html.Div(id='div1',
    children=[
        
        #ROW 1
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Legend('Fuel Price Brazil')
                            ], sm=8),
                            dbc.Col([
                                html.I(className='fa fa-balance-scale', style={'font-size': '300%'})
                            ], sm=4, align='center'),
                        ]),
                        
                        dbc.Row([
                            dbc.Col([
                                ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2])
                            ])
                        ], style={'margin-top':'10px'}),
                        
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        dbc.Row([
                                            html.H6('Selecione as opções desejadas', style={'text-align':'center'})
                                        ]),
                                        dbc.Row([
                                            dbc.Col([
                                                html.Label('Estados:'),
                                                dcc.Dropdown([{'label': uf, 'value':uf} for uf in uf_list],id='dp-uf'),
                                            ],sm=6),
                                            dbc.Col([
                                                html.Label('Produtos:'),
                                                dcc.Dropdown([{'label': product, 'value':product} for product in products_list],id='dp-product'),
                                            ],sm=6),
                                            
                                            dbc.Row([
                                                html.Hr(style={'margin-top':'15px'}),
                                                
                                                html.Label('Ano'),
                                                dcc.Slider(
                                                    min=2001,
                                                    max=2023,
                                                    marks=None,
                                                    value=2001,
                                                    step=1,
                                                    id='sd-year',
                                                    tooltip={"placement": "bottom", "always_visible": True} 
                                                )   
                                            ], style={'padding':' 0px 100px 0px 100px'})
                                            
                                        ])
                                    ])
                                ], style=tab_card)
                            ])
                        ])
                        
                    ])
                ])
            ],md=4),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row(
                            dbc.Col(
                                html.Legend('Top Consultores por Equipe')
                            )
                        ),
                        
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='graph-uf', className='dbc')
                            ])
                        ])
                    ])
                ], style=tab_card)
            ],md=8)
            
        ],className='g-2 my-auto', style={'margin-top': '7px'}),
        
        #ROW 2
        dbc.Row([
            dbc.Col([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph_indicator_max', className='dbc')
                        ])
                    ],style=tab_card)
                ],md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph_indicator_min', className='dbc')
                        ])
                    ],style=tab_card)
                ],md=4),
                
            ],md=4)
        ])
        
])


#PRINCIPAL     
@app.callback(
    Output('graph-uf', 'figure'),
    Output('graph_indicator_max', 'figure'),
    Output('graph_indicator_min', 'figure'),
    # Output('graph-comparative','figure'),
    # Output('graph-region','figure'),
    # Output('graph-max-min','figure'),
    
    Input('dp-uf', 'value'),
    Input('dp-product', 'value'),
    Input('sd-year', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'),'value'),
    # Input('check-option', 'value'),
)    
def graph_select(uf,product,year,theme):
    
    #ESTADO
    var_graph_uf=graph_uf(uf,product,year,theme)
    var_graph_indicator_max=graph_indicator_max(uf,product,year,theme)
    var_graph_indicator_min=graph_indicator_min(uf,product,year,theme)
    # var_dinamyc_week = graph_dinamyc_week(uf,product,year)
    # var_graph_uf_x_br=graph_uf_x_br(product,uf,year)
    # var_graph_max_min=graph_max_min(product,uf,year)
    
    #BRASIL
    # var_graph_br = graph_br(product,year)
    # var_graph_max_min_br=graph_max_min_br(product,year)
    # var_graph_br_top3_cheap=graph_br_top3_cheap(product,year)
    # var_graph_region=graph_region(product,year)
    
    return var_graph_uf,var_graph_indicator_max,var_graph_indicator_min
    
    # if not option:
    #     if year >=2004:
    #         return var_graph_uf,var_graph_uf_x_br,var_dinamyc_week,var_graph_max_min
    #     else:
    #         return var_graph_uf,var_graph_uf_x_br,var_graph_region,var_graph_max_min

    
    # elif 'Brasil' in option:
        
    #     return var_graph_br,var_graph_br_top3_cheap,var_graph_region,var_graph_max_min_br
        
    
    # else:
    #     return None
    
# #ESTADO    
def graph_uf(uf,product,year,theme):
    
    #VAR AUX
    # product ='GASOLINA COMUM'
    # year=2001
    # uf='SERGIPE'
    
    template = template_theme1 if theme else template_theme2
    month_name = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
    
    #============================================================#
    
    df_filtered= df[['PRODUTO','ESTADO','MÊS','PREÇO MÉDIO REVENDA']]
    
    final_df=df_filtered[(df_filtered['ESTADO']==uf) & (df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)] 
    final_df['MÊS NÚMERO']= final_df['MÊS'].dt.month
    final_df['MÊS NOME']= final_df['MÊS NÚMERO'].map(month_name)
    
    fig=px.bar(final_df, y='PREÇO MÉDIO REVENDA',x='MÊS NÚMERO',color='MÊS NOME')
    
    fig.update_layout(main_config, height=260, template=template)

    
    return fig

def graph_indicator_max(uf,product,year,theme):
    
    template = template_theme1 if theme else template_theme2
    
    # product ='GASOLINA COMUM'
    # year=2002
    # uf='SERGIPE'
    
    df_filtered= df[['PRODUTO','ESTADO','MÊS','PREÇO MÉDIO REVENDA','MÊS NÚMERO','MÊS NOME']]
    
    final_df=df_filtered[(df_filtered['ESTADO']==uf) & (df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)]
    
    df_max=final_df.groupby('MÊS NOME',as_index=False)['PREÇO MÉDIO REVENDA'].max().sort_values(by='PREÇO MÉDIO REVENDA', ascending=False).head(1)
    
    #ANO ANTERIOR
    df_ano_interior=df_filtered[(df_filtered['ESTADO']==uf) & (df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year-1)]
    df_max_anterior=df_ano_interior.groupby('MÊS NOME',as_index=False)['PREÇO MÉDIO REVENDA'].max().sort_values(by='PREÇO MÉDIO REVENDA', ascending=False).head(1)
    
    variacao_porcentual_max= ((df_max['PREÇO MÉDIO REVENDA'].max() - df_max_anterior['PREÇO MÉDIO REVENDA'].max()) /  df_max_anterior['PREÇO MÉDIO REVENDA'].max()) * 100
        
    fig_indicator_max= go.Figure(
            go.Indicator(
                mode='number+delta',
                title={'text':f'<span style="font-size:90%">{df_max["MÊS NOME"].iloc[0]} - MÊS MAIS BARATO</span>'},
                value=df_max['PREÇO MÉDIO REVENDA'].iloc[0],
                number={'prefix':'R$'}
            )
        )
        
    if variacao_porcentual_max > 1:
        
        fig_indicator_max.add_annotation(
            text=f'Variação Percentual: {variacao_porcentual_max:.2f}%',
            showarrow=False,
            x=0.5,
            y=0.20,
            font=dict(size=20, color='red')
        )
    else:    
        fig_indicator_max.add_annotation(
            text=f'Variação Percentual: {variacao_porcentual_max:.2f}%',
            showarrow=False,
            x=0.5,
            y=0.20,
            font=dict(size=20, color='green')
        )
        
        
    return fig_indicator_max
    
def graph_indicator_min(uf,product,year,theme):
    
    template = template_theme1 if theme else template_theme2
    
    # product ='GASOLINA COMUM'
    # year=2002
    # uf='SERGIPE'
    
    df_filtered= df[['PRODUTO','ESTADO','MÊS','PREÇO MÉDIO REVENDA','MÊS NÚMERO','MÊS NOME']]
    
    final_df=df_filtered[(df_filtered['ESTADO']==uf) & (df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)]
    
    df_min=final_df.groupby('MÊS NOME',as_index=False)['PREÇO MÉDIO REVENDA'].min().sort_values(by='PREÇO MÉDIO REVENDA', ascending=True).head(1)
    
    #ANO ANTERIOR
    df_ano_interior=df_filtered[(df_filtered['ESTADO']==uf) & (df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year-1)]
    df_min_anterior=df_ano_interior.groupby('MÊS NOME',as_index=False)['PREÇO MÉDIO REVENDA'].min().sort_values(by='PREÇO MÉDIO REVENDA', ascending=True).head(1)
    
    variacao_porcentual_min= ((df_min['PREÇO MÉDIO REVENDA'].min() - df_min_anterior['PREÇO MÉDIO REVENDA'].min()) /  df_min_anterior['PREÇO MÉDIO REVENDA'].min()) * 100
    
    fig_indicator_min= go.Figure(
            go.Indicator(
                mode='number+delta',
                title={'text':f'<span style="font-size:90%">{df_min["MÊS NOME"].iloc[0]} - MÊS MAIS BARATO</span>'},
                value=df_min['PREÇO MÉDIO REVENDA'].iloc[0],
                number={'prefix':'R$'}
            )
        )
    
    if variacao_porcentual_min > 0:
        
        fig_indicator_min.add_annotation(
            text=f'Variação Percentual: {variacao_porcentual_min:.2f}%',
            showarrow=False,
            x=0.5,
            y=0.20,
            font=dict(size=20, color='red')
        )
    else:    
        fig_indicator_min.add_annotation(
            text=f'Variação Percentual: {variacao_porcentual_min:.2f}%',
            showarrow=False,
            x=0.5,
            y=0.20,
            font=dict(size=20, color='green')
        )
        
    return fig_indicator_min
    
        
    
    
   
    
    
    
    
   
# def graph_uf_x_br(product,uf,year):
    
#     # product = 'GASOLINA COMUM'
#     # uf='AMAZONAS'
#     # year=2008
    
#     df_filtered = df[['PRODUTO','REGIÃO','PREÇO MÉDIO REVENDA','MÊS','ESTADO']]
    
#     df_uf=df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['ESTADO']==uf) & (df_filtered['MÊS'].dt.year==year)].groupby(['ESTADO','PRODUTO','MÊS'],as_index=False)['PREÇO MÉDIO REVENDA'].mean()
    
#     df_br = df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)].groupby(['PRODUTO','MÊS'],as_index=False)['PREÇO MÉDIO REVENDA'].mean()
    
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=df_br['MÊS'].dt.month,y=df_br['PREÇO MÉDIO REVENDA'], mode='lines+markers', name='Brasil'))
#     fig.add_trace(go.Scatter(x=df_uf['MÊS'].dt.month,y=df_uf['PREÇO MÉDIO REVENDA'], mode='lines', name=uf))
    
#     fig.update_layout(margin=dict(l=0,r=0,t=20,b=20),height=300)

#     return fig

# def graph_dinamyc_week(uf,product,year):
    
#     # product = 'GASOLINA COMUM'
#     # uf='AMAZONAS'
#     # year=2008
    
#     df_filtered = df_semanal[['PRODUTO','REGIÃO','PREÇO MÉDIO REVENDA','DATA FINAL','ESTADO']]
    
#     final_df = df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['ESTADO']==uf) & (df_filtered['DATA FINAL'].dt.year==year)].groupby(['ESTADO','DATA FINAL'], as_index=False)['PREÇO MÉDIO REVENDA'].mean()
    
    
#     fig = go.Figure()

#     fig.add_trace(
#         go.Scatter(x=final_df['DATA FINAL'],y=final_df['PREÇO MÉDIO REVENDA']))

#     fig.update_layout(
#         xaxis=dict(
#             rangeselector=dict(
#                 buttons= list([
#                     dict(count=0,
#                         label='1m',
#                         step='month',
#                         stepmode="backward",
#                         visible=False
#                     )
#                 ])
#             ),
#             rangeslider=dict(
#                 visible=True,
#             ),
            
#         )
#     ),
    
#     return fig

# def graph_max_min(product,uf,year):
    
#     df_filtered= df[['PRODUTO','ESTADO','MÊS','PREÇO MÉDIO REVENDA']]
    
#     # product = 'GASOLINA COMUM'
#     # uf='AMAZONAS'
#     # year=2008
    
#     final_df=df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['ESTADO']==uf) & (df_filtered['MÊS'].dt.year==year)].groupby(['PRODUTO','ESTADO','MÊS'],as_index=False)['PREÇO MÉDIO REVENDA'].mean()
    
#     month_name = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
    
#     final_df['MÊS_'] =final_df['MÊS'].dt.month
#     final_df['MÊS NOME'] = final_df['MÊS_'].map(month_name)
    
    
#     df_max=final_df[(final_df['PREÇO MÉDIO REVENDA']==final_df['PREÇO MÉDIO REVENDA'].max())]
#     df_min=final_df[(final_df['PREÇO MÉDIO REVENDA']==final_df['PREÇO MÉDIO REVENDA'].min())]
    
#     fig = go.Figure(
#         data = [
#             go.Bar(x=df_max['MÊS NOME'], y=df_max['PREÇO MÉDIO REVENDA'], name='Max'),
#             go.Bar(x=df_min['MÊS NOME'], y=df_min['PREÇO MÉDIO REVENDA'], name='Min'),
#         ]
#     )
    
#     fig.update_layout(margin=dict(l=0,r=0,t=20,b=20),height=300)
    
#     return fig

 
# #BRASIL
# def graph_br(product,year):
      
#     #VAR AUX
#     # product ='GASOLINA COMUM'
#     # year=2001
#     # uf='SERGIPE'
    
#     df_filtered= df[['PRODUTO','ESTADO','MÊS','PREÇO MÉDIO REVENDA']]

#     final_df = df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)].groupby(['ESTADO'],as_index=False)['PREÇO MÉDIO REVENDA'].mean()
    
#     return px.bar(final_df,y='PREÇO MÉDIO REVENDA',x='ESTADO', color='ESTADO')

# def graph_br_top3_cheap(product,year):
    
#     # product = 'GASOLINA COMUM'
#     # year=2015
    
#     df_filtered= df[['PRODUTO','ESTADO','MÊS','PREÇO MÉDIO REVENDA']]
    
#     df_=df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)]
    
#     top_3=df_.groupby('ESTADO')['PREÇO MÉDIO REVENDA'].mean().sort_values(ascending=True).head(3)
    
#     ufs=top_3.index.to_list()
    
#     list_dict = []
    
#     for uf in ufs:      
    
#         df_dict=df_filtered[(df_filtered['ESTADO']==uf) & (df_filtered['MÊS'].dt.year==year) & (df_filtered['PRODUTO']==product)].groupby(['ESTADO','MÊS'],as_index=False)['PREÇO MÉDIO REVENDA'].mean()
#         df_dict['MONTH'] = df_dict['MÊS'].dt.month
        
#         dict_df=df_dict.to_dict()
        
#         list_dict.append(dict_df)
        
#     uf_1=pd.DataFrame(list_dict[0])
#     uf_2=pd.DataFrame(list_dict[1])
#     uf_3=pd.DataFrame(list_dict[2])
    
#     fig = go.Figure()
    
#     fig.add_trace(go.Scatter(x=uf_1['MONTH'],y=uf_1['PREÇO MÉDIO REVENDA'], mode='lines+markers', name=uf_1.iloc[1,0]))
#     fig.add_trace(go.Scatter(x=uf_2['MONTH'],y=uf_2['PREÇO MÉDIO REVENDA'], mode='lines', name=uf_2.iloc[1,0]))
#     fig.add_trace(go.Scatter(x=uf_3['MONTH'],y=uf_3['PREÇO MÉDIO REVENDA'], mode='markers', name=uf_3.iloc[1,0]))
    
#     fig.update_layout(margin=dict(l=0,r=0,t=20,b=20),height=300)
    
#     return fig

# def graph_region(product,year):
#     df_filtered = df[['PRODUTO','REGIÃO','PREÇO MÉDIO REVENDA','MÊS','ESTADO']]
                
#     df_= df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)]
            
#     final_df=df_.groupby('REGIÃO',as_index=False)['PREÇO MÉDIO REVENDA'].mean()
        
#     fig = px.bar(final_df, x='PREÇO MÉDIO REVENDA', y='REGIÃO', color='REGIÃO', orientation='h', barmode='group')
    
#     fig.update_layout(margin=dict(l=0,r=0,t=20,b=20),height=300)
    
#     return fig

# def graph_max_min_br(product,year):
    
    # df_filtered= df[['PRODUTO','ESTADO','MÊS','PREÇO MÉDIO REVENDA']]

    # final_df = df_filtered[(df_filtered['PRODUTO']==product) & (df_filtered['MÊS'].dt.year==year)].groupby(['ESTADO'],as_index=False)['PREÇO MÉDIO REVENDA'].mean()
    
    # df_max = final_df[(final_df['PREÇO MÉDIO REVENDA']==final_df['PREÇO MÉDIO REVENDA'].max())]
    
    # df_min = final_df[(final_df['PREÇO MÉDIO REVENDA']==final_df['PREÇO MÉDIO REVENDA'].min())]
    
    # fig = go.Figure(
    #     data=[
    #         go.Bar(x=df_max['ESTADO'],y=df_max['PREÇO MÉDIO REVENDA'], name='Max', marker=dict(color='red')),
    #         go.Bar(x=df_min['ESTADO'],y=df_min['PREÇO MÉDIO REVENDA'], name='Min', marker=dict(color='blue'))
    #     ]
    # )
    
    # fig.update_layout(margin=dict(l=0,r=0,t=20,b=20),height=300)
    
    # return fig

if __name__ == '__main__':
    app.run_server(debug=True,port=8040)