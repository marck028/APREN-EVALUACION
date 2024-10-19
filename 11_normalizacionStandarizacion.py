import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Cargar el dataset
df = pd.read_csv('C:\\Users\\Marco\\Downloads\\IEA_Global_EV_Data_Sin_Outliers.csv', delimiter=',', encoding='utf-8')

# Columnas a normalizar y estandarizar
columns_to_transform = [
    'Log_price', 'Log_range_km', 'Log_charging_time', 'Log_sales_volume',
    'Log_co2_saved', 'Log_battery_capacity', 'Log_energy_efficiency',
    'Log_weight_kg', 'Log_number_of_seats', 'Log_motor_power', 'Log_distance_traveled'
]

# 1. Normalización Min-Max
scaler_minmax = MinMaxScaler()
df_minmax = df.copy()
df_minmax[columns_to_transform] = scaler_minmax.fit_transform(df[columns_to_transform])

# 2. Estandarización Z-Score (StandardScaler)
scaler_standard = StandardScaler()
df_standard = df.copy()
df_standard[columns_to_transform] = scaler_standard.fit_transform(df[columns_to_transform])

# Guardar los DataFrames normalizados y estandarizados como archivos CSV
minmax_output_path = 'C:\\Users\\Marco\\Downloads\\Datos_Normalizados.csv'
standard_output_path = 'C:\\Users\\Marco\\Downloads\\Datos_Estandarizados.csv'

df_minmax.to_csv(minmax_output_path, index=False)
df_standard.to_csv(standard_output_path, index=False)

print(f"Datos normalizados guardados en '{minmax_output_path}'.")
print(f"Datos estandarizados guardados en '{standard_output_path}'.")
