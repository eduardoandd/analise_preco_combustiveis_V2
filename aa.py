import plotly.graph_objects as go

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_us_cities.csv')
df.head()

df['text'] = df['name'] + '<br>Population ' + (df['pop']/1e6).astype(str)+' million'
limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
cities = []
scale = 5000

fig = go.Figure()

fig.add_trace(go.Scattergeo(
    locationmode= 'USA-states',
    lat=[-9.974],
    lon=[-67.8076],
    text='ACRE',
))

fig.update_layout(
    title_text='2023',
    showlegend=True,
    geo = dict(
        scope='south america',
        landcolor= 'rgb(217, 217, 217)',
    )
)



