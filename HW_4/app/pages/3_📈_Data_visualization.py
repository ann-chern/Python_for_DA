import streamlit as st
import pandas as pd
import numpy as np
import plotly.offline as py
import plotly.express as px
import plotly.graph_objs as go


st.write("# Визуализация данных")

global_temp = pd.read_csv(r'C:\Users\karlo\OneDrive\Desktop\Python_homeworks\Python_for_DA\ДЗ_4\app\data\GlobalTemperatures.csv')
global_temp2 = global_temp.copy()
global_temp2['dt'] = pd.to_datetime(global_temp2.dt) # меняем тип колонки dt на datetime
global_temp2['year'] = global_temp2['dt'].dt.year
global_temp2 = global_temp2.set_index('dt') # делаем колонку dt индексом
global_temp2 = global_temp2.interpolate(method='time') # интерполяция пропущенных значений

st.write("## Скользящее среднее для средней температуры в мире с течением времени")
# Interactive slider for moving average window
window_size = st.slider("Выберите размер окна скользящего среднего", min_value=1, max_value=50, value=5)
global_temp2['Moving_Avg'] = global_temp2['LandAverageTemperature'].rolling(window=window_size).mean()

st.write(f"Применим скользящее среднее для сглаживания данных и устранения случайных колебаний с размером окна {window_size}")

on = st.toggle("Показывать исходные данные")

if on:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=global_temp2.index, y=global_temp2['LandAverageTemperature'], mode='lines', name='Original Data'))
    fig.add_trace(go.Scatter(x=global_temp2.index, y=global_temp2['Moving_Avg'], mode='lines', name='Moving Average'))
    fig.update_layout(title='Average Temperature in the world smoothed', xaxis_title='Year', yaxis_title='AverageTemperature')

    #Streamlit plot
    st.plotly_chart(fig)
else:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=global_temp2.index, y=global_temp2['Moving_Avg'], mode='lines', name='Moving Average'))
    fig.update_layout(title='Average Temperature in the world smoothed', xaxis_title='Year', yaxis_title='AverageTemperature', showlegend=True)

    #Streamlit plot
    st.plotly_chart(fig)

#
st.write("## Средняя температура в выбранный месяц")   
global_temp1 = global_temp.copy()
global_temp1['dt'] = pd.to_datetime(global_temp1['dt'])
global_temp1['year'] = global_temp1['dt'].map(lambda x: x.year)
global_temp1['month'] = global_temp1['dt'].map(lambda x: x.month)

min_year = global_temp1['year'].min()
max_year = global_temp1['year'].max()
years = np.arange(min_year, max_year + 1)

month_temps = []
month = st.number_input("Введите натуральное число до 12 - номер месяца для построения графика, например 1")
month = int(month)
    
for year in years:
    curr_years_data = global_temp1[global_temp1['year'] == year]
    month_temps.append(curr_years_data[curr_years_data['month'] == month]['LandAverageTemperature'].mean())
    
    
fig = go.Figure()
fig.add_trace(go.Scatter(x=years,y=month_temps,mode='lines'))
fig.update_layout(title=f'Average temperature in {month} month', xaxis_title='Year', yaxis_title='Average Temperature, °C')
    
#Streamlit plot
st.plotly_chart(fig)

st.write("## Средняя температура в выбранной стране")
temp_country = pd.read_csv(r'C:\Users\karlo\OneDrive\Desktop\Python_homeworks\Python_for_DA\ДЗ_4\app\data\GlobalLandTemperaturesByCountry.csv')
temp_country2 = temp_country.copy()
temp_country2['dt'] = pd.to_datetime(temp_country2.dt) # меняем тип колонки dt на datetime

temp_country2 = temp_country2.set_index('dt') # делаем колонку dt индексом
temp_country2 = temp_country2.interpolate(method='time') # интерполяция пропущенных значений
    
country = st.text_input("Введите название страны для построения графика, например Russia")
    
if country in temp_country["Country"].unique():
    filtered_temp_country = temp_country2[temp_country2["Country"] == country]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_temp_country.index, y=filtered_temp_country['AverageTemperature'], mode='lines'))
    fig.update_layout(title=f'Average Temperature in {country}', xaxis_title='Year', yaxis_title='AverageTemperature')

    #Streamlit plot
    st.plotly_chart(fig)
else:
    st.write('Такой страны нет в наборе данных')


