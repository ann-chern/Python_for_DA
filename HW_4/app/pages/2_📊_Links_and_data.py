import streamlit as st
import pandas as pd

global_temp_city =  pd.read_csv(r'C:\Users\karlo\OneDrive\Desktop\Python_homeworks\Python_for_DA\ДЗ_4\app\data\GlobalLandTemperaturesByCity.csv')
global_temp_country =  pd.read_csv(r'C:\Users\karlo\OneDrive\Desktop\Python_homeworks\Python_for_DA\ДЗ_4\app\data\GlobalLandTemperaturesByCountry.csv')
global_temp =  pd.read_csv(r'C:\Users\karlo\OneDrive\Desktop\Python_homeworks\Python_for_DA\ДЗ_4\app\data\GlobalTemperatures.csv')

n = len(global_temp)
start = str(global_temp.dt.min())
stop = str(global_temp.dt.max())

st.header("Ссылка на источник данных")

name = 'Climate Change: Earth Surface Temperature Data'
url = 'https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data/data'
st.write(f"[{name}]({url})" )

st.header("Данные")
st.markdown("Выведем некоторые данные, с которыми была проведена работа в данном проекте")

f"""

Датасет содержит данные по температуре суши и океана с {start} по {stop} и состоит из {n} записей.

Чтобы прочитать датасет:

```python
import pandas as pd
global_temp = pd.read_csv('data/GlobalTemperatures.csv')
```
"""

st.dataframe(global_temp)

"""

Также имеется датасет, содержащий данные температуры по странам мира.

Чтобы прочитать датасет:

```python
import pandas as pd
global_temp_city = pd.read_csv('data/GlobalLandTemperaturesByCountry.csv')
```
"""

st.dataframe(global_temp_country)

"""

И датасет, содержащий данные температуры по некоторым городам мира.

Чтобы прочитать датасет:

```python
import pandas as pd
global_temp_city = pd.read_csv('data/GlobalLandTemperaturesByCity.csv')
```
"""

st.dataframe(global_temp_city[:800000])