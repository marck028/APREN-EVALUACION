import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

# Crear el DataFrame con valores faltantes
data = {
    'Producto': ['TV', 'Refrigerador', 'Smartphone', 'Auriculares', 'Laptop', 'Galletas', 'Cereal'],
    'Precio': [500, 800, np.nan, 50, 1200, 2, np.nan],
    'Ventas_Mensuales': [20, np.nan, 50, 200, np.nan, 500, np.nan],
    'Categoría': ['Electrónica', 'Electrónica', 'Electrónica', 'Electrónica', 'Electrónica', 'Alimentos', 'Alimentos'],
    'Inventario_Disponible': [15, 10, np.nan, 100, 5, 300, 150]
}

df = pd.DataFrame(data)
# Mostrar el dataset original
print("Datos originales con valores faltantes:")
print(df)

# Imputación simple con el promedio
imputer = SimpleImputer(strategy = 'mean')
df[['Precio', 'Ventas_Mensuales', 'Inventario_Disponible']] = imputer.fit_transform(df[['Precio', 'Ventas_Mensuales', 'Inventario_Disponible']])

print('\nDatos después de la imputación simple:')
print(df)

# MAECI: Imputación mediante MICE
df_copy2 = df.copy()  # Crear una copia del DataFrame original.
df_mice = df_copy2.copy()  # Crear otra copia para trabajar con MICE.

from sklearn.experimental import enable_iterative_imputer  # Necesario para activar el iterador
from sklearn.impute import IterativeImputer

# Imputación iterativa con MICE
imputer_mice = IterativeImputer(max_iter=10, random_state=0)
df_mice[['Precio', 'Ventas_Mensuales', 'Inventario_Disponible']] = imputer_mice.fit_transform(df_mice[['Precio', 'Ventas_Mensuales', 'Inventario_Disponible']])

print('\nDatos después de la imputación por algoritmo de MICE:')
print(df_mice)
