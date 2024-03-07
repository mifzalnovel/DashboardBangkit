import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data without using st.cache
data = pd.read_csv("data_clean.csv")

# Convert 'date' column to datetime format
data['date'] = pd.to_datetime(data['date'])

# Sort data by date
data = data.sort_values(by='date')

# Line plot for bike usage over time
st.title('Tren Penggunaan Sepeda Seiring Waktu')
st.line_chart(data.set_index('date')['total_count'])

# Add a new column 'season' based on the month
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

data['season'] = data['date'].dt.month.apply(get_season)

# Group data by season and calculate average bike rentals
grouped_data = data.groupby('season')['total_count'].mean().reset_index()

# Bar plot for average bike rentals per season
st.title('Rata-rata Jumlah Peminjaman Sepeda pada Setiap Musim')
st.bar_chart(grouped_data.set_index('season'))