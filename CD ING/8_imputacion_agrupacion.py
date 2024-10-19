import streamlit as st
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar el DataFrame de ejemplo
df = pd.read_csv('C:\\Users\\Marco\\Documents\\UNIVERSIDAD\\4 SEMESTRE\\PROYECTO INTEGRADOR\\CODIGO\\df\\country_comparison_large_dataset.csv', delimiter=',')

# Título de la aplicación
st.title("Eliminación e Imputación de Valores por País")

# Selección del país desde un combo box
pais_seleccionado = st.selectbox('Seleccione un país', df['País'].unique())

# Filtrar el DataFrame por el país seleccionado
df_filtrado = df[df['País'] == pais_seleccionado]

# Mostrar las columnas disponibles para la eliminación de valores
columnas_disponibles = df_filtrado.columns.tolist()
columnas_a_eliminar = st.multiselect('Seleccione columnas para eliminar valores', columnas_disponibles[9:])

# Selección del porcentaje a eliminar
porcentaje_seleccionado = st.slider('Seleccione el porcentaje de valores a eliminar', min_value=0.1, max_value=0.4, step=0.05)

# Función para eliminar un porcentaje de valores de las columnas seleccionadas
def eliminar_porcentaje_valores(df, columnas, porcentaje):
    df_copy = df.copy()
    for col in columnas:
        total_filas = len(df_copy[col])
        num_eliminar = int(total_filas * porcentaje)
        
        if num_eliminar > 0:
            # Seleccionar índices aleatorios donde eliminar valores
            indices_a_eliminar = np.random.choice(df_copy.index, size=num_eliminar, replace=False)
            # Reemplazar esos valores con NaN
            df_copy.loc[indices_a_eliminar, col] = np.nan

    return df_copy

# Si se seleccionan columnas, aplicar la eliminación de valores
if len(columnas_a_eliminar) > 0:
    # Crear una copia del DataFrame para modificar
    df_modificado = eliminar_porcentaje_valores(df_filtrado, columnas_a_eliminar, porcentaje_seleccionado)

    # Mostrar el DataFrame modificado
    st.write("DataFrame con valores eliminados:")
    st.write(df_modificado)

    # Mostrar el promedio de las columnas originales (antes de la imputación)
    st.subheader("Promedio de las columnas antes de la imputación:")
    for col in columnas_a_eliminar:
        promedio_original = df_filtrado[col].mean()
        st.write(f"Promedio original de {col}: {promedio_original}")
        
    # Imputación de los valores eliminados utilizando la media
    #imputer = SimpleImputer(strategy='mean')
    #df_modificado[columnas_a_eliminar] = imputer.fit_transform(df_modificado[columnas_a_eliminar])
    
    from sklearn.experimental import enable_iterative_imputer  # Necesario para activar el iterador
    from sklearn.impute import IterativeImputer

    # Aplicar imputación con MICE
    imputer_mice = IterativeImputer(max_iter=10, random_state=0)
    df_modificado[columnas_a_eliminar]= imputer_mice.fit_transform(df_modificado[columnas_a_eliminar])
    
    # Redondear los valores imputados a dos decimales
    for col in columnas_a_eliminar:
        df_modificado[col] = df_modificado[col].round(2)

    # Mostrar el promedio de las columnas imputadas
    st.subheader("Promedio de las columnas después de la imputación:")
    for col in columnas_a_eliminar:
        promedio_imputado = df_modificado[col].mean()
        st.write(f"Promedio imputado de {col}: {promedio_imputado}")

    # Graficar la comparación de los datos actuales vs imputados usando Plotly Express
    st.subheader("Comparación de los datos originales e imputados (distribución con curva de Gauss):")
     
    # Crear una figura para el gráfico
    fig, ax = plt.subplots()

    # Graficar los datos originales e imputados con Seaborn
    for col in columnas_a_eliminar:
        sns.kdeplot(df_filtrado[col], label=f'{col} (Original)', ax=ax)
        sns.kdeplot(df_modificado[col], label=f'{col} (Imputado)', ax=ax)

    # Configurar el gráfico
    ax.set_title("Distribución de los valores originales vs imputados")
    ax.set_xlabel("Valor")
    ax.set_ylabel("Densidad")
    plt.legend()

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)


    # Opción para descargar el DataFrame modificado
    st.download_button(
        label="Descargar CSV",
        data=df_modificado.to_csv(index=False),
        file_name='datos_modificados.csv',
        mime='text/csv'
    )
    
else:
    st.write("Seleccione columnas para eliminar valores.")
