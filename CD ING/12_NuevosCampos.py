import pandas as pd
import streamlit as st
import numpy as np

# Crear un DataFrame con 5 vendedores, 10 productos y 50 registros

# Generar datos extendidos a 50 registros
vendedores = np.random.choice(['Carlos', 'Maria', 'Luis', 'Ana', 'Pedro'], 50)
productos = np.random.choice(['Bicicleta', 'Casco', 'Guantes', 'Rodilleras', 'Luz', 'Cadena', 'Frenos', 'Timbre', 'Manillar', 'Sillin'], 50)
regiones = np.random.choice(['Norte', 'Sur'], 50)
ventas = np.random.randint(100, 500, 50)
costos = ventas * np.random.uniform(0.6, 0.9, 50)

# Crear DataFrame de ejemplo con 50 registros
df = pd.DataFrame({
    'Vendedor': vendedores,
    'Producto': productos,
    'Región': regiones,
    'Ventas': ventas,
    'Costos': costos
})

# Mostrar el dataset original
st.write("### Dataset Original con 50 registros:")
st.dataframe(df)

### 1 Agregacion Simple
ventas_por_vendedor=df.groupby("Vendedor")["Ventas"].sum().reset_index()
st.write("### Ventas Totales por Vendedor")
st.dataframe(ventas_por_vendedor)
#### 2 Agregacion Multiple
ventas_agrupadas= df.groupby(['Vendedor','Región'])['Ventas'].agg(['sum','mean']).reset_index()
st.write("### Suma y Promedio de Ventas por Vendedor y Region")
st.dataframe(ventas_agrupadas)


# ####: Agregación con múltiples funciones ---
ventas_costos = df.groupby('Vendedor').agg(
    Total_Ventas=('Ventas', 'sum'),
    Total_Costos=('Costos', 'sum'),
    Promedio_Ventas=('Ventas', 'mean')
).reset_index()
st.write("### Suma de Ventas y Costos, y Promedio de Ventas por Vendedor:")
st.dataframe(ventas_costos)


######Nuevos Campos

##1 Crear nueva variable que sea Ganancia
df['Ganancia']= df['Ventas']-df['Costos']
st.write('### Despues de crear el nuevo cmapo Ganancia')
st.dataframe(df)

###### 2 Creacionn de variables categoricas
def clasificar_rentabilidad(g):
    if(g>200):
        return 'Alta'
    elif( g>100 ):
        return 'Media'
    else:
        return 'Baja'
    
df['Rentabilidad']= df['Ganancia'].apply(clasificar_rentabilidad)

st.write("##Crear el Campo Categorico Rentabilidad")

st.dataframe(df)


# 3. Crear una variable 'Costo_Por_Venta' (Costos / Ventas)
df['Costo_Por_Venta'] = df['Costos'] / df['Ventas']
st.write("### Después de Crear la Variable 'Costo_Por_Venta':")
st.dataframe(df)


# 4. Crear una variable 'Precio_Efectivo' que aplique un descuento del 10% a productos con ventas mayores a 300
df['Precio_Efectivo'] = df.apply(lambda row: row['Ventas'] * 0.9 if row['Ventas'] > 300 else row['Ventas'], axis=1)
st.write("### Después de Crear la Variable 'Precio Efectivo':")
st.dataframe(df)
