import streamlit as st
import pandas as pd
import numpy as np

# Crear el DataFrame con valores faltantes
data = {
    'Producto': ['TV', 'Refrigerador', 'Smartphone', 'Auriculares', 'Laptop', 'Galletas', 'Cereal'],
    'Precio': [500, 800, np.nan, 50, 1200, 2, np.nan],
    'Ventas_Mensuales': [20, np.nan, 50, 200, np.nan, 500, np.nan],
    'Categoría': ['Electrónica', 'Electrónica', 'Electrónica', 'Electrónica', 'Electrónica', 'Alimentos', 'Alimentos'],
    'Inventario_Disponible': [15, 10, np.nan, 100, 5, 300, 150]
}

# Crear el DataFrame
df = pd.DataFrame(data)

# Mostrar el dataset original
st.write("Datos originales con valores faltantes:")
st.dataframe(df)

#1 eliminar filas con cualquier valor faltante
df_drop_rows = df.dropna()
st.dataframe(df_drop_rows)

#eliminar columnas faltantes
df_drop_cols = df.dropna(axis = 1)
st.dataframe(df_drop_cols)

# 3. Imputar valores faltantes con valores por defecto
df_fill_default = df.fillna({ #fillna rellena los nulos con:
    'Precio': 100,  # Rellenar valores faltantes en 'Precio' con 100
    'Ventas_Mensuales': 0,  # Rellenar valores faltantes en 'Ventas_Mensuales' con 0
    'Inventario_Disponible': 0  # Rellenar valores faltantes en 'Inventario_Disponible' con 0
})

# Mostrar el dataset después de rellenar con valores por defecto
st.write("Datos después de rellenar valores faltantes con valores por defecto:")
st.dataframe(df_fill_default)

# Guardar el DataFrame en un archivo CSV
if st.button('Guardar CSV'):
    file_path = 'df/datos_rellenados.csv'  # Cambia la ruta según sea necesario
    df_fill_default.to_csv(file_path, index=False)
    st.success(f'Dataset guardado en {file_path}')  