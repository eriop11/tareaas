# inicio_view.py (Versión Corregida para Tema Oscuro)

import streamlit as st
from gsheets_connector import get_sheet

@st.cache_data(ttl=300)
def cargar_ultima_nota():
    """
    Carga la última nota de la hoja de cálculo.
    """
    worksheet = get_sheet("dataefe")
    if worksheet:
        all_data = worksheet.get_all_records()
        if all_data:
            return all_data[-1]
    return None

def guardar_nueva_nota(datos_nota: list):
    """
    Guarda una nueva fila de datos en la hoja de cálculo.
    """
    worksheet = get_sheet("dataefe")
    if worksheet:
        worksheet.append_row(datos_nota)
        st.cache_data.clear()
        return True
    return False

def mostrar_pagina_inicio():
    st.header("🏠 Vista de Inicio")
    st.write("Aquí puedes ver la última nota registrada y añadir una nueva.")

    st.subheader("Última nota registrada")
    
    ultima_nota = cargar_ultima_nota()

    if ultima_nota:
        # CAMBIO 1: Reemplazamos st.json por st.code
        # st.code tiene un tema oscuro por defecto y se ve mucho mejor.
        st.code(str(ultima_nota), language='json')
    else:
        # CAMBIO 2: Reemplazamos st.info por st.write con un ícono
        # st.write hereda el color de texto blanco global.
        st.write("ℹ️ No se encontraron notas o hubo un error al cargar los datos.")

    st.divider()

    st.subheader("Añadir nueva nota")
    with st.form("nueva_nota_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            campo1 = st.text_input("Nombre del dato")
        with col2:
            campo2 = st.number_input("Valor numérico", step=1)
        
        submitted = st.form_submit_button("Guardar Nota")
        if submitted:
            nueva_fila = [campo1, campo2]
            if guardar_nueva_nota(nueva_fila):
                st.success("¡Nota guardada con éxito!")
            else:
                st.error("No se pudo guardar la nota.")
