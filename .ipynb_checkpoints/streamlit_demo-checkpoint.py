# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 08:43:41 2023

@author: herbort
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Pfad zur CSV-Datei
DATA_URL = "./data/imdb_ratings.csv"

st.title('Movie Analysis Dashboard')

@st.cache_data
def load_data():
    """
    Funktion zum Laden der Daten aus einer CSV-Datei.
    Die Daten werden zwischengespeichert, um die Leistung zu verbessern.
    """
    data = pd.read_csv(DATA_URL)
    return data

# Daten laden
data = load_data()

# Filter für Jahr, Bewertung, x- und y-Achse
# Multiselect für die Auswahl der Jahre
years = st.multiselect('Choose Years', data['Year'].unique())

# Slider für die Auswahl des Bewertungsbereichs
rating = st.slider('Choose Rating', 
                   min_value=float(data['Rating'].min()), 
                   max_value=float(data['Rating'].max()), 
                   value=(float(data['Rating'].min()), float(data['Rating'].max())))

# Dropdown-Menü für die Auswahl der x-Achsenvariable
x_axis = st.selectbox('Choose x variable', data.columns, index=list(data.columns).index('Runtime (Minutes)'))

# Dropdown-Menü für die Auswahl der y-Achsenvariable
y_axis = st.selectbox('Choose y variable', data.columns, index=list(data.columns).index('Metascore'))

# Radio-Button zur Auswahl der Punktgröße nach Umsatz
size_by_revenue = st.radio('Size by Revenue', ('No Size', 'Size by Revenue'))

# Daten nach Jahr und Bewertung filtern
filtered_data = data[(data['Year'].isin(years)) & 
                     (data['Rating'] >= rating[0]) & 
                     (data['Rating'] <= rating[1])]

# Scatterplot erstellen mit Plotly
if size_by_revenue == 'Size by Revenue' and 'Revenue (Millions)' in data.columns:
    # Wenn die Größe der Punkte durch den Umsatz bestimmt wird
    fig = px.scatter(filtered_data, x=x_axis, y=y_axis, 
                     size='Revenue (Millions)',
                     labels={x_axis: x_axis, y_axis: y_axis},
                     title='Scatterplot')
else:
    # Wenn die Größe der Punkte nicht durch den Umsatz bestimmt wird
    fig = px.scatter(filtered_data, x=x_axis, y=y_axis, 
                     size_max=10,
                     labels={x_axis: x_axis, y_axis: y_axis},
                     title=f'Scatterplot of {y_axis} vs {x_axis}')

# Scatterplot in Streamlit anzeigen
st.plotly_chart(fig)

