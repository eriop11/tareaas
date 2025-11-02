# inicio_view.py (Versión Gestor de Tareas)

import streamlit as st
from gsheets_connector import get_sheet
from usuarios_view import cargar_usuarios # Importamos la función para cargar usuarios
import pandas as pd # Usaremos pandas para mostrar las tareas en una tabla bonita
from datetime import datetime

# --- FUNCIONES DE DATOS PARA TAREAS Y CATEGORÍAS ---

@st.cache_data(ttl=300)
def cargar_categorias():
    worksheet = get_sheet("Categorias")
    if worksheet:
        return [row.get("Nombre Categoria") for row in worksheet.get_all_records()]
    return []

def guardar_nueva_categoria(nombre_categoria):
    worksheet = get_sheet("Categorias")
    if worksheet:
        worksheet.append_row([nombre_categoria])
        st.cache_data.clear() # Limpiamos toda la caché para asegurar que se recargue
        return True
    return False

@st.cache_data(ttl=60) # Las tareas se actualizan más seguido
def cargar_tareas():
    worksheet = get_sheet("Tareas")
    if worksheet:
        return worksheet.get_all_records()
    return []

def guardar_nueva_tarea(datos_tarea):
    worksheet = get_sheet("Tareas")
    if worksheet:
        # El orden debe coincidir con las columnas en Google Sheets
        fila = [
            datos_tarea['tarea'],
            datos_tarea['usuario'],
            datos_tarea['categoria'],
            datos_tarea['fecha_limite'].strftime("%Y-%m-%d"), # Formatear fecha a texto
            datos_tarea['estado'],
            datos_tarea['avance']
        ]
        worksheet.append_row(fila)
        st.cache_data.clear()
        return True
    return False

def actualizar_tarea(tarea_original, nuevos_datos):
    worksheet = get_sheet("Tareas")
    if worksheet:
        registros = worksheet.get_all_records()
        for i, registro in enumerate(registros, start=2):
            # Identificamos la tarea por su descripción y usuario (más seguro que solo por descripción)
            if registro.get("Tarea") == tarea_original['Tarea'] and registro.get("Usuario Asignado") == tarea_original['Usuario Asignado']:
                worksheet.update_cell(i, 5, nuevos_datos['estado']) # Columna 5: Estado
                worksheet.update_cell(i, 6, nuevos_datos['avance']) # Columna 6: Avance (%)
                st.cache_data.clear()
                return True
    return False

# --- VISTA PRINCIPAL DE LA PÁGINA DE INICIO ---

def mostrar_pagina_inicio():
    st.header("📋 Gestor de Tareas")
    
    # Cargamos todos los datos necesarios al principio
    usuarios = cargar_usuarios()
    nombres_usuarios = [u.get("Nombre") for u in usuarios]
    categorias = cargar_categorias()
    tareas = cargar_tareas()

    # --- SECCIÓN PARA AÑADIR NUEVA TAREA Y CATEGORÍAS ---
    with st.expander("➕ Añadir Nueva Tarea o Categoría"):
        tab1, tab2 = st.tabs(["Crear Tarea", "Añadir Categoría"])

        with tab1:
            with st.form("nueva_tarea_form", clear_on_submit=True):
                st.subheader("Nueva Tarea")
                tarea_desc = st.text_area("Descripción de la tarea")
                
                col1, col2 = st.columns(2)
                with col1:
                    usuario_asignado = st.selectbox("Asignar a:", options=nombres_usuarios)
                    categoria_tarea = st.selectbox("Categoría:", options=categorias)
                with col2:
                    fecha_limite = st.date_input("Fecha límite")
                    estado_inicial = st.selectbox("Estado:", ["Pendiente", "En Proceso", "Terminada"])
                
                avance = st.slider("Porcentaje de Avance (%)", 0, 100, 0)
                
                submitted_tarea = st.form_submit_button("Guardar Tarea")
                if submitted_tarea:
                    datos_tarea = {
                        "tarea": tarea_desc, "usuario": usuario_asignado, "categoria": categoria_tarea,
                        "fecha_limite": fecha_limite, "estado": estado_inicial, "avance": avance
                    }
                    if guardar_nueva_tarea(datos_tarea):
                        st.success("¡Tarea guardada con éxito!")
                        st.rerun()

        with tab2:
            with st.form("nueva_categoria_form", clear_on_submit=True):
                st.subheader("Nueva Categoría")
                nombre_cat = st.text_input("Nombre de la nueva categoría")
                submitted_cat = st.form_submit_button("Guardar Categoría")
                if submitted_cat and nombre_cat:
                    if guardar_nueva_categoria(nombre_cat):
                        st.success("¡Categoría guardada!")
                        st.rerun()

    st.divider()

    # --- VISUALIZACIÓN DE TAREAS ---
    st.subheader("Listado de Tareas Pendientes y en Proceso")
    
    if not tareas:
        st.info("No hay tareas registradas. ¡Añade la primera!")
    else:
        # Usamos Pandas para una mejor visualización y filtrado
        df_tareas = pd.DataFrame(tareas)
        
        # Filtramos para no mostrar las terminadas por defecto
        df_activas = df_tareas[df_tareas['Estado'] != 'Terminada']

        if df_activas.empty:
            st.success("🎉 ¡Felicidades! No hay tareas pendientes.")
        else:
            st.dataframe(
                df_activas[['Tarea', 'Usuario Asignado', 'Categoría', 'Fecha Límite', 'Estado', 'Avance (%)']],
                use_container_width=True
            )

    st.divider()

    # --- SECCIÓN PARA ACTUALIZAR TAREAS ---
    st.subheader("⚙️ Actualizar Estado de una Tarea")
    
    tareas_no_terminadas = [t for t in tareas if t.get('Estado') != 'Terminada']
    if not tareas_no_terminadas:
        st.write("No hay tareas activas para actualizar.")
    else:
        # Creamos una lista legible para el selectbox
        opciones_tareas = [f"{t.get('Tarea')} (Asignada a: {t.get('Usuario Asignado')})" for t in tareas_no_terminadas]
        tarea_seleccionada_str = st.selectbox("Selecciona una tarea para actualizar", options=opciones_tareas)
        
        # Encontramos los datos completos de la tarea seleccionada
        indice_seleccionado = opciones_tareas.index(tarea_seleccionada_str)
        tarea_a_actualizar = tareas_no_terminadas[indice_seleccionado]

        with st.form("actualizar_tarea_form"):
            st.write(f"**Tarea:** {tarea_a_actualizar.get('Tarea')}")
            
            # Convertimos el avance a número para el slider
            try:
                avance_actual = int(tarea_a_actualizar.get("Avance (%)"))
            except (ValueError, TypeError):
                avance_actual = 0
                
            nuevo_estado = st.selectbox(
                "Nuevo Estado",
                ["Pendiente", "En Proceso", "Terminada"],
                index=["Pendiente", "En Proceso", "Terminada"].index(tarea_a_actualizar.get("Estado"))
            )
            nuevo_avance = st.slider("Nuevo Porcentaje de Avance (%)", 0, 100, avance_actual)
            
            submitted_update = st.form_submit_button("Actualizar Tarea")
            if submitted_update:
                nuevos_datos = {"estado": nuevo_estado, "avance": nuevo_avance}
                if actualizar_tarea(tarea_a_actualizar, nuevos_datos):
                    st.success("¡Tarea actualizada!")
                    st.rerun()
