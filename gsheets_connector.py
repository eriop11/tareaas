# gsheets_connector.py

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Alcances (scopes) necesarios para la API de Google Sheets y Drive.
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Usamos st.cache_resource para inicializar la conexión una sola vez.
@st.cache_resource
def connect_to_gsheets():
    """
    Establece la conexión con la API de Google Sheets y devuelve
    el objeto cliente autorizado.
    """
    try:
        # Cargamos las credenciales desde los secretos de Streamlit.
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=SCOPES
        )
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        return None

# Función de ejemplo para abrir una hoja específica.
# No la cacheadamos aquí, solo obtenemos el recurso.
def get_sheet(sheet_name: str):
    """
    Abre una hoja de cálculo y devuelve un objeto worksheet.
    """
    client = connect_to_gsheets()
    if client:
        try:
            # La URL completa o la clave de la hoja también la guardamos en secretos.
            spreadsheet = client.open_by_key(st.secrets["gsheets"]["spreadsheet_key"])
            worksheet = spreadsheet.worksheet(sheet_name)
            return worksheet
        except gspread.exceptions.SpreadsheetNotFound:
            st.error("Error: No se encontró la hoja de cálculo. Verifica la 'spreadsheet_key' en tus secretos.")
            return None
        except gspread.exceptions.WorksheetNotFound:
            st.error(f"Error: No se encontró la pestaña '{sheet_name}'. Verifica el nombre.")
            return None
    return None
