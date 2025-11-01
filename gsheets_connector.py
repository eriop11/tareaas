# gsheets_connector.py

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from gspread.exceptions import GSpreadException

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

@st.cache_resource
def connect_to_gsheets():
    """
    Se conecta a Google Sheets usando los secretos y devuelve el objeto cliente.
    Esta función se cachea para no reconectar en cada recarga.
    """
    try:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=SCOPES
        )
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        return None

def get_sheet(sheet_name: str):
    """
    Abre una hoja de cálculo específica por su nombre.
    """
    client = connect_to_gsheets()
    if client:
        try:
            spreadsheet = client.open_by_key(st.secrets["gsheets"]["spreadsheet_key"])
            worksheet = spreadsheet.worksheet(sheet_name)
            return worksheet
        except GSpreadException as e:
            st.error(f"Error al abrir la hoja de cálculo: {e}")
            st.info("Verifica que la 'spreadsheet_key' y el nombre de la pestaña ('sheet_name') sean correctos y que la cuenta de servicio tenga permisos de 'Editor'.")
            return None
    return None
