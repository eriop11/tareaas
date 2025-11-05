# inicio_view.py (Versión Mejorada)

import streamlit as st
from gsheets_connector import get_sheet
from usuarios_view import cargar_usuarios
import pandas as pd
from datetime import datetime
import random # Para generar IDs y colores

# --- FUNCIONES DE DATOS: CATEGORÍAS, TAREAS Y COMENTARIOS ---

@st.cache_data(ttl=300)
def cargar_categorias():
    """Carga las categorías desde Google Sheets."""
    worksheet = get_sheet("Categorias")
    if worksheet:
        return [row.get("Nombre Categoria") for row in worksheet.get_all_records() if row.get("Nombre Categoria")]
    return []

def guardar_nueva_categoria(nombre_categoria):
    """Guarda una nueva categoría y limpia la caché."""
    worksheet = get_sheet("Categorias")
    if worksheet:
        worksheet.append_row([nombre_categoria])
        st.cache_data.clear()
        return True
    return False

@st.cache_data(ttl=60)
def cargar_tareas():
    """Carga todas las tareas desde Google Sheets."""
    worksheet = get_sheet("Tareas")
    if worksheet:
        return worksheet.get_all_records()
    return []

@st.cache_data(ttl=60)
def cargar_comentarios():
    """Carga todos los comentarios desde Google Sheets."""
    worksheet = get_sheet("Comentarios")
    if worksheet:
        return worksheet.get_all_records()
    return []

def guardar_nueva_tarea(datos_tarea):
    """Guarda una nueva tarea en Google Sheets."""
    worksheet = get_sheet("Tareas")
    if worksheet:
        # Generamos un ID único para la tarea para poder referenciarla
        id_tarea = f"T-{random.randint(1000, 9999)}-{int(datetime.now().timestamp())}"
        fila = [
            id_tarea,
            datos_tarea['titulo'],
            datos_tarea['descripcion'],
            datos_tarea['usuario'],
            datos_tarea['categoria'],
            datos_tarea['fecha_limite'].strftime("%Y-%m-%d"),
            datos_tarea['estado'],
            datos_tarea['avance']
        ]
        worksheet.append_row(fila)
        st.cache_data.clear()
        return True
    return False

def guardar_comentario(id_tarea, usuario, comentario):
    """Guarda un nuevo comentario asociado a una tarea."""
    worksheet = get_sheet("Comentarios")
    if worksheet:
        fila = [id_tarea, usuario, comentario, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        worksheet.append_row(fila)
        st.cache_data.clear() # Limpiamos para que se recarguen los comentarios
        return True
    return False

def actualizar_tarea(id_tarea, nuevos_datos):
    """Actualiza los datos de una tarea existente."""
    worksheet = get_sheet("Tareas")
    if worksheet:
        cell = worksheet.find(id_tarea) # Buscamos la fila por ID
        if cell:
            fila = cell.row
            # Actualizamos cada celda según corresponda (el orden de las columnas importa)
            worksheet.update_cell(fila, 2, nuevos_datos['titulo'])
            worksheet.update_cell(fila, 3, nuevos_datos['descripcion'])
            worksheet.update_cell(fila, 4, nuevos_datos['usuario'])
            worksheet.update_cell(fila, 5, nuevos_datos['categoria'])
            worksheet.update_cell(fila, 6, nuevos_datos['fecha_limite'].strftime("%Y-%m-%d"))
            worksheet.update_cell(fila, 7, nuevos_datos['estado'])
            worksheet.update_cell(fila, 8, nuevos_datos['avance'])
            st.cache_data.clear()
            return True
    return False

def actualizar_estado_tarea(id_tarea, nuevo_estado, nuevo_avance):
    """Actualiza solo el estado y el avance de una tarea."""
    worksheet = get_sheet("Tareas")
    if worksheet:
        cell = worksheet.find(id_tarea)
        if cell:
            worksheet.update_cell(cell.row, 7, nuevo_estado) # Columna 7: Estado
            worksheet.update_cell(cell.row, 8, nuevo_avance) # Columna 8: Avance (%)
            st.cache_data.clear()
            return True
    return False

def eliminar_tarea(id_tarea):
    """Elimina una tarea de la hoja de cálculo."""
    worksheet = get_sheet("Tareas")
    if worksheet:
        cell = worksheet.find(id_tarea)
        if cell:
            worksheet.delete_rows(cell.row)
            st.cache_data.clear()
            return True
    return False


# --- FUNCIONES AUXILIARES DE LA VISTA ---

@st.cache_resource
def get_category_colors(categorias):
    """Genera un mapa de colores para cada categoría."""
    colors = ["#FFADAD", "#FFD6A5", "#FDFFB6", "#CAFFBF", "#9BF6FF", "#A0C4FF", "#BDB2FF", "#FFC6FF"]
    color_map = {}
    for i, cat in enumerate(categorias):
        color_map[cat] = colors[i % len(colors)] # Asigna colores de forma cíclica
    return color_map


# --- VISTA PRINCIPAL ---

def mostrar_pagina_inicio():
    st.header("📋 Gestor de Tareas Avanzado")

    # --- Carga de datos ---
    usuarios = cargar_usuarios()
    nombres_usuarios = [u.get("Nombre") for u in usuarios]
    categorias = cargar_categorias()
    tareas = cargar_tareas()
    comentarios = cargar_comentarios()
    category_colors = get_category_colors(categorias)

    # --- SECCIÓN PARA AÑADIR NUEVA TAREA Y CATEGORÍA ---
    with st.expander("➕ Añadir Nueva Tarea o Categoría"):
        tab1, tab2 = st.tabs(["Crear Tarea", "Añadir Categoría"])

        with tab1:
            with st.form("nueva_tarea_form", clear_on_submit=True):
                st.subheader("Nueva Tarea")
                tarea_titulo = st.text_input("Título de la tarea")
                tarea_desc = st.text_area("Descripción detallada")

                col1, col2 = st.columns(2)
                with col1:
                    usuario_asignado = st.selectbox("Asignar a:", options=nombres_usuarios, key="user_assign")
                    categoria_tarea = st.selectbox("Categoría:", options=categorias, key="cat_assign")
                with col2:
                    fecha_limite = st.date_input("Fecha límite")
                    estado_inicial = st.selectbox("Estado:", ["Pendiente", "En Proceso", "Terminada"])

                avance = st.slider("Porcentaje de Avance (%)", 0, 100, 0)

                if st.form_submit_button("Guardar Tarea"):
                    if tarea_titulo: # Al menos el título es obligatorio
                        datos_tarea = {
                            "titulo": tarea_titulo, "descripcion": tarea_desc, "usuario": usuario_asignado,
                            "categoria": categoria_tarea, "fecha_limite": fecha_limite,
                            "estado": estado_inicial, "avance": avance
                        }
                        if guardar_nueva_tarea(datos_tarea):
                            st.success("¡Tarea guardada con éxito!")
                            st.rerun()
                    else:
                        st.warning("El título de la tarea no puede estar vacío.")

        with tab2:
            with st.form("nueva_categoria_form", clear_on_submit=True):
                st.subheader("Nueva Categoría")
                nombre_cat = st.text_input("Nombre de la nueva categoría")
                if st.form_submit_button("Guardar Categoría") and nombre_cat:
                    if guardar_nueva_categoria(nombre_cat):
                        st.success("¡Categoría guardada!")
                        st.rerun()

    st.divider()

    # --- VISUALIZACIÓN DE TAREAS ---
    st.subheader("Listado de Tareas")

    if not tareas:
        st.info("No hay tareas registradas. ¡Añade la primera!")
    else:
        df_tareas = pd.DataFrame(tareas)
        df_activas = df_tareas[df_tareas['Estado'] != 'Terminada']

        if df_activas.empty:
            st.success("🎉 ¡Felicidades! No hay tareas pendientes.")
        else:
            for index, row in df_activas.iterrows():
                color = category_colors.get(row.get("Categoría"), "#FFFFFF") # Color por defecto si no encuentra
                
                with st.container(border=True):
                    col_info, col_actions = st.columns([0.8, 0.2])
                    
                    with col_info:
                        st.markdown(f"**{row.get('Título')}**")
                        st.caption(f"Asignada a: {row.get('Usuario Asignado')} | Fecha Límite: {row.get('Fecha Límite')}")
                        
                        # Usamos HTML para el círculo de color
                        st.markdown(f"""
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <div style="width: 15px; height: 15px; background-color: {color}; border-radius: 50%;"></div>
                                <span>{row.get('Categoría')}</span>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.progress(int(row.get("Avance (%)", 0)), text=f"{row.get('Avance (%)')}% - {row.get('Estado')}")

                    with col_actions:
                        # Botón para Editar
                        if st.button("✏️ Editar", key=f"edit_{row.get('ID')}"):
                            st.session_state.tarea_a_editar = row.to_dict()

                        # Botón para Eliminar
                        if st.button("🗑️ Borrar", key=f"del_{row.get('ID')}"):
                            eliminar_tarea(row.get('ID'))
                            st.rerun()
                            
    # --- MODAL DE EDICIÓN (fuera del bucle) ---
    if 'tarea_a_editar' in st.session_state:
        tarea_actual = st.session_state.tarea_a_editar
        
        @st.dialog("Editar Tarea")
        def edit_modal():
            with st.form("edit_form"):
                st.subheader("Modificando Tarea")
                
                nuevo_titulo = st.text_input("Título", value=tarea_actual.get('Título'))
                nueva_desc = st.text_area("Descripción", value=tarea_actual.get('Descripción'))
                
                # Para evitar errores con fechas vacías o mal formateadas
                try:
                    fecha_val = datetime.strptime(tarea_actual.get('Fecha Límite'), "%Y-%m-%d").date()
                except (TypeError, ValueError):
                    fecha_val = datetime.now().date()
                    
                nueva_fecha = st.date_input("Fecha Límite", value=fecha_val)
                
                # Buscamos los índices para los selectbox
                user_index = nombres_usuarios.index(tarea_actual.get('Usuario Asignado')) if tarea_actual.get('Usuario Asignado') in nombres_usuarios else 0
                cat_index = categorias.index(tarea_actual.get('Categoría')) if tarea_actual.get('Categoría') in categorias else 0
                
                nuevo_usuario = st.selectbox("Asignar a:", options=nombres_usuarios, index=user_index)
                nueva_categoria = st.selectbox("Categoría:", options=categorias, index=cat_index)

                if st.form_submit_button("Guardar Cambios"):
                    datos_actualizados = {
                        "titulo": nuevo_titulo, "descripcion": nueva_desc, "usuario": nuevo_usuario,
                        "categoria": nueva_categoria, "fecha_limite": nueva_fecha,
                        "estado": tarea_actual.get("Estado"), # Mantenemos el estado y avance
                        "avance": tarea_actual.get("Avance (%)")
                    }
                    if actualizar_tarea(tarea_actual.get('ID'), datos_actualizados):
                        st.success("Tarea actualizada correctamente.")
                        del st.session_state.tarea_a_editar # Cerramos el modal
                        st.rerun()
        
        edit_modal()


    st.divider()

    # --- SECCIÓN PARA ACTUALIZAR ESTADO Y AÑADIR COMENTARIOS ---
    st.subheader("⚙️ Actualizar Avance y Añadir Comentarios")

    tareas_no_terminadas = [t for t in tareas if t.get('Estado') != 'Terminada']
    if not tareas_no_terminadas:
        st.write("No hay tareas activas para actualizar.")
    else:
        opciones_tareas = {f"{t.get('Título')} (Asignada a: {t.get('Usuario Asignado')})": t.get('ID') for t in tareas_no_terminadas}
        tarea_seleccionada_str = st.selectbox("Selecciona una tarea", options=opciones_tareas.keys())
        
        id_tarea_seleccionada = opciones_tareas[tarea_seleccionada_str]
        tarea_a_actualizar = next((t for t in tareas_no_terminadas if t.get('ID') == id_tarea_seleccionada), None)

        if tarea_a_actualizar:
            # Sección de Actualización de Estado
            with st.form("actualizar_estado_form"):
                st.write(f"**Actualizando:** {tarea_a_actualizar.get('Título')}")
                
                try:
                    avance_actual = int(tarea_a_actualizar.get("Avance (%)"))
                except (ValueError, TypeError):
                    avance_actual = 0
                
                nuevo_estado = st.selectbox(
                    "Nuevo Estado", ["Pendiente", "En Proceso", "Terminada"],
                    index=["Pendiente", "En Proceso", "Terminada"].index(tarea_a_actualizar.get("Estado"))
                )
                nuevo_avance = st.slider("Nuevo Porcentaje de Avance (%)", 0, 100, avance_actual)
                
                if st.form_submit_button("Actualizar Estado"):
                    if actualizar_estado_tarea(id_tarea_seleccionada, nuevo_estado, nuevo_avance):
                        st.success("¡Estado de la tarea actualizado!")
                        st.rerun()

            # Sección de Comentarios
            st.markdown("---")
            st.write(f"**Comentarios para:** {tarea_a_actualizar.get('Título')}")

            # Mostrar comentarios existentes
            comentarios_tarea = [c for c in comentarios if c.get('ID Tarea') == id_tarea_seleccionada]
            if not comentarios_tarea:
                st.info("Aún no hay comentarios para esta tarea.")
            else:
                for comm in sorted(comentarios_tarea, key=lambda x: x['Fecha'], reverse=True):
                    st.info(f"**{comm['Usuario']}** ({comm['Fecha']}):\n> {comm['Comentario']}")

            # Añadir nuevo comentario
            with st.form("comentario_form", clear_on_submit=True):
                usuario_comenta = st.selectbox("Tu usuario:", options=nombres_usuarios, key="user_comment")
                nuevo_comentario = st.text_area("Añadir un comentario:")
                
                if st.form_submit_button("Publicar Comentario"):
                    if nuevo_comentario:
                        guardar_comentario(id_tarea_seleccionada, usuario_comenta, nuevo_comentario)
                        st.rerun()

# Para ejecutar la aplicación (si este es el archivo principal)
# if __name__ == "__main__":
#     mostrar_pagina_inicio()
