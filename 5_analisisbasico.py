import streamlit as st
import pandas as pd

st.title('Análisis de Datos')

uploaded_file = st.file_uploader('Subir Archivo CSV', type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='UTF-8', delimiter=',')
    
    st.subheader('Primeras Filas del Dataset')
    st.dataframe(df.head())
    
    st.subheader('Resumen Estadístico')
    st.write(df.describe())
    
    st.subheader('Nombres de las Columnas')
    st.write(df.columns)
    
    st.subheader('Tipos de Datos')
    st.write(df.dtypes)
    
    st.subheader('Tamaño del Dataset')
    st.write(df.shape)

    st.subheader('Valores Nulos en el Dataset')
    st.write(df.isnull().sum())
    
    st.subheader('Filas Duplicadas')
    st.write(df.duplicated().sum())

    # Comprobación de valores atípicos
    st.subheader('Valores Atípicos')
    for column in df.select_dtypes(include=['float64', 'int64']).columns:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        if not outliers.empty:
            st.write(f'Valores atípicos en la columna {column}:')
            st.dataframe(outliers)

    # Comprobación de tipos de datos inconsistentes
    st.subheader('Comprobación de Tipos de Datos Inconsistentes')
    for column in df.columns:
        if df[column].dtype == 'object':
            unique_values = df[column].unique()
            st.write(f'Valores únicos en la columna {column}: {unique_values}')
    
else:
    st.write('No hay archivo subido')
