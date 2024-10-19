import pandas as pd
import numpy as np

# Función para aplicar la transformación logarítmica
def transformar_logaritmicamente(df, columns):
    for column in columns:
        # Evitar el log(0) reemplazando valores 0 por NaN
        df['Log_' + column] = np.log(df[column].replace(0, np.nan))
    return df

# Función para eliminar outliers basados en el Z-Score
def eliminar_outliers_z_score(df, columns, threshold=3):
    for column in columns:
        mean = df['Log_' + column].mean()
        std = df['Log_' + column].std()
        z_score = (df['Log_' + column] - mean) / std
        df = df[(z_score >= -threshold) & (z_score <= threshold)]
    return df

def main():
    try:
        # Cargar los datos
        data = pd.read_csv("C:\\Users\\Marco\\Downloads\\datos_modificados_maeci.csv", delimiter=',')
    except FileNotFoundError:
        print("Error: No se encontró el archivo. Verifica la ruta y el nombre del archivo.")
        return
    except pd.errors.EmptyDataError:
        print("Error: El archivo está vacío.")
        return
    except Exception as e:
        print(f"Error inesperado: {e}")
        return

    # Obtener los nombres de las columnas desde la columna 9 (índice 8)
    columns_to_transform = data.columns[8:]

    # Transformar logarítmicamente las columnas seleccionadas
    data = transformar_logaritmicamente(data, columns_to_transform)

    # Eliminar outliers en las columnas transformadas
    data_sin_outliers = eliminar_outliers_z_score(data, columns_to_transform)

    # Seleccionar solo las columnas deseadas
    columnas_deseadas = [
        'region', 'category', 'parameter', 'mode', 'powertrain',
        'year', 'unit', 'value', 'Log_price', 'Log_range_km',
        'Log_charging_time', 'Log_sales_volume', 'Log_co2_saved',
        'Log_battery_capacity', 'Log_energy_efficiency', 'Log_weight_kg',
        'Log_number_of_seats', 'Log_motor_power', 'Log_distance_traveled'
    ]

    # Filtrar el DataFrame para que contenga solo las columnas deseadas
    data_final = data_sin_outliers[columnas_deseadas]

    # Guardar el resultado en un archivo CSV
    output_path_csv = 'C:\\Users\\Marco\\Downloads\\IEA_Global_EV_Data_Sin_Outliers.csv'
    data_final.to_csv(output_path_csv, index=False)  # index=False para no incluir el índice en el CSV

    print(f"Datos procesados y guardados en '{output_path_csv}'.")


if __name__ == "__main__":
    main()
 