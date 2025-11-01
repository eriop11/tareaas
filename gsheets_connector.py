# gsheets_connector.py (Versión de Diagnóstico)

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from gspread.exceptions import GSpreadException

# Alcances (scopes) necesarios para la API
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def connect_and_diagnose():
    """
    Intenta conectarse a Google Sheets y devuelve mensajes de error claros.
    """
    st.header("🔬 Diagnóstico de Conexión a Google Sheets")

    # 1. Verificar si los secretos existen en Streamlit
    if "gcp_service_account" not in st.secrets or "gsheets" not in st.secrets:
        st.error("Error Crítico: No se encontraron las secciones `[gcp_service_account]` o `[gsheets]` en los secretos de Streamlit. Por favor, verifica la configuración de secretos en Streamlit Cloud.")
        return None

    # 2. Intentar cargar las credenciales
    try:
        creds_dict = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        st.success("✅ Paso 1/3: Las credenciales se cargaron correctamente desde los secretos de Streamlit.")
    except Exception as e:
        st.error(f"❌ Error en Paso 1/3: Hubo un problema al cargar las credenciales desde los secretos. Revisa el formato del TOML. Error: {e}")
        return None

    # 3. Intentar autorizar y crear el cliente gspread
    try:
        client = gspread.authorize(creds)
        st.success("✅ Paso 2/3: La autorización con Google fue exitosa (¡Buena señal!).")
    except Exception as e:
        # Este es el punto donde probablemente está fallando
        st.error(f"❌ Error en Paso 2/3: La autorización con Google falló. Esto es un 'RefreshError'.")
        st.error("Causas más probables:")
        st.error("  - La clave privada (private_key) en los secretos es incorrecta o está mal formateada.")
        st.error("  - La cuenta de servicio fue eliminada o su clave fue revocada en Google Cloud.")
        st.error("  - Las APIs de Google Drive y Sheets no están habilitadas en Google Cloud.")
        st.error(f"  - Error detallado: {e}")
        return None

    # 4. Intentar abrir la hoja de cálculo por su clave
    try:
        spreadsheet_key = st.secrets["gsheets"]["spreadsheet_key"]
        spreadsheet = client.open_by_key(spreadsheet_key)
        st.success("✅ Paso 3/3: Se encontró y abrió la hoja de cálculo con la clave proporcionada.")
        return spreadsheet
    except GSpreadException as e:
        st.error(f"❌ Error en Paso 3/3: Se pudo conectar a Google, pero no se pudo abrir la hoja de cálculo.")
        st.error("Causas más probables:")
        st.error("  - La `spreadsheet_key` en los secretos es incorrecta.")
        st.error("  - La cuenta de servicio no tiene permisos de 'Editor' en esa hoja de cálculo específica.")
        st.error(f"  - Error detallado: {e}")
        return None

# ----- No necesitas un archivo inicio_view.py para esta prueba -----
# ----- Simplemente llama a esta función desde app.py -----
