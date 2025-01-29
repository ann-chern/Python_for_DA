import streamlit as st
import pandas as pd
import numpy as np
import plotly.offline as py
import plotly.express as px
import plotly.graph_objs as go
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

st.write("# Проверка гипотезы")
st.write("## Наблюдаем ли мы глобальное потепление?")

st.markdown(
"""
**Нулевая гипотеза ($H_0$)**: Средние значения температур не стационарны (имеют некоторую структуру, зависящую от времени). То есть средние значения температур за последние годы  отличаются от средних значений прошлых лет. Это означает наличие глобального потепления.

**Альтернативная гипотеза ($H_a$)**: Средние значения температур стационарны. То есть нет значимого изменения температуры со временем.
"""
            )

global_temp = pd.read_csv(r'C:\Users\karlo\OneDrive\Desktop\Python_homeworks\Python_for_DA\ДЗ_4\app\data\GlobalTemperatures.csv')
global_temp2 = global_temp.copy()
global_temp2['dt'] = pd.to_datetime(global_temp2.dt) # меняем тип колонки dt на datetime
global_temp2['year'] = global_temp2['dt'].dt.year

global_temp2 = global_temp2.set_index('dt') # делаем колонку dt индексом
global_temp2 = global_temp2.interpolate(method='time') # интерполяция пропущенных значений


def test_smoothed_trend(window_size=20, add_MA=True):
    series = global_temp2['LandAverageTemperature']
    if add_MA:
        series = series.rolling(window=window_size).mean()
    result = seasonal_decompose(series.dropna(), model='additive', period=12)
    trend = result.trend.dropna()
    adf_result = adfuller(trend)
    
    if adf_result[1] > 0.05:
        answer = f'Нельзя отклонить H_0: временной ряд нестационарен (p-value={adf_result[1]:.3f})'
    else:
        answer = f'Отклоненяем H_0: временной ряд является стационарным (p-value={adf_result[1]:.3f})'
    return answer
        

on = st.toggle("Добавить скользящее среднее", value=True)
# Interactive slider for moving average window
window_size = st.slider("Выберите размер окна скользящего среднего", min_value=1, max_value=50, value=5)     

if st.button('Проверить гипотезу о глобальном потеплении'):
    if on:   
        test_smoothed_trend(window_size=window_size, add_MA=True)
        st.write(f'При добавке скользящего среднего с окном размера {window_size} результат:')
        st.write(test_smoothed_trend(window_size=window_size, add_MA=True))
    else:
        test_smoothed_trend(add_MA=False)
        st.write(f'Без добавки скользящего среднего результат:')
        st.write(test_smoothed_trend(add_MA=False))

"""
```python
def test_smoothed_trend(window_size=20, add_MA=True):
    series = global_temp2['LandAverageTemperature']
    if add_MA:
        series = series.rolling(window=window_size).mean()
    result = seasonal_decompose(series.dropna(), model='additive', period=12)
    trend = result.trend.dropna()
    adf_result = adfuller(trend)
    
    if adf_result[1] > 0.05:
        print(f'Нельзя отклонить H_0: временной ряд нестационарен (p-value={adf_result[1]:.3f})')
    else:
        print(f'Отклоненяем H_0: временной ряд является стационарным (p-value={adf_result[1]:.3f})')
    
test_smoothed_trend()

```
"""





