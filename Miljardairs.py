#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import folium
from streamlit_folium import st_folium


# Assuming you've defined the 'load_data' function as before
@st.experimental_singleton
def load_data():
    data = pd.read_csv('Billionaires Statistics Dataset.csv').head(100)
    data['age'] = data['age'].astype(int)
    return data

# Loading the data
df = load_data()
df1=pd.read_csv('Billionaires Statistics Dataset.csv')
df['finalWorth'] = df['finalWorth']/1000
df1['finalWorth'] = df1['finalWorth']/1000
# Defining your plotting functions
def plot_count(column, df):
    plt.figure(figsize=(10, 6))
    sns.countplot(x=column, data=df)
    plt.title(f'Count Plot of {column}')
    plt.xlabel(column)
    plt.ylabel('Count')
    st.pyplot(plt.gcf())

def plot_boxplot(column, df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df[column])
    plt.title(f'Boxplot of {column}')
    st.pyplot(plt.gcf())

def plot_scatter(x, y, df):
    # Create a select box for user to filter on 'selfMade' column
    unique_values = df['selfMade'].unique()
    selected_value = st.selectbox('Filter by selfMade:', options=unique_values)

    # Filter the dataframe based on the selected value for 'selfMade'
    filtered_df = df[df['selfMade'] == selected_value]

    # Create the scatter plot with the filtered data and color by 'category'
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=filtered_df, x=x, y=y, hue='category', palette='tab10', ax=ax)
    ax.set_title(f'{x} vs {y} Scatter Plot filtered by selfMade: {selected_value}')
    ax.set_xlabel(x)
    ax.set_ylabel(y)

    # Place the legend outside the plot
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
    
    # Ensure the plot displays without being cut-off
    plt.tight_layout()

    st.pyplot(fig)
    
def inspect_1d(df, column):
    fig, ax = plt.subplots(figsize=(10, 6))  # Streamlit requires the use of Matplotlib's Figure and Axes objects
    sns.countplot(y=column, data=df, ax=ax)
    ax.set_title(f'Count Plot of {column}')
    st.pyplot(fig) 
    
# Streamlit Sidebar for page selection
st.sidebar.title("Billionaires Dashboard")
page = st.sidebar.selectbox("Choose a view", 
                            ["Overview", "Dutch Billionaires",  "Dutch Billionaires Map","Top 100 Billionaires", "Self-Made Distribution", "Age Distribution", "Age vs Worth Scatter", "Wealth vs Self-Made", "Industry categories"])

if page == "Top 100 Billionaires":
    st.title("Top 100 Billionaires")
    # Get user input
    search_term = st.text_input('Search by name:')

    # Filter the DataFrame based on the search term
    if search_term:
        # Using .str.contains() to filter the DataFrame
        filtered_df = df[df['personName'].str.contains(search_term, case=False, na=False)]
    else:
        # When there is no search term, display the original DataFrame
        filtered_df = df
    st.table(filtered_df[['personName', 'age', 'finalWorth', 'selfMade', 'category']])

elif page == "Self-Made Distribution":
    st.title("Distribution of Self-Made Billionaires")
    plot_count('selfMade', df)
elif page == "Industry categories":
    st.title("Industry categories")
    inspect_1d(df, 'category') 
elif page == "Age Distribution":
    st.title("Age Distribution of Billionaires")
    plot_boxplot('age', df)
elif page == "Age vs Worth Scatter":
    st.title("Age vs Final Worth of Billionaires")
    plot_scatter('age', 'finalWorth', df)
elif page == "Wealth vs Self-Made":
    st.title("Final Worth vs Self-Made Status")
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='selfMade', y='finalWorth', data=df)
    plt.title('Boxplot of Final Worth segmented by Self-Made')
    st.pyplot(plt.gcf())
elif page == "1D Inspections":
    st.title("1D Inspections")
    inspect_1d(df, 'category') 
    
# Overview page
elif page == "Overview":
    st.title('Bronnen:')
    st.write('Dataset: https://www.kaggle.com/datasets/nelgiriyewithana/billionaires-statistics-dataset')
    st.title("Miljardairs Dashboard")
    st.write('Henrik Bout & Roien Ghorbanzadeh')
    st.header("Overzicht van alle miljardairs")

    fig = px.bar(df1, x=df1.index, y='finalWorth', title='Histogram van alle Miljardairs')
    fig.update_yaxes(title_text="Vermogen (in miljarden USD)")
    # fig.show()
    st.plotly_chart(fig)
    
    
    # Assuming you want a scatter plot here:
    fig = px.scatter(df1, x='age', y='finalWorth', title='Scatterplot Leeftijd vs Vermogen')
    fig.update_xaxes(title_text='Leeftijd')
    fig.update_yaxes(title_text='Vermogen in Miljard USD')
    st.plotly_chart(fig)
    
    st.title("Boxplots op basis van Leeftijd of Vermogen")
# Voeg een dropdown-menu toe om te selecteren op basis van welke kolom je de boxplots wilt zien
    selectie = st.selectbox("Selecteer op basis van welke kolom:", ['Leeftijd', 'Vermogen'])
    # Maak de boxplot op basis van de selectie
    if selectie == 'Leeftijd':
        fig = px.box(df1, x='gender', y='age', title='Boxplot van Leeftijd gesorteerd op Geslacht')
        fig.update_xaxes(title_text="Geslacht")
        fig.update_yaxes(title_text="Leeftijd")
    elif selectie == 'Vermogen':
        fig = px.box(df1, x='gender', y='finalWorth', title='Boxplot van Vermogen gesorteerd op Geslacht')
        fig.update_xaxes(title_text="Geslacht")
        fig.update_yaxes(title_text="Vermogen")
    st.plotly_chart(fig)
        
        # Streamlit-app
    st.title("Histogram met dropdown-menu")
        # Voeg een dropdown-menu toe om te selecteren op welke gegevens je het histogram wilt weergeven
    selectie = st.selectbox("Selecteer de gegevens:", ['Aantal mannen en vrouwen', 'Aantal miljardairs per land', 'Aantal miljardairs per industrie', 'Aantal miljardairs per status'])

        # Maak het histogram op basis van de selectie
    if selectie == 'Aantal mannen en vrouwen':
        fig = px.histogram(df1, x='gender', title='Histogram van Aantal Mannen en Vrouwen')
        fig.update_xaxes(title_text="Geslacht")
        fig.update_yaxes(title_text="Aantal")
    elif selectie == 'Aantal miljardairs per land':
        fig = px.histogram(df1, x='country', title='Histogram van Aantal Miljardairs per Land')
        fig.update_xaxes(title_text="Land")
        fig.update_yaxes(title_text="Aantal")
    elif selectie == 'Aantal miljardairs per industrie':
        fig = px.histogram(df1, x='industries', title='Histogram van Aantal Miljardairs per Industrie')
        fig.update_xaxes(title_text="Industrie")
        fig.update_yaxes(title_text="Aantal")
    elif selectie == 'Aantal miljardairs per status':
        fig = px.histogram(df1, x='status', title='Histogram van Aantal Miljardairs per Status')
        fig.update_xaxes(title_text="Status")
        fig.update_yaxes(title_text="Aantal")

    # Toon het geselecteerde histogram
    st.plotly_chart(fig)

# Self-Made Distribution page
elif page == "Self-Made Distribution":
    st.title("Distribution of Self-Made Billionaires")
    plot_count('selfMade', df)

 
# Dutch Billionaires page
elif page == "Dutch Billionaires":

    dfnl = df1[df1['countryOfCitizenship']=='Netherlands'].reset_index()
   
    st.header("Overzicht van Nederlandse miljardairs")
    st.title("Histogram van Nederlandse Miljardairs op basis van vermogen")
    fig = px.bar(dfnl, x=dfnl.index, y='finalWorth', title='Histogram van Nederlandse Miljardairs')
    fig.update_yaxes(title_text="Vermogen (in miljarden USD)")
    fig.update_xaxes(title_text="Ranking NL Miljardairs")
    # fig.show()
    st.plotly_chart(fig)
    
    # Streamlit-app
    st.title("Histogrammen van Nederlandse Miljardairs")
    # Voeg een dropdown-menu toe om te selecteren op welke gegevens je het histogram wilt weergeven
    selectie = st.selectbox("Selecteer de gegevens:", ['Mannen vs Vrouwen', 'Industrie','Leeftijd', 'Status'])

    # Maak het histogram op basis van de selectie
    if selectie == 'Mannen vs Vrouwen':
        fig = px.histogram(dfnl, x='gender', title='Histogram van Aantal Mannen vs Vrouwen')
        fig.update_xaxes(title_text="Geslacht")
        fig.update_yaxes(title_text="Aantal")
    elif selectie == 'Industrie':
        fig = px.histogram(dfnl, x='industries', title='Histogram van Aantal Miljardairs per Industrie')
        fig.update_xaxes(title_text="Industrie")
        fig.update_yaxes(title_text="Aantal")
    elif selectie == 'Leeftijd':
        fig = px.bar(dfnl, x='age', y='personName', title='Histogram van leeftijd')
        fig.update_xaxes(title_text= "Leeftijd")
        fig.update_yaxes(title_text= "Naam")
    elif selectie == 'Status':
        fig = px.histogram(dfnl, x='status', title='Histogram van Aantal Miljardairs per Status')
        fig.update_xaxes(title_text="Status")
        fig.update_yaxes(title_text="Aantal")

# Toon het geselecteerde histogram
    st.plotly_chart(fig)

elif page == "Dutch Billionaires Map":
  
    dfnl = df1[df1['countryOfCitizenship']=='Netherlands'].reset_index()
    
    st.title('Kaart met Nederlandse Miljardairs')
    st.write('Klik op de popup voor informatie over de Miljardair')
    m = folium.Map([52.0893191, 5.1101691], zoom_start=7)



    # Voeg markers toe aan de kaart
    folium.Marker(location=[51.508523192296124, -0.11950854824384642], popup='<b>Charlene de Carvalho-Heineken & family, Rank: 119, Vermogen: 14,7 Miljard  </b>', tooltip='Charlene de Carvalho-Heineken & family').add_to(m)
    folium.Marker(location=[52.36246586231535, 4.8917783082531665], popup='<b>Frits Goldschmeding Rank: 411, Vermogen: 6,2 Miljard  </b>', tooltip='Frits Goldschmeding').add_to(m)
    folium.Marker(location=[51.438994243547334, 5.471407445694404], popup='<b>Wim van der Leegte & family Rank: 818, Vermogen: 3,5 Miljard  </b>', tooltip='Wim van der Leegte & family').add_to(m)
    folium.Marker(location=[52.105696091639054, 6.311631231296584], popup='<b> Hans Melchers Rank: 1164, Vermogen: 2.6 Miljard  </b>', tooltip='Hans Melchers ').add_to(m)
    folium.Marker(location=[52.37151754926965, 4.893261581601775], popup='<b> Arnout Schuijff Rank: 1272, Vermogen: 2,4 Miljard  </b>', tooltip='Arnout Schuijff').add_to(m)
    folium.Marker(location=[52.277275366997735, 5.233716948637874], popup='<b>John de Mol, Rank: 1647, Vermogen: 1,8 Miljard  </b>', tooltip='John de Mol').add_to(m)
    folium.Marker(location=[52.37673930324946, 4.886757384656176], popup='<b>Adriaan Mol, Rank: 1647, Vermogen: 1,8 Miljard  </b>', tooltip='Adriaan Mol').add_to(m)
    folium.Marker(location=[52.3783, 4.9031], popup='<b>Lesley Bamberger, Rank: 1725, Vermogen: 1,7 Miljard  </b>', tooltip='Lesley Bamberger').add_to(m)
    folium.Marker(location=[51.836200018540616, 4.9750231783638625], popup='<b>Kommer Damen, Rank: 1725, Vermogen: 1,7 Miljard  </b>', tooltip='Kommer Damen').add_to(m)
    folium.Marker(location=[37.76448552544274, -122.41923223352154], popup='<b>Sytse Sijbrandij, Rank: 2259, Vermogen: 1,2 Miljard  </b>', tooltip='Sytse Sijbrandij').add_to(m)
    folium.Marker(location=[52.211453541929906, 5.286181340084006], popup='<b>Joop van den Ende, Rank: 2259, Vermogen: 1,2 Miljard  </b>', tooltip='Joop van den Ende').add_to(m)

    # Toon de kaart
    # m
    st_data = st_folium(m, width=725)

# Now you will have to define all pages like above and at the end of the file, you run:
# streamlit run your_script.py


# In[1]:


#pip install plotly


# In[ ]:




