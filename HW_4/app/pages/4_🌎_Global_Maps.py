import streamlit as st
import pandas as pd
import numpy as np
import plotly.offline as py
import plotly.express as px
import plotly.graph_objs as go


st.write("# Средняя температура на глобусе и карте")
st.write("## Средняя температура на вращающемся глобусе")

st.markdown("""
Перед тем, как строить график, произведем некоторую обработку данных. Для начала удалим дублирующиеся страны. 
Найдем среднюю температуру для каждой страны, сделав группировку строк таблицы по колонке 'Country'.
    """)

temp_country = pd.read_csv(r'C:\Users\karlo\OneDrive\Desktop\Python_homeworks\Python_for_DA\ДЗ_4\app\data\GlobalLandTemperaturesByCountry.csv')

temp_country_clear = temp_country[~temp_country['Country'].isin(
    ['Denmark', 'Antarctica', 'France', 'Europe', 'Netherlands',
     'United Kingdom', 'Africa', 'South America'])]

temp_country_clear = temp_country_clear.replace(
   ['Denmark (Europe)', 'France (Europe)', 'Netherlands (Europe)', 'United Kingdom (Europe)'],
   ['Denmark', 'France', 'Netherlands', 'United Kingdom'])


# Найдем среднюю температуру для каждой страны
temp_country_clear_by_country = temp_country_clear.dropna(axis = 0).groupby(by= 'Country')[['AverageTemperature', 'AverageTemperatureUncertainty']].mean().reset_index()
countries = np.unique(temp_country_clear['Country'])
   
data = [ dict(
        type = 'choropleth',
        locations = countries,
        z = temp_country_clear_by_country['AverageTemperature'],
        locationmode = 'country names',
        text = countries,
        marker = dict(
            line = dict(#color = 'rgb(0,0,0)',
                         width = 1)),
            colorbar = dict(#autotick = True, tickprefix = '', 
            title = 'Average\nTemperature,\n°C')
            )
       ]

layout = dict(
    title = 'Average land temperature in countries',
    geo = dict(
        showframe = False,
        showocean = True,
        oceancolor = 'rgb(0,255,255)',
        projection = dict(
        type = 'orthographic',
            rotation = dict(
                    lon = 60,
                    lat = 10),
        ),
        lonaxis =  dict(
                showgrid = True,
                gridcolor = 'rgb(102, 102, 102)'
            ),
        lataxis = dict(
                showgrid = True,
                gridcolor = 'rgb(102, 102, 102)'
                )
            ),
        )

fig = dict(data=data, layout=layout)

#Streamlit plot
st.plotly_chart(fig)

st.write("## Средняя температура на интерактивной карте с анимацией в разные годы")

temp_country_clear['dt'] = pd.to_datetime(temp_country_clear.dt) 
temp_country_clear['year'] = temp_country_clear['dt'].dt.year
temp_country_clear_by_country_by_year = temp_country_clear.dropna(axis = 0).groupby(by = ['year', 'Country']).mean().reset_index()
temp_country_clear_by_country_by_year = temp_country_clear_by_country_by_year.sort_values(['year', 'Country'])

temp_country_clear_by_country_by_year['AverageTemperature+23'] = temp_country_clear_by_country_by_year['AverageTemperature'] + 23


fig = px.scatter_geo(temp_country_clear_by_country_by_year, locations='Country', locationmode='country names', color='AverageTemperature+23',
                     color_continuous_scale= 'Plasma',
                     hover_name="Country", size="AverageTemperature+23", size_max=20, opacity = 0.8,
                     animation_frame="year",
                     projection="natural earth", title='Interactive Globe Map - Average Temperature')

st.markdown("""
Предобработка данных так же состоит из удаления дублирующихся стран. 
Найдем среднюю температуру для каждой страны в каждый год, сделав группировку строк таблицы по колонкам 'Year' и 'Country'.
    """)
st.markdown('Минимальная температура равна -22.616, и поскольку значения карты не могут быть отрицательным, было добавлено 23 ко всем температурам, чтобы "стандартизировать данные"')

#Streamlit plot
st.plotly_chart(fig)
