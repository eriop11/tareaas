# gsheets_connector.py

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from gspread.exceptions import GSpreadException
import uuid
from datetime import datetime

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

@st.cache_resource(ttl=3600)
def connect_to_gsheets():
    try:
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        return None

def get_sheet(sheet_name: str):
    client = connect_to_gsheets()
    if client:
        try:
            spreadsheet = client.open_by_key(st.secrets["gsheets"]["spreadsheet_key"])
            return spreadsheet.worksheet(sheet_name)
        except GSpreadException as e:
            st.error(f"Error al abrir la hoja '{sheet_name}': {e}")
            return None
    return None

# --- LECTURA DE DATOS ---
@st.cache_data(ttl=300)
def cargar_usuarios():
    sheet = get_sheet("usuarios")
    return sheet.get_all_records() if sheet else []

@st.cache_data(ttl=60)
def cargar_tareas():
    sheet = get_sheet("tareas")
    return sheet.get_all_records() if sheet else []

@st.cache_data(ttl=300)
def cargar_categorias():
    sheet = get_sheet("categorias")
    if sheet:
        values = sheet.col_values(1)
        return values[1:] if len(values) > 1 else []
    return []

@st.cache_data(ttl=60)
def cargar_comentarios():
    sheet = get_sheet("comentarios")
    return sheet.get_all_records() if sheet else []

# --- ESCRITURA DE DATOS ---
def guardar_nueva_tarea(datos_tarea: dict):
    sheet = get_sheet("tareas")
    if sheet:
        try:
            id_tarea = str(uuid.uuid4())
            fecha_str = datos_tarea["fecha_limite"].strftime("%Y-%m-%d")
            
            # CORRECCIÓN: El orden debe coincidir EXACTAMENTE con las columnas en la hoja
            # ID, Título, Descripción, Usuario Asignado, Categoría, Fecha Límite, Estado, Avance (%)
            nueva_fila = [
                id_tarea,
                datos_tarea["titulo"],
                datos_tarea["descripcion"],
                datos_tarea["usuario_asignado"],
                datos_tarea["categoria"],
                fecha_str,
                datos_tarea["estado"],
                datos_tarea["avance"]
            ]
            sheet.append_row(nueva_fila)
            st.cache_data.clear()
            return True
        except Exception as e:
            st.error(f"No se pudo guardar la tarea: {e}")
    return False

def actualizar_tarea(id_tarea: str, datos: dict):
    sheet = get_sheet("tareas")
    if sheet:
        try:
            cell = sheet.find(id_tarea)
            if cell:
                row_num = cell.row
                fecha_str = datos["fecha_limite"].strftime("%Y-%m-%d")
                
                # CORRECCIÓN: El rango ahora va de B a H (7 columnas)
                # Título, Descripción, Usuario Asignado, Categoría, Fecha Límite, Estado, Avance (%)
                sheet.update(f'B{row_num}:H{row_num}', [[
                    datos["titulo"],
                    datos["descripcion"],
                    datos["usuario_asignado"],
                    datos["categoria"],
                    fecha_str,
                    datos["estado"],
                    datos["avance"]
                ]])
                st.cache_data.clear()
                return True
        except Exception as e:
            st.error(f"Error al actualizar la tarea: {e}")
    return False

def actualizar_estado_tarea(id_tarea: str, estado: str, avance: int):
    sheet = get_sheet("tareas")
    if sheet:
        try:
            cell = sheet.find(id_tarea)
            if cell:
                row_num = cell.row
                # CORRECCIÓN: 'Estado' es la columna G (7) y 'Avance (%)' es la H (8)
                sheet.update_cell(row_num, 7, estado)
                sheet.update_cell(row_num, 8, avance)
                st.cache_data.clear()
                return True
        except Exception as e:
            st.error(f"Error al actualizar el estado: {e}")
    return False

# (Las demás funciones de guardado y auxiliares no necesitan cambios)
# ... [copia el resto de funciones como guardar_nueva_categoria, eliminar_tarea, etc.] ...
