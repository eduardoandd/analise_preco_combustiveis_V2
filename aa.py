import geopandas as gpd
import plotly.express as px

# Carregar o GeoJSON dos estados do Brasil
url_geojson_brasil_ibge = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
gdf_brasil = gpd.read_file(url_geojson_brasil_ibge)

# Adicionar coluna com a cor desejada
gdf_brasil['color'] = 'Restante do País'
gdf_brasil.loc[gdf_brasil['sigla'] == 'AC', 'color'] = 'Acre'

# Criar o mapa choropleth com cores e legenda personalizadas
fig = px.choropleth(
    gdf_brasil,
    geojson=gdf_brasil.geometry,
    locations=gdf_brasil.index,
    color='color',
    color_discrete_map={'Acre': 'blue', 'Restante do País': 'lightgreen'},
    projection="mercator",
)

# Configurar layout do mapa
fig.update_geos(
    center=dict(lon=-55, lat=-15),
    projection_scale=5,
    visible=False,
)

# Configurar legenda
fig.update_layout(
    legend_title_text='',
    coloraxis_colorbar=dict(
        title='',
        tickvals=[0, 1],
        ticktext=['Restante do País', 'Acre'],
    )
)

# Mostrar o mapa
fig.show()

