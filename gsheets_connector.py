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

# --- CONEXIÓN BÁSICA ---

@st.cache_resource(ttl=3600) # Cache para 1 hora
def connect_to_gsheets():
    """Se conecta a Google Sheets usando los secretos y devuelve el objeto cliente."""
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
    """Abre una hoja de cálculo específica por su nombre."""
    client = connect_to_gsheets()
    if client:
        try:
            spreadsheet = client.open_by_key(st.secrets["gsheets"]["spreadsheet_key"])
            worksheet = spreadsheet.worksheet(sheet_name)
            return worksheet
        except GSpreadException as e:
            st.error(f"Error al abrir la hoja '{sheet_name}': {e}")
            return None
    return None

# --- FUNCIONES DE CARGA DE DATOS (LECTURA) ---

@st.cache_data(ttl=300) # Cache para 5 minutos
def cargar_usuarios():
    """Carga los usuarios desde la pestaña 'Usuarios'."""
    sheet = get_sheet("Usuarios")
    if sheet:
        return sheet.get_all_records()
    return []

@st.cache_data(ttl=60) # Cache para 1 minuto
def cargar_tareas():
    sheet = get_sheet("Tareas")
    if sheet:
        return sheet.get_all_records()
    return []

@st.cache_data(ttl=300)
def cargar_categorias():
    sheet = get_sheet("Categorias")
    if sheet:
        # Asume que las categorías están en la primera columna
        values = sheet.col_values(1)
        return values[1:] if len(values) > 1 else [] # Omitir encabezado
    return []

@st.cache_data(ttl=60)
def cargar_comentarios():
    sheet = get_sheet("Comentarios")
    if sheet:
        return sheet.get_all_records()
    return []

# --- FUNCIONES DE MODIFICACIÓN DE DATOS (ESCRITURA) ---

def guardar_nueva_tarea(datos_tarea: dict):
    """Añade una nueva fila a la hoja 'Tareas'."""
    sheet = get_sheet("Tareas")
    if sheet:
        try:
            id_tarea = str(uuid.uuid4())
            fecha_str = datos_tarea["fecha_limite"].strftime("%Y-%m-%d")
            
            # Asegúrate de que el orden coincida con las columnas de tu Google Sheet
            nueva_fila = [
                id_tarea, datos_tarea["titulo"], datos_tarea["descripcion"],
                datos_tarea["usuario"], datos_tarea["categoria"], fecha_str,
                datos_tarea["estado"], datos_tarea["avance"]
            ]
            sheet.append_row(nueva_fila)
            st.cache_data.clear() # Limpiar cache para recargar datos
            return True
        except Exception as e:
            st.error(f"No se pudo guardar la tarea: {e}")
    return False

def guardar_nueva_categoria(nombre_cat: str):
    sheet = get_sheet("Categorias")
    if sheet:
        try:
            sheet.append_row([nombre_cat])
            st.cache_data.clear()
            return True
        except Exception as e:
            st.error(f"No se pudo guardar la categoría: {e}")
    return False

def eliminar_tarea(id_tarea: str):
    sheet = get_sheet("Tareas")
    if sheet:
        try:
            cell = sheet.find(id_tarea)
            if cell:
                sheet.delete_rows(cell.row)
                st.cache_data.clear()
                return True
        except Exception as e:
            st.error(f"Error al eliminar la tarea: {e}")
    return False

def actualizar_tarea(id_tarea: str, datos: dict):
    sheet = get_sheet("Tareas")
    if sheet:
        try:
            cell = sheet.find(id_tarea)
            if cell:
                row_num = cell.row
                fecha_str = datos["fecha_limite"].strftime("%Y-%m-%d")
                # El rango a actualizar NO incluye la columna A (ID)
                sheet.update(f'B{row_num}:H{row_num}', [[
                    datos["titulo"], datos["descripcion"], datos["usuario"],
                    datos["categoria"], fecha_str, datos["estado"], datos["avance"]
                ]])
                st.cache_data.clear()
                return True
        except Exception as e:
            st.error(f"Error al actualizar la tarea: {e}")
    return False

def actualizar_estado_tarea(id_tarea: str, estado: str, avance: int):
    sheet = get_sheet("Tareas")
    if sheet:
        try:
            cell = sheet.find(id_tarea)
            if cell:
                row_num = cell.row
                # Asume que 'Estado' es la columna G (7) y 'Avance (%)' es la H (8)
                sheet.update_cell(row_num, 7, estado)
                sheet.update_cell(row_num, 8, avance)
                st.cache_data.clear()
                return True
        except Exception as e:
            st.error(f"Error al actualizar el estado: {e}")
    return False
    
def guardar_comentario(id_tarea: str, usuario: str, comentario: str):
    sheet = get_sheet("Comentarios")
    if sheet:
        try:
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # ID Comentario, ID Tarea, Usuario, Comentario, Fecha
            nueva_fila = [str(uuid.uuid4()), id_tarea, usuario, comentario, fecha_actual]
            sheet.append_row(nueva_fila)
            st.cache_data.clear()
            return True
        except Exception as e:
            st.error(f"No se pudo guardar el comentario: {e}")
    return False

# --- FUNCIÓN AUXILIAR ---

def get_category_colors(categorias: list):
    """Genera un mapa de colores para las categorías."""
    colors = ["#FFC300", "#FF5733", "#C70039", "#900C3F", "#581845", "#DAF7A6", "#33FF57"]
    color_map = {}
    for i, cat in enumerate(categorias):
        color_map[cat] = colors[i % len(colors)]
    return color_map
