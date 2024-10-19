import streamlit as st
import requests 
from lxml import html  # pip install lxml

st.title("Extraccion de idiomas con Wikipedia")


# USER AGENT PARA PROTEGERNOS DE BANEOS
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# URL SEMILLA
url = 'https://www.wikipedia.org/'


# REQUERIMIENTO AL SERVIDOR
respuesta = requests.get(url, headers=headers)
respuesta.encoding = 'utf-8'  # Codificar correctamente caracteres extraños

# PARSEO DEL ÁRBOL HTML QUE RECIBO COMO RESPUESTA CON LXML
parser = html.fromstring(respuesta.content)  # Uso .content para poder codificar los caracteres raros

# Mostrar en la interfaz que la conexión ha sido exitosa
st.write("Conexión exitosa con Wikipedia. Extrayendo información...")

# EXTRACCIÓN DE IDIOMA INGLÉS
ingles = parser.get_element_by_id("js-link-box-en")
st.subheader("Extracción del idioma Inglés:")
st.write(ingles.text_content())

 # EXTRACCIÓN DE TODOS LOS IDIOMAS POR CLASE
st.subheader("Extracción de todos los idiomas disponibles por clase:")
idiomas = parser.find_class('central-featured-lang')
for idioma in idiomas:
    print(idioma)
    st.write(idioma.text_content())  # Mostrar cada idioma extraído