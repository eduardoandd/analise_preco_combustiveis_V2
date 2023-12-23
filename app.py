import dash
from dash import html,dcc,Output,Input
import pandas as pd
import plotly.express as px
import unicodedata
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash import html,dcc,Input,Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import ThemeSwitchAIO
import dash
import geopandas as gpd
import sqlite3

# #INGESTÃO DE DADOS

conn = sqlite3.connect('web.db',check_same_thread=False)

# df1=pd.read_excel('2001.xlsx')
# df2=pd.read_excel('2013.xlsx')  
# df1.columns = df2.columns

# #REMOVENDOS OS ACENTOS DAS LINHAS
# for i in range(len(df1)):
#     linha= df1.iloc[i,1]
#     linha_sem_acentos = unicodedata.normalize('NFD', linha).encode('ascii', 'ignore').decode('utf-8')
#     df1.iloc[i, 1] = linha_sem_acentos  
           
# df= pd.concat([df1,df2])

# month_name = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}

# df['MÊS NÚMERO']= df['MÊS'].dt.month
# df['MÊS NOME']= df['MÊS NÚMERO'].map(month_name)

# for i in range(len(df)):
#     df['ANO']= df['MÊS'].dt.year


# df1_semanal=pd.read_excel('semanal-estados-2004-a-2012.xlsx',skiprows=12)
# df2_semanal=pd.read_excel('semanal-estados-desde-2013.xlsx',skiprows=17)
# #REMOVENDOS OS ACENTOS DAS LINHAS
# for i in range(len(df1)):
#     linha= df1_semanal.iloc[i,4]
#     linha_sem_acentos = unicodedata.normalize('NFD', linha).encode('ascii', 'ignore').decode('utf-8')
#     df1_semanal.iloc[i, 4] = linha_sem_acentos  
       
# df_semanal= pd.concat([df1_semanal,df2_semanal])

# for i in range(len(df_semanal)):
#     df_semanal['ANO']= df_semanal['DATA FINAL'].dt.year

# #======================= SQL =======================
c= conn.cursor()

# #MENSAL ESTADO
# # df.index.name='ID'
# df.to_sql('MENSAL_ESTADO', conn, index_label='ID')

# # #SEMANAL ESTADO
# # df_semanal.index.name='ID'
# df_semanal.to_sql('SEMANAL_ESTADO', conn, index_label='ID')

# # #SELECT
# # c.execute('SELECT  PREÇO MÉDIO REVENDA,ESTADO,PRODUTO FROM MENSAL_ESTADO WHERE ESTADO = "ACRE" AND PRODUTO="GASOLINA COMUM"')
# # c.fetchone()
# # c.fetchall()
# # df_fetch= pd.DataFrame(c.fetchall())

# # query= 'SELECT PRODUTO FROM MENSAL_ESTADO'
# # df_query= pd.read_sql_query(query, conn).drop_duplicates()


# c.execute('DROP TABLE MENSAL_ESTADO')
# c.execute('DROP TABLE SEMANAL_ESTADO')

# #VAR AUX. 
uf_list= pd.read_sql_query('SELECT ESTADO FROM MENSAL_ESTADO',conn).drop_duplicates()['ESTADO'].tolist()
products_list= pd.read_sql_query('SELECT PRODUTO FROM MENSAL_ESTADO',conn).drop_duplicates()['PRODUTO'].tolist()
year_list = pd.read_sql_query('SELECT ANO FROM MENSAL_ESTADO',conn).drop_duplicates()['ANO'].tolist()


template_theme1='flatly'
template_theme2='darkly'
url_theme1=dbc.themes.FLATLY
url_theme2=dbc.themes.DARKLY
tab_card = {'height': '100%'}
main_config = {
    'hovermode': 'x unified',
    "margin": {"l":10,"r":10,"t":10,"b":10}
}
config_graph={"displayModeBar":False, "showTips":False}


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
                                html.I(className='fa fa-balance-scale', style={'font-size': '300%'})
                            ], sm=2,style={'margin-bottom': '5px;'}),
                            dbc.Col([
                                html.Legend('Fuel Price Brazil')
                            ], sm=8, align='center',style={'margin-bottom': '5px;'}),
                             dbc.Col([
                                ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2])
                            ],style={'margin-bottom': '5px;'})
                        ], style={'position':'relative', 'bottom':'7px'}),
                        
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
                                                dcc.Dropdown(
                                                options=[{'label': uf, 'value':uf} for uf in uf_list],
                                                id='dp-uf',
                                                value='RIO DE JANEIRO'
                                                ),
                                            ],sm=6),
                                            dbc.Col([
                                                html.Label('Produtos:'),
                                                dcc.Dropdown(
                                                    options=[{'label': product, 'value':product} for product in products_list],
                                                    id='dp-product',
                                                    value='GASOLINA COMUM'
                                                ),
                                            ],sm=6),
                                            
                                            dbc.Row([
                                                html.Hr(style={'margin-top':'15px'}),
                                                
                                                html.Label('Ano'),
                                                dcc.Slider(
                                                    min=2001,
                                                    max=2023,
                                                    marks=None,
                                                    value=2004,
                                                    step=1,
                                                    id='sd-year',
                                                    tooltip={"placement": "bottom", "always_visible": True} 
                                                )   
                                            ], style={'padding':' 0px 100px 0px 100px'})
                                            
                                        ])
                                    ])
                                ], style={**tab_card, 'padding': '0px 0px 33px 0px'})
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
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='graph_indicator_max', className='dbc', config=config_graph)
                            ])
                        ], style=tab_card)
                    ],sm=6),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='graph_indicator_min', className='dbc', config=config_graph)
                            ])
                        ], style=tab_card)
                    ],sm=6)
                ])
            ],md=4),
            
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='graph_dinamyc_week', className='dbc', config=config_graph)
                            ])
                        ], style=tab_card)
                    ],sm=12)
                ])
            ],md=8)
        ],className='g-2 my-auto', style={'margin-top': '7px'}),
        
        #ROW 3
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph_max_x_min_x_br', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ])
            ],md=4),
            
            dbc.Col([
                dbc.Row([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph_the_most_expensive', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ]),
            ],md=4),
            
            dbc.Col([
                dbc.Row([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph_region', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ])
            ],md=4)
        ],className='g-2 my-auto', style={'margin-top': '7px'})
        
])

#PRINCIPAL     
@app.callback(
    Output('graph-uf', 'figure'),
    Output('graph_indicator_max', 'figure'),
    Output('graph_indicator_min', 'figure'),
    Output('graph_max_x_min_x_br', 'figure'),
    Output('graph_dinamyc_week', 'figure'),
    Output('graph_the_most_expensive', 'figure'),
    Output('graph_region', 'figure'),
    
    Input('dp-uf', 'value'),
    Input('dp-product', 'value'),
    Input('sd-year', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'),'value'),

)    
def graph_select(uf,product,year,theme):
    
    var_graph_uf=graph_uf(uf,product,year,theme)
    var_graph_indicator_max=graph_indicator_max(uf,product,year,theme)
    var_graph_indicator_min=graph_indicator_min(uf,product,year,theme)
    var_map=select_map(uf,product,year,theme)
    var_graph_dinamyc_week=graph_dinamyc_week(uf,product,year,theme)
    var_graph_top_5_cheapest=graph_top_5_cheapest(uf,product,year,theme)
    var_graph_region=graph_region(product,year,theme)
    
    return var_graph_uf,var_graph_indicator_max,var_graph_indicator_min,var_map,var_graph_dinamyc_week,var_graph_top_5_cheapest,var_graph_region
    
def graph_uf(uf,product,year,theme):
    
    #VAR AUX
    # product ='GASOLINA COMUM'
    # year=2001
    # uf='SERGIPE'
    # theme='darkly'
    
    template = template_theme1 if theme else template_theme2
    
    query = f'''
        SELECT PRODUTO, ESTADO,ANO, "MÊS NÚMERO", "MÊS NOME", "PREÇO MÉDIO REVENDA" FROM MENSAL_ESTADO 
        WHERE PRODUTO = '{product}' AND ESTADO = '{uf}' AND ANO = {year}
    '''

    df_query = pd.read_sql_query(query, conn)
    
    # df_query.memory_usage(deep=True)
    # df_query.info()
    
    fig=px.bar(df_query, y='PREÇO MÉDIO REVENDA',x='MÊS NÚMERO',color='MÊS NOME')
    
    fig.update_layout(main_config, height=260, template=template)

    
    return fig

def graph_indicator_max(uf,product,year,theme):
    
    # product ='GASOLINA COMUM'
    # year=2003
    # uf='SERGIPE'
    # theme='darkly'
    
    template = template_theme1 if theme else template_theme2
    
    query = f'''
        SELECT PRODUTO, ESTADO,ANO, "MÊS NÚMERO", "MÊS NOME", "PREÇO MÉDIO REVENDA" FROM MENSAL_ESTADO 
        WHERE PRODUTO = '{product}' AND ESTADO = '{uf}' AND ANO = {year}
    '''
    
    query_anterior = f'''
        SELECT PRODUTO, ESTADO,ANO, "MÊS NÚMERO", "MÊS NOME", "PREÇO MÉDIO REVENDA" FROM MENSAL_ESTADO 
        WHERE PRODUTO = '{product}' AND ESTADO = '{uf}' AND ANO = {year-1}
    '''

    df_query = pd.read_sql_query(query, conn)
    df_query_anterior = pd.read_sql_query(query_anterior, conn)
    
    df_max=df_query.groupby('MÊS NOME',as_index=False)['PREÇO MÉDIO REVENDA'].max().sort_values(by='PREÇO MÉDIO REVENDA', ascending=False).head(1)
    
    #ANO ANTERIOR
    df_ano_interior=df_query_anterior[(df_query_anterior['ESTADO']==uf) & (df_query_anterior['PRODUTO']==product) & (df_query_anterior['ANO']==year-1) & (df_query_anterior['MÊS NOME']==df_max['MÊS NOME'].iloc[0])]
    
    
    variacao_porcentual_max= ((df_max['PREÇO MÉDIO REVENDA'].max() - df_ano_interior['PREÇO MÉDIO REVENDA'].max()) /  df_ano_interior['PREÇO MÉDIO REVENDA'].max()) * 100
    
    title_text = f'<span style="font-size:90%; margin-top: 100px;"><b>{df_max["MÊS NOME"].iloc[0]}</b> - MÊS MAIS <span style="color: red;">CARO</span></span>'
        
    fig_indicator_max= go.Figure(
            go.Indicator(
                mode='number+delta',
                title={'text':title_text},
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
        
    fig_indicator_max.update_layout(main_config, height=300, template=template)
        
        
    return fig_indicator_max
    
def graph_indicator_min(uf,product,year,theme):
    
    template = template_theme1 if theme else template_theme2
    
    # product ='GASOLINA COMUM'
    #year=2003
    # uf='SERGIPE'
    
    query = f'''
        SELECT PRODUTO, ESTADO,ANO, "MÊS NÚMERO", "MÊS NOME", "PREÇO MÉDIO REVENDA" FROM MENSAL_ESTADO 
        WHERE PRODUTO = '{product}' AND ESTADO = '{uf}' AND ANO = {year}
    '''
    
    query_anterior = f'''
        SELECT PRODUTO, ESTADO,ANO, "MÊS NÚMERO", "MÊS NOME", "PREÇO MÉDIO REVENDA" FROM MENSAL_ESTADO 
        WHERE PRODUTO = '{product}' AND ESTADO = '{uf}' AND ANO = {year-1}
    '''
    
    df_query = pd.read_sql_query(query, conn)
    df_query_anterior = pd.read_sql_query(query_anterior, conn)
    
    df_min=df_query.groupby('MÊS NOME',as_index=False)['PREÇO MÉDIO REVENDA'].min().sort_values(by='PREÇO MÉDIO REVENDA', ascending=True).head(1)
    
    #ANO ANTERIOR
    df_ano_interior=df_query_anterior[(df_query_anterior['ESTADO']==uf) & (df_query_anterior['PRODUTO']==product) & (df_query_anterior['ANO']==year-1) & (df_query_anterior['MÊS NOME']==df_min['MÊS NOME'].iloc[0])]
    
    variacao_porcentual_min= ((df_min['PREÇO MÉDIO REVENDA'].min() - df_ano_interior['PREÇO MÉDIO REVENDA'].min()) /  df_ano_interior['PREÇO MÉDIO REVENDA'].min()) * 100
    
    title_text = f'<span style="font-size:90%;"><b>{df_min["MÊS NOME"].iloc[0]}</b> - MÊS MAIS <span style="color: green;">BARATO</span></span>'

    fig_indicator_min= go.Figure(
            go.Indicator(
                mode='number+delta',
                title={'text':title_text},
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
        
    fig_indicator_min.update_layout(main_config, height=300, template=template)
    
    return fig_indicator_min
    
def select_map(uf,product,year,theme):
    
    template = template_theme1 if theme else template_theme2
    
    url_geojson_brasil_ibge = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
    gdf_brasil = gpd.read_file(url_geojson_brasil_ibge)
    

    gdf_brasil['name'] = [unicodedata.normalize('NFD', line.upper()).encode('ascii', 'ignore').decode('utf-8') for line in gdf_brasil['name']]
    
    
    gdf_select_uf = gdf_brasil[gdf_brasil['name'] == uf]
    

    fig = px.choropleth(
        gdf_brasil,
        geojson=gdf_brasil.geometry,

        locations=gdf_brasil.index,
        color=gdf_brasil['name'].apply(lambda x: 'blue' if x == uf else 'lightgreen'),

        color_discrete_map={'Acre': 'lightgreen', uf: 'blue'},  # Pinte o estado desejado de azul
        projection="mercator",
        hover_data=[]

    )
    
    
    fig.update_geos(
        center=dict(lon=-55, lat=-15),
        projection_scale=7,
        visible=False,
    )
    
    fig.update_layout(
        showlegend=False,
        legend_title_text='',
        coloraxis_colorbar=dict(
            title='',
            tickvals=[0, 1],
            ticktext=['Restante do País', uf],
        )
    )
    fig.update_layout(main_config, height=300, template=template)


    return fig
        
def graph_dinamyc_week(uf,product,year,theme):
    
    # product = 'GASOLINA COMUM'
    # uf='AMAZONAS'
    # year=2008
    # theme='darkly'
    
    template = template_theme1 if theme else template_theme2
    
    query = f'''
       SELECT ANO,PRODUTO,ESTADO,"DATA FINAL","PREÇO MÉDIO REVENDA" FROM SEMANAL_ESTADO WHERE ANO = {year} AND PRODUTO = "{product}" AND ESTADO = "{uf}"
    '''

    df_query = pd.read_sql_query(query, conn)
        
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df_query['DATA FINAL'],y=df_query['PREÇO MÉDIO REVENDA']))

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
    fig.update_layout(main_config, height=300, template=template)
    
    return fig    

def graph_top_5_cheapest(uf,product,year,theme):
    
    # product = 'GASOLINA COMUM'
    # uf='AMAZONAS'
    # year=2020
    # theme='darkly'
    
    template = template_theme1 if theme else template_theme2
    
    query = f'''
        SELECT PRODUTO,ESTADO,"PREÇO MÉDIO REVENDA","MÊS NÚMERO","MÊS NOME",ANO FROM MENSAL_ESTADO 
        WHERE PRODUTO = '{product}' AND ANO = {year}
    '''

    df_query = pd.read_sql_query(query, conn)
    
    df_=df_query[(df_query['ANO'] == year) & (df_query['PRODUTO'] == product)]
    
    df_=df_.groupby('ESTADO',as_index=False)['PREÇO MÉDIO REVENDA'].mean().sort_values(ascending=True,by='PREÇO MÉDIO REVENDA').head(5)
    
    fig = go.Figure()
    
    for i in range(len(df_)):
        estado=df_['ESTADO'].iloc[i]
        
        df_estado=df_query[(df_query['ESTADO']==estado) & (df_query['ANO'] == year) & (df_query['PRODUTO'] == product) ]
        
        fig.add_trace(go.Scatter(x=df_estado['MÊS NÚMERO'],y=df_estado['PREÇO MÉDIO REVENDA'], mode='lines+markers', name=df_estado['ESTADO'].iloc[0]))

    fig.update_layout(main_config, height=300, template=template)
    
    return fig

def graph_region(product,year,theme):
    
    query = f'''
        SELECT PRODUTO,ANO,REGIÃO,"PREÇO MÉDIO REVENDA" FROM MENSAL_ESTADO 
        WHERE PRODUTO = '{product}' AND ANO = {year}
    '''

    df_query = pd.read_sql_query(query, conn)
    
    template = template_theme1 if theme else template_theme2
          
    df_= df_query[(df_query['PRODUTO']==product) & (df_query['ANO']==year)]
            
    final_df=df_.groupby('REGIÃO',as_index=False)['PREÇO MÉDIO REVENDA'].mean()
        
    fig = px.bar(final_df, x='PREÇO MÉDIO REVENDA', y='REGIÃO', color='REGIÃO', orientation='h', barmode='group')
    
    fig.update_layout(main_config, height=300, template=template)
    
    return fig 
    

if __name__ == '__main__':
    app.run_server(debug=True,port=8061)