import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud 
import seaborn as sns 

st.set_page_config(layout="wide")

df = pd.read_csv('C:/Users/Marco/Documents/UNIVERSIDAD/4 SEMESTRE/PROYECTO INTEGRADOR/CODIGO/df/country_comparison_large_dataset_m.csv')

st.title("Analisis Exploratorios de datos por Pais")

st.sidebar.header("Filtros")

select_country = st.sidebar.multiselect('Seleccione el/los Paises', df['Country'].unique(), default=df['Country'].unique())

select_year = st.sidebar.selectbox("Seleccione el Año", df['Year'].unique())

select_variable = st.sidebar.selectbox("Seleccione una variable para las graficas", df.columns[2:])

df = df[(df['Country'].isin(select_country)) & (df['Year']>=select_year)]

if st.checkbox("Mostrar informacion del dataset"):
    with st.expander('Estadisticas descriptivas del Dataset'):
        st.subheader('Estadisticas descriptivas del Dataset')
        st.write(df.describe())
    with st.expander('Datos Originales'):
        st.subheader('Datos Originales')
        st.write(df)
        
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Distribucion del {select_variable}")
    st.write(f'Este grafico muestra la distribucion del {select_variable} por paises')
    fig_gdp = px.histogram(df, x = select_variable, nbins = 30, title = 'Distribucion del PIB')
    st.plotly_chart(fig_gdp)
with col2:
    st.subheader(f"Distrucion del {select_variable}") 
    st.write(f"Este grafico representa la distribucion del {select_variable}")
    fig_gdp_capita = px.box(df, x = 'Country', y = select_variable, title = f'Distribucion del {select_variable}', color = "Country")
    st.plotly_chart(fig_gdp_capita)  

with st.expander("Indicadores economicos"):
    st.subheader("Graficos de barras Indicadores")
    fig_gdp2 = px.bar(df, x = 'Country', y = select_variable, color = "Country", barmode = 'overlay', title = f'Barras de Pais vs {select_variable}')
    st.plotly_chart(fig_gdp2)    
    
with st.expander("Indicadores economicos"):
    st.subheader("Graficos de barras Indicadores")
    fig_gdp21 = px.bar(df, x = 'Country', y = select_variable, color = "Country", barmode = 'stack', title = f'Barras de Pais vs {select_variable}')
    st.plotly_chart(fig_gdp21)  
    
with st.expander("Indicadores economicos"):
    st.subheader("Graficos de barras Indicadores")
    fig_gdp23 = px.bar(df, x = 'Country', y = select_variable, color = "Country", barmode = 'relative', title = f'Barras de Pais vs {select_variable}')
    st.plotly_chart(fig_gdp23)
     
    
st.subheader(f'{select_variable} vs Esperanza de vida')
fig_scatter = px.scatter(df, x = select_variable, y = 'Life Expectancy (Years)', title = f"{select_variable} vs Esperanza de vida", color = "Country")
st.plotly_chart(fig_scatter)

st.subheader(f'Crecimient {select_variable} a lo largo del tiempo')
fig_line = px.line(df, x = 'Year', y = select_variable, color = 'Country', title = f"Crecimiento {select_variable} a lo largo del tiempo")
st.plotly_chart(fig_line)

st.subheader(f'Cuota de {select_variable} por pais')
fig_violin = px.violin(df, x = 'Country', y = select_variable, title = f'{select_variable} por pais', color = "Country")
st.plotly_chart(fig_violin)

st.subheader(f'Nube de Palabras de paises segun {select_variable}')
fig_cloud = dict(zip(df['Country'], df[select_variable]))
wordCloud = WordCloud(width = 800, height = 400, background_color = 'white')
wordCloud.generate_from_frequencies(fig_cloud)
plt.figure(figsize = (10,5))
plt.imshow(wordCloud, interpolation = 'bilinear')
plt.axis('off')
st.pyplot(plt)

st.subheader(f'GRafico de Barras {select_variable} por pais')
df_barras = df.groupby('Country')[select_variable].mean()
with st.expander(f'Datos agrupados por {select_variable}'):
    st.write(df_barras)
st.bar_chart(df_barras)
