import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping

# Cargar los datos desde el archivo CSV
data = pd.read_csv(r"C:\Users\Marco\Downloads\datos_modificados_maeci.csv")

# Seleccionar las características y la variable objetivo
feature_columns = [
    'range_km', 'charging_time', 'sales_volume', 'co2_saved',
    'battery_capacity', 'energy_efficiency', 'weight_kg', 
    'number_of_seats', 'motor_power', 'distance_traveled'
]
X = data[feature_columns].values
y = data['price'].values

# Escalar los datos
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))

# Definición del modelo DNN optimizado
model = Sequential()
model.add(Dense(64, input_dim=len(feature_columns), activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(1))

# Compilar el modelo usando el optimizador Adam y MSE como función de pérdida
model.compile(optimizer='adam', loss='mean_squared_error')

# Uso de EarlyStopping para evitar un sobreentrenamiento innecesario
early_stopping = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)

# Entrenar el modelo con EarlyStopping
model.fit(X_scaled, y_scaled, epochs=500, verbose=0, callbacks=[early_stopping])

# Hacer predicciones con los datos existentes
predictions_scaled = model.predict(X_scaled)
predictions = scaler_y.inverse_transform(predictions_scaled)

# Mostrar las predicciones para los datos de entrenamiento
print("Predicciones para datos de entrenamiento:")
print(predictions)

# --- Aquí comienza la parte para ingresar datos por teclado ---

# Obtener las categorías únicas
unique_regions = data['region'].unique()
unique_categories = data['category'].unique()
unique_parameters = data['parameter'].unique()
unique_modes = data['mode'].unique()
unique_powertrains = data['powertrain'].unique()
unique_years = data['year'].unique()

# Solicitar al usuario que seleccione entre las opciones
print("Selecciona una opción de las siguientes categorías:")
region = input(f"Ingresa la región {unique_regions}: ")
category = input(f"Ingresa la categoría {unique_categories}: ")
parameter = input(f"Ingresa el parámetro {unique_parameters}: ")
mode = input(f"Ingresa el modo {unique_modes}: ")
powertrain = input(f"Ingresa el tipo de motorización (powertrain) {unique_powertrains}: ")
year = int(input(f"Ingresa el año {unique_years}: "))

# Definir valores predeterminados
default_values = {
    'range_km': 300,
    'charging_time': 4,
    'sales_volume': 1000,
    'co2_saved': 50,
    'battery_capacity': 75,
    'energy_efficiency': 0.2,
    'weight_kg': 1500,
    'number_of_seats': 5,
    'motor_power': 150,
    'distance_traveled': 15000
}

# Solicitar al usuario que confirme si desea usar los valores predeterminados
print("Valores predeterminados:")
for key, value in default_values.items():
    print(f"{key}: {value}")

use_defaults = input("¿Deseas usar los valores predeterminados? (s/n): ")

if use_defaults.lower() == 'n':
    # Solo solicita ingresar los datos que se deseen cambiar
    range_km = float(input("Ingresa el rango (km) (dejar vacío para usar predeterminado): ") or default_values['range_km'])
    charging_time = float(input("Ingresa el tiempo de carga (horas) (dejar vacío para usar predeterminado): ") or default_values['charging_time'])
    sales_volume = float(input("Ingresa el volumen de ventas (dejar vacío para usar predeterminado): ") or default_values['sales_volume'])
    co2_saved = float(input("Ingresa el CO2 ahorrado (dejar vacío para usar predeterminado): ") or default_values['co2_saved'])
    battery_capacity = float(input("Ingresa la capacidad de la batería (dejar vacío para usar predeterminado): ") or default_values['battery_capacity'])
    energy_efficiency = float(input("Ingresa la eficiencia energética (dejar vacío para usar predeterminado): ") or default_values['energy_efficiency'])
    weight_kg = float(input("Ingresa el peso (kg) (dejar vacío para usar predeterminado): ") or default_values['weight_kg'])
    number_of_seats = int(input("Ingresa el número de asientos (dejar vacío para usar predeterminado): ") or default_values['number_of_seats'])
    motor_power = float(input("Ingresa la potencia del motor (dejar vacío para usar predeterminado): ") or default_values['motor_power'])
    distance_traveled = float(input("Ingresa la distancia recorrida (dejar vacío para usar predeterminado): ") or default_values['distance_traveled'])
else:
    # Usar todos los valores predeterminados
    range_km = default_values['range_km']
    charging_time = default_values['charging_time']
    sales_volume = default_values['sales_volume']
    co2_saved = default_values['co2_saved']
    battery_capacity = default_values['battery_capacity']
    energy_efficiency = default_values['energy_efficiency']
    weight_kg = default_values['weight_kg']
    number_of_seats = default_values['number_of_seats']
    motor_power = default_values['motor_power']
    distance_traveled = default_values['distance_traveled']

# Crear una nueva entrada con los valores del usuario
nuevo_X = np.array([[range_km, charging_time, sales_volume, co2_saved,
                     battery_capacity, energy_efficiency, weight_kg,
                     number_of_seats, motor_power, distance_traveled]])

# Escalar la entrada del usuario
nuevo_X_scaled = scaler_X.transform(nuevo_X)

# Realizar la predicción con la nueva entrada escalada
nueva_prediccion_scaled = model.predict(nuevo_X_scaled)

# Desescalar la predicción para obtener el precio en términos reales
nueva_prediccion = scaler_y.inverse_transform(nueva_prediccion_scaled)

# Mostrar el precio predicho
print(f"El precio estimado para las características ingresadas es: {nueva_prediccion[0][0]:.2f}")
