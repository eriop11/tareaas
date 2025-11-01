# inicio_view.py

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import pandas as pd
from datetime import datetime

# --- FUNCIONES PARA INTERACTUAR CON GOOGLE SHEETS ---

@st.cache_resource(ttl=600) # Cache para no reconectar en cada rerun
def conectar_a_gsheets():
    """Conecta con Google Sheets usando las credenciales de Streamlit Secrets."""
    try:
        creds = st.secrets["gcp_service_account"]
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        s_creds = Credentials.from_service_account_info(creds, scopes=scopes)
        client = gspread.authorize(s_creds)
        return client
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        return None

@st.cache_data(ttl=60) # Cache para no recargar los datos tan seguido
def cargar_nota(cliente_gsheets):
    """Carga la última nota guardada desde Google Sheets."""
    if cliente_gsheets is None:
        return "" # Devuelve vacío si no hay conexión
    try:
        # Reemplaza "NotasAppStreamlit" con el nombre exacto de tu hoja de cálculo
        sheet = cliente_gsheets.open("NotasAppStreamlit").sheet1
        df = pd.DataFrame(sheet.get_all_records())
        if not df.empty:
            return df.iloc[-1]['nota'] # Devuelve el texto de la última fila
        return "" # Devuelve vacío si la hoja no tiene notas
    except gspread.exceptions.SpreadsheetNotFound:
        st.warning("Hoja de cálculo 'NotasAppStreamlit' no encontrada. Creando una nota inicial.")
        return ""
    except Exception as e:
        st.error(f"Error al cargar la nota: {e}")
        return ""

def guardar_nota(cliente_gsheets, nueva_nota):
    """Guarda una nueva nota en Google Sheets."""
    if cliente_gsheets is None:
        st.error("No se pudo conectar a Google Sheets para guardar la nota.")
        return False
    try:
        sheet = cliente_gsheets.open("NotasAppStreamlit").sheet1
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        nueva_fila = [timestamp, nueva_nota]
        sheet.append_row(nueva_fila)
        # Limpiamos el caché de la función de carga para que la próxima vez lea los datos actualizados
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error al guardar la nota: {e}")
        return False

# --- FUNCIÓN PRINCIPAL DE LA VISTA ---

def mostrar_pagina_inicio():
    """Renderiza la página de "Inicio" con el bloc de notas conectado a Google Sheets."""
    st.header("🏠 Página de Inicio")
    st.write("Bloc de notas persistente. La información se guarda en Google Sheets.")
    st.markdown("---")
    
    # Conectamos al servicio
    cliente = conectar_a_gsheets()
    
    # Cargamos la última nota guardada para mostrarla
    ultima_nota = cargar_nota(cliente)
    
    # Usamos el estado de sesión para manejar el texto actual en el widget
    if 'nota_actual' not in st.session_state:
        st.session_state.nota_actual = ultima_nota
    
    # Creamos el área de texto
    nota_ingresada = st.text_area(
        label="Escribe algo para guardar:",
        value=st.session_state.nota_actual,
        height=250,
        key="area_de_nota"
    )
    
    # Botón para guardar
    if st.button("Guardar Nota"):
        if nota_ingresada:
            if guardar_nota(cliente, nota_ingresada):
                st.success("¡Nota guardada con éxito!")
                st.session_state.nota_actual = nota_ingresada # Actualizamos el estado
            else:
                st.error("No se pudo guardar la nota.")
        else:
            st.warning("No hay nada que guardar.")
