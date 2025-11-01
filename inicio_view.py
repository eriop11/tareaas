# inicio_view.py

import streamlit as st
from gsheets_connector import get_sheet  # <-- Importamos desde nuestro conector

# Usamos st.cache_data para cachear los datos que devuelve la función.
# ttl (Time To Live) define cada cuántos segundos se debe refrescar la caché.
@st.cache_data(ttl=300)  # Refresca los datos cada 5 minutos (300 segundos)
def cargar_ultima_nota():
    """
    Carga la última nota de la hoja de cálculo.
    Esta función no recibe parámetros "inhasheables".
    """
    worksheet = get_sheet("Hoja1")  # <-- Cambia "Hoja1" por el nombre de tu pestaña
    
    if worksheet:
        # Obtenemos todos los registros (asume que la primera fila es encabezado)
        all_data = worksheet.get_all_records()
        if all_data:
            # Devolvemos el último diccionario de la lista
            return all_data[-1]
    return None

def guardar_nueva_nota(datos_nota: list):
    """
    Guarda una nueva fila de datos en la hoja de cálculo.
    """
    worksheet = get_sheet("Hoja1") # <-- Cambia "Hoja1" por el nombre de tu pestaña
    if worksheet:
        worksheet.append_row(datos_nota)
        # Limpiamos la caché de la función que lee los datos para que se actualice al momento.
        st.cache_data.clear()
        return True
    return False

# Esta es la función principal que se llama desde app.py
def mostrar_pagina_inicio():
    st.header("🏠 Vista de Inicio")
    st.write("Aquí puedes ver la última nota registrada y añadir una nueva.")

    st.subheader("Última nota registrada")
    
    # Llamamos a la función que carga los datos (sin pasarle el cliente)
    ultima_nota = cargar_ultima_nota()

    if ultima_nota:
        st.json(ultima_nota)
    else:
        st.info("No se encontraron notas o hubo un error al cargar los datos.")

    st.divider()

    st.subheader("Añadir nueva nota")
    with st.form("nueva_nota_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            # Ajusta estos campos a las columnas de tu Google Sheet
            campo1 = st.text_input("Nombre del dato")
        with col2:
            campo2 = st.number_input("Valor numérico", step=1)
        
        submitted = st.form_submit_button("Guardar Nota")
        if submitted:
            # La lista debe tener el mismo orden que las columnas en tu hoja
            nueva_fila = [campo1, campo2]
            if guardar_nueva_nota(nueva_fila):
                st.success("¡Nota guardada con éxito!")
            else:
                st.error("No se pudo guardar la nota.")
