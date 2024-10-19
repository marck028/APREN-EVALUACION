import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import streamlit as st
# Opciones de Chrome
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
opts.add_argument("--disable-search-engine-choice-screen")

# Iniciar el driver de Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

# Navegar a la página
driver.get('https://www.olx.in/cars_c84')

# Esperar hasta que el disclaimer cargue y cerrarlo
try:
    disclaimer_boton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@class="fc-button fc-cta-consent fc-primary-button"]'))
    )
    disclaimer_boton.click()
except Exception as e:
    print("No se encontró el botón de disclaimer:", e)

# Esperar hasta que el botón "Cargar más" esté disponible
try:
    boton_cargar_mas = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
    )
    
    # Clic en "Cargar más" 3 veces
    for i in range(3):
        boton_cargar_mas.click()
        sleep(random.uniform(10.0, 15.0))  # Esperar a que la información cargue
        boton_cargar_mas = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
        )

except Exception as e:
    print("Error al hacer clic en el botón Cargar más:", e)

# Extraer la información de los autos
autos = driver.find_elements(By.XPATH, '//li[@data-aut-id="itemBox2"]')

cont=0
with open('resultados.txt', 'w', encoding='utf-8') as file:
        # Recorro cada uno de los anuncios que he encontrado
        for auto in autos:
            try:
                # Por cada anuncio hallo el precio
                precio = auto.find_element(By.XPATH, './/span[@data-aut-id="itemPrice"]').text
                # Por cada anuncio hallo la descripción
                descripcion = auto.find_element(By.XPATH, './/div[@data-aut-id="itemTitle"]').text
                # Escribir en el archivo
                file.write(f"Precio: {precio}\nDescripción: {descripcion}\n-----------------------------------------\n")
                cont+=1
            except Exception as e:
                print('Anuncio carece de precio o descripción:', e)
                file.write(f"Anuncio carece de precio o descripción: {e}\n\n")

# Cerrar el navegador después del scraping
driver.quit()
print(f'Total registros: {cont}')
print('Fin del Scraping!!!!')



def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
        return data
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return ""


st.title("Scraping de OLX Autos")
st.write("Este es un ejemplo de cómo realizar web scraping de OLX Autos utilizando Selenium en una aplicación de Streamlit.")


file_path = 'resultados.txt'

    # Leer y mostrar el contenido del archivo
content = read_file(file_path)

if content:
    st.write('### RESULTADOS:')
    st.text(content)
    st.write(f'Total registros:{cont}')

