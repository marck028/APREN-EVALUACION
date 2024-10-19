import pandas as pd

# Cargar los datos desde el archivo CSV
df = pd.read_csv("C:\\Users\\Marco\\Downloads\\datos_modificados_maeci.csv")

# Definir las columnas de las que deseas obtener las categorías únicas
categorical_columns = ['region', 'category', 'parameter', 'mode', 'powertrain', 'year']

# Obtener y mostrar las categorías únicas para cada columna
for column in categorical_columns:
    unique_categories = df[column].unique()
    print(f"Categorías únicas en '{column}':")
    print(unique_categories)
    print()  # Línea en blanco para mejor legibilidad
