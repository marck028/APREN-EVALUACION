import requests
from bs4 import BeautifulSoup
import streamlit as st

# Título de la aplicación
st.title("Preguntas Recientes de StackOverflow")

# USER AGENT para protegernos de baneos
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# URL semilla
url = 'https://stackoverflow.com/questions'

# Requerimiento al servidor
respuesta = requests.get(url, headers=headers)

# Parseo del árbol con Beautiful Soup
soup = BeautifulSoup(respuesta.text, 'html.parser')  # Especificamos el parser para evitar advertencias
contenedor_de_preguntas = soup.find(id="questions")  # Encontrar el elemento por ID
lista_de_preguntas = contenedor_de_preguntas.find_all('div', class_="s-post-summary")  # Encontrar varios elementos por clase

# Mostrar las preguntas en Streamlit
for pregunta in lista_de_preguntas:  # Iterar sobre cada elemento
    # Método 1: Extracción tradicional
    texto_pregunta = pregunta.find('h3').text  # Extraer el texto de la pregunta
    descripcion_pregunta = pregunta.find(class_='s-post-summary--content-excerpt').text  # Extraer la descripción
    descripcion_pregunta = descripcion_pregunta.replace('\n', '').replace('\r', '').strip()  # Limpieza del texto
    
    # Mostrar en la interfaz
    st.subheader(texto_pregunta)
    st.write(descripcion_pregunta)
    st.write('---')  # Línea divisoria para separar preguntas

# Mensaje final
st.write("Fin de las preguntas.")