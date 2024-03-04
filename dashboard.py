import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data without using st.cache
data = pd.read_csv("hour.csv").copy()

# Add a title to the app
st.title("Bikeshare Data Analysis Dashboard")

# Show the raw data
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.write(data)

# Data preprocessing
st.subheader("Data Preprocessing")

# Check for duplicates
if st.checkbox("Check for Duplicates"):
    duplicate_count = data.duplicated().sum()
    st.write(f"Number of duplicates: {duplicate_count}")

# Describe the data
st.subheader("Data Description")
st.write(data.describe())

# Convert data types
st.subheader("Convert Data Types")

data['date'] = pd.to_datetime(data['dteday'])
data['season'] = data['season'].astype('category')
data['month'] = data['mnth'].map({1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}).astype('category')
data['holiday'] = data['holiday'].astype('category')
data['weekday'] = data['weekday'].astype('category')
data['workingday'] = data['workingday'].astype('category')
data['weather'] = data['weathersit'].map({1:'Clear', 2:'Misty', 3:'Light_RainSnow', 4:'Heavy_RainSnow'}).astype('category')


# Drop unnecessary columns
data = data.drop("instant", axis=1)

# Rename columns
data.rename(columns={
    "dteday" : "date",
    "yr" : "year",
    "mnth" : "month",
    "weathersit" : "weather",
    "hum" : "humidity",
    "cnt" : "total_count"}, inplace=True
)

# Convert values for categorical columns
data['season'].replace((1,2,3,4), ('Winter','Spring','Summer','Fall'), inplace=True)
data['year'].replace((0,1), (2011,2012), inplace=True)
data['month'].replace((1,2,3,4,5,6,7,8,9,10,11,12),('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'), inplace=True)
data['weather'].replace((1,2,3,4), ('Clear','Misty','Light_RainSnow','Heavy_RainSnow'), inplace=True)
data['weekday'].replace((0,1,2,3,4,5,6), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'), inplace=True)
data['workingday'].replace((0,1), ('No', 'Yes'), inplace=True)

# Normalize numerical columns
data['temp'] = data['temp']*41
data['atemp'] = data['atemp']*50
data['humidity'] = data['humidity']*100
data['windspeed'] = data['windspeed']*67

# Visualization
st.header("Data Visualization")

# Histograms
st.subheader("Histograms")
columns = ['casual', 'registered', 'total_count']
fig, ax = plt.subplots(1, 3, figsize=(10,5))
for i, ax in enumerate(ax):
    sns.histplot(x=data[columns[i]], ax=ax, bins=10, color='red')
    ax.set_title(columns[i])
    ax.set_xlabel("")
    ax.set_ylabel("")
st.pyplot(fig)

# Boxplots
st.subheader("Boxplots")
fig, ax = plt.subplots(1, 3, figsize=(10,5))
for i, ax in enumerate(ax):
    sns.boxplot(y=data[columns[i]], ax=ax, color='red')
    ax.set_title(columns[i])
    ax.set_xlabel("")
    ax.set_ylabel("")
st.pyplot(fig)

# Boxplot by season
st.subheader("Boxplot by Season")
plt.figure(figsize=(10, 6))
season_boxplot = sns.boxplot(x="season", y="total_count", data=data, palette=["red", "lightcoral"])
season_boxplot.set_xlabel("Season")
season_boxplot.set_ylabel("Total Rides")
season_boxplot.set_title("Total bikeshare rides by Season")
st.pyplot(plt.gcf())
