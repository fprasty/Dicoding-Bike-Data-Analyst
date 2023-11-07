import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

data = pd.read_csv("main_data.csv") 

# Mengubah kolom 'dteday' menjadi datetime
data['dteday'] = pd.to_datetime(data['dteday'])

# Deskripsi cuaca
weather_desc = {
    1: "Clear, Few clouds, Partly cloudy",
    2: "Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist",
    3: "Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds",
    4: "Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog"
}

st.title("Bike Rental Dashboard")

# Date selection
start_date = st.date_input("Start Date", data['dteday'].min(), min_value=data['dteday'].min().date(), max_value=data['dteday'].max().date())
end_date = st.date_input("End Date", data['dteday'].max(), min_value=data['dteday'].min().date(), max_value=data['dteday'].max().date())

# Mengubah objek date menjadi datetime
start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.min.time())

# Checkbox untuk enable/disable weathersit filter
filter_weathersit = st.checkbox("Filter by Jenis Cuaca")
if filter_weathersit:
    selected_weather_code = st.selectbox("Pilih Jenis Cuaca", data['weathersit'].unique(), format_func=lambda code: weather_desc[code])
else:
    selected_weather_code = None

# Filter data berdasarkan pilihan date range dan weathersit
if selected_weather_code is not None:
    filtered_data = data[(data['dteday'] >= start_date) & (data['dteday'] <= end_date) & (data['weathersit'] == selected_weather_code)][['dteday', 'cnt', 'holiday', 'weekday', 'workingday', 'weathersit']]
else:
    filtered_data = data[(data['dteday'] >= start_date) & (data['dteday'] <= end_date)][['dteday', 'cnt', 'holiday', 'weekday', 'weathersit']]

# Hitung and jumlah total "cnt"
total_cnt = filtered_data['cnt'].sum()

# Tampilkan pilihan date range dan total "cnt"
st.markdown(f"**Date Range**: {start_date.strftime('%b %d, %Y')} to {end_date.strftime('%b %d, %Y')}")
if filter_weathersit:
    st.markdown(f"**Jenis Cuaca**: {selected_weather_code} - {weather_desc[selected_weather_code]}")
st.markdown(f"**Total Penyewa**: {total_cnt}")

# Tampilkan tabel dengan data yang sudah difilter
st.write("### Bike Rental Data")
st.dataframe(filtered_data)

# Dynamic line chart
st.write("### Bike Line Chart")

if filter_weathersit:
    chart_data = filtered_data[['dteday', 'cnt']]
else:
    chart_data = filtered_data[['dteday', 'cnt']]

line_chart = alt.Chart(chart_data).mark_line().encode(
    x=alt.X('dteday:T', title='Date Time'),
    y=alt.Y('cnt:Q', title='Jumlah Penyewa'),  
    tooltip=['dteday:T', alt.Tooltip('cnt:Q', title='Jumlah Penyewa')]  
).properties(
    width=900,
    height=500
)

st.altair_chart(line_chart)

