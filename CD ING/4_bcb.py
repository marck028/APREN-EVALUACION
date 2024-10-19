from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import streamlit  as st

# Configuración de opciones para el navegador
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
opts.add_argument("--disable-search-engine-choice-screen")

# Inicializar el driver de Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

# Navegar a la página
driver.get('https://www.bcb.gob.bo/librerias/indicadores/otras/ultimo.php')

# Esperar a que la tabla esté disponible
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'tablaborde'))
    )
    print("La tabla ha cargado correctamente.")
except Exception as e:
    print("Error al cargar la tabla:", e)
    driver.quit()
    
# Extraer la información de la tabla
try:
    tabla = driver.find_element(By.CLASS_NAME, 'tablaborde')
    filas = tabla.find_elements(By.TAG_NAME, 'tr')
    
    with open('cotizaciones_monedas.txt', 'w', encoding='utf-8') as file:
        for fila in filas:
            columnas = fila.find_elements(By.TAG_NAME, 'td')
            if columnas:
                # Extraer texto de cada columna
                datos = [columna.text.strip() for columna in columnas]
                file.write("|".join(datos) + "\n")
    
    print("Datos extraídos correctamente.")
except Exception as e:
    print("Error al extraer la información:", e)

# Cerrar el navegador
driver.quit()

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
        return data
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return ""

st.title('Scraping de Cotizaciones del Banco Central de Bolivia')
# Seleccionar el archivo de cotizaciones
file_path = 'cotizaciones_monedas.txt'

# Leer y mostrar el contenido del archivo
content = read_file(file_path)

if content:
    st.write('### Datos de Cotizaciones:')
    st.text(content)
