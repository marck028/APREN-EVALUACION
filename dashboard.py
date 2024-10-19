# Importar las librerías necesarias
import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar los datos
@st.cache
def load_data():
    df = pd.read_csv("C:\\Users\\Marco\\Downloads\\datos_modificados_maeci.csv")
    return df

# Cargar los datos
df = load_data()

# Título del dashboard
st.title("Dashboard de Ventas de Autos Eléctricos")

# Sidebar - Filtros de selección
st.sidebar.header("Filtros de Selección")

# Multiselección de filtros
year = st.sidebar.multiselect("Seleccionar Año:", df['year'].unique(), default=df['year'].unique().tolist())
mode = st.sidebar.multiselect("Seleccionar Modo:", df['mode'].unique(), default=df['mode'].unique().tolist())
powertrain = st.sidebar.multiselect("Seleccionar Powertrain:", df['powertrain'].unique(), default=df['powertrain'].unique().tolist())

# Filtrar los datos según las selecciones del usuario
filtered_data = df.copy()
if year:
    filtered_data = filtered_data[filtered_data['year'].isin(year)]
if mode:
    filtered_data = filtered_data[filtered_data['mode'].isin(mode)]
if powertrain:
    filtered_data = filtered_data[filtered_data['powertrain'].isin(powertrain)]

# Mostrar los datos filtrados
st.write("Datos Filtrados", filtered_data)

# Gráficos
st.header("Visualizaciones")

# Gráfico 1: Clasificación por Volumen de Ventas
st.subheader("Clasificación por Volumen de Ventas")
sales_by_powertrain = filtered_data.groupby('powertrain')['sales_volume'].sum().reset_index()
fig_sales_powertrain = px.bar(sales_by_powertrain, x='powertrain', y='sales_volume',
                               title="Clasificación por Volumen de Ventas por Powertrain", 
                               color='sales_volume', text='sales_volume',
                               hover_data=['sales_volume'])  # Datos al pasar el cursor
st.plotly_chart(fig_sales_powertrain)

# Gráfico 2: Clasificación por Precio
st.subheader("Clasificación por Precio")
price_by_mode = filtered_data.groupby('mode')['price'].mean().reset_index()
fig_price_mode = px.bar(price_by_mode, x='mode', y='price',
                         title="Precio Promedio por Modo", 
                         color='price', text='price',
                         hover_data=['price'])  # Datos al pasar el cursor
st.plotly_chart(fig_price_mode)

# Gráfico 3: Tendencias de Ventas por Año
st.subheader("Tendencias de Ventas por Año")
sales_trends = filtered_data.groupby('year')['sales_volume'].sum().reset_index()
fig_sales_trends = px.line(sales_trends, x='year', y='sales_volume',
                            title="Tendencias de Ventas por Año",
                            markers=True, hover_data=['sales_volume'])  # Datos al pasar el cursor
st.plotly_chart(fig_sales_trends)

# Gráfico 4: Relación entre Precio y Eficiencia Energética
st.subheader("Relación entre Precio y Eficiencia Energética")
fig_price_efficiency = px.scatter(filtered_data, x='price', y='energy_efficiency',
                                   color='powertrain', 
                                   title="Relación entre Precio y Eficiencia Energética",
                                   hover_data=['powertrain', 'sales_volume'])  # Datos al pasar el cursor
st.plotly_chart(fig_price_efficiency)

# Gráfico 5: Distribución de Precios (Univariado)
st.subheader("Distribución de Precios")
fig_price_distribution = px.histogram(filtered_data, x='price', 
                                       title="Distribución de Precios",
                                       nbins=30, hover_data=['price'])  # Datos al pasar el cursor
st.plotly_chart(fig_price_distribution)

# Gráfico 6: Boxplot de Ventas por Tipo de Modo (Bivariado)
st.subheader("Boxplot de Ventas por Tipo de Modo")
fig_boxplot_sales = px.box(filtered_data, x='mode', y='sales_volume',
                            title="Distribución de Ventas por Tipo de Modo",
                            hover_data=['sales_volume'])  # Datos al pasar el cursor
st.plotly_chart(fig_boxplot_sales)

# Filtrar datos para el gráfico multivariado asegurando que no hay valores negativos
filtered_multivariate = filtered_data[filtered_data['battery_capacity'] >= 0]

# Gráfico 7: Gráfico de Dispersión (Multivariado)
st.subheader("Gráfico de Dispersión de Ventas, Precio y Eficiencia Energética")
fig_multivariate = px.scatter(filtered_multivariate, x='price', y='sales_volume',
                               size='battery_capacity', color='powertrain',
                               hover_name='mode', title="Relación entre Precio, Ventas y Capacidad de Batería",
                               size_max=20)  # Tamaño por capacidad de batería
st.plotly_chart(fig_multivariate)

# Gráfico 8: Relación entre CO2 Ahorrado y Ventas
st.subheader("Relación entre CO2 Ahorrado y Ventas")
fig_co2_sales = px.scatter(filtered_data, x='co2_saved', y='sales_volume',
                            color='powertrain', 
                            title="Relación entre CO2 Ahorrado y Ventas",
                            hover_data=['co2_saved', 'sales_volume'])  # Datos al pasar el cursor
st.plotly_chart(fig_co2_sales)

st.subheader("Relación entre Precio y Rango de Carga")
fig_price_range = px.scatter(filtered_data, x='price', y='range_km',
                              color='powertrain',
                              title="Relación entre Precio y Rango de Carga",
                              hover_data=['mode'])
st.plotly_chart(fig_price_range)

st.subheader("Eficiencia Energética Promedio a lo Largo de los Años")
efficiency_trends = filtered_data.groupby('year')['energy_efficiency'].mean().reset_index()
fig_efficiency_trends = px.line(efficiency_trends, x='year', y='energy_efficiency',
                                 title="Tendencias de Eficiencia Energética por Año",
                                 markers=True)
st.plotly_chart(fig_efficiency_trends)

st.subheader("Distribución de Capacidad de Batería")
fig_battery_capacity = px.histogram(filtered_data, x='battery_capacity', nbins=30,
                                     title="Distribución de Capacidad de Batería",
                                     hover_data=['battery_capacity'])
st.plotly_chart(fig_battery_capacity)

st.subheader("CO2 Ahorrado por Powertrain")
co2_by_powertrain = filtered_data.groupby('powertrain')['co2_saved'].sum().reset_index()
fig_co2_powertrain = px.bar(co2_by_powertrain, x='powertrain', y='co2_saved',
                             title="Total de CO2 Ahorrado por Powertrain",
                             color='co2_saved', text='co2_saved')
st.plotly_chart(fig_co2_powertrain)

st.subheader("Distribución de Peso por Powertrain")
fig_boxplot_weight = px.box(filtered_data, x='powertrain', y='weight_kg',
                             title="Distribución del Peso de Vehículos por Powertrain")
st.plotly_chart(fig_boxplot_weight)

st.subheader("Distribución de Peso por Powertrain")
fig_boxplot_weight = px.box(filtered_data, x='powertrain', y='weight_kg',
                             title="Distribución del Peso de Vehículos por Powertrain")
st.plotly_chart(fig_boxplot_weight)

st.subheader("Comparación de Ventas por Año y Powertrain")
sales_by_year_powertrain = filtered_data.groupby(['year', 'powertrain'])['sales_volume'].sum().reset_index()
fig_sales_year_powertrain = px.bar(sales_by_year_powertrain, x='year', y='sales_volume',
                                    color='powertrain', title="Ventas de Vehículos por Año y Powertrain",
                                    barmode='group')
st.plotly_chart(fig_sales_year_powertrain)
