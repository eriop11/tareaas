# inicio_view.py (Versión Corregida)

# ... (todas las funciones de datos de arriba permanecen igual) ...
import streamlit as st
from gsheets_connector import get_sheet
from usuarios_view import cargar_usuarios # Importamos la función para cargar usuarios
import pandas as pd # Usaremos pandas para mostrar las tareas en una tabla bonita
from datetime import datetime
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
        # Filtramos primero las tareas que no tengan un ID para evitar problemas
        tareas_validas = [t for t in tareas if t.get('ID')]
        df_tareas = pd.DataFrame(tareas_validas)
        
        # Continuamos solo si el dataframe no está vacío después de filtrar
        if not df_tareas.empty:
            df_activas = df_tareas[df_tareas['Estado'] != 'Terminada']

            if df_activas.empty:
                st.success("🎉 ¡Felicidades! No hay tareas pendientes.")
            else:
                for index, row in df_activas.iterrows():
                    color = category_colors.get(row.get("Categoría"), "#FFFFFF")
                    
                    with st.container(border=True):
                        col_info, col_actions = st.columns([0.8, 0.2])
                        
                        with col_info:
                            st.markdown(f"**{row.get('Título')}**")
                            st.caption(f"Asignada a: {row.get('Usuario Asignado')} | Fecha Límite: {row.get('Fecha Límite')}")
                            
                            st.markdown(f"""
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <div style="width: 15px; height: 15px; background-color: {color}; border-radius: 50%;"></div>
                                    <span>{row.get('Categoría')}</span>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            st.progress(int(row.get("Avance (%)", 0)), text=f"{row.get('Avance (%)')}% - {row.get('Estado')}")

                        with col_actions:
                            # Botón para Editar
                            if st.button("✏️ Editar", key=f"edit_{row.get('ID')}_{index}"): # <-- CAMBIO AQUÍ
                                st.session_state.tarea_a_editar = row.to_dict()

                            # Botón para Eliminar
                            if st.button("🗑️ Borrar", key=f"del_{row.get('ID')}_{index}"): # <-- CAMBIO AQUÍ
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
                
                try:
                    fecha_val = datetime.strptime(tarea_actual.get('Fecha Límite'), "%Y-%m-%d").date()
                except (TypeError, ValueError):
                    fecha_val = datetime.now().date()
                    
                nueva_fecha = st.date_input("Fecha Límite", value=fecha_val)
                
                user_index = nombres_usuarios.index(tarea_actual.get('Usuario Asignado')) if tarea_actual.get('Usuario Asignado') in nombres_usuarios else 0
                cat_index = categorias.index(tarea_actual.get('Categoría')) if tarea_actual.get('Categoría') in categorias else 0
                
                nuevo_usuario = st.selectbox("Asignar a:", options=nombres_usuarios, index=user_index)
                nueva_categoria = st.selectbox("Categoría:", options=categorias, index=cat_index)

                if st.form_submit_button("Guardar Cambios"):
                    datos_actualizados = {
                        "titulo": nuevo_titulo, "descripcion": nueva_desc, "usuario": nuevo_usuario,
                        "categoria": nueva_categoria, "fecha_limite": nueva_fecha,
                        "estado": tarea_actual.get("Estado"),
                        "avance": tarea_actual.get("Avance (%)")
                    }
                    if actualizar_tarea(tarea_actual.get('ID'), datos_actualizados):
                        st.success("Tarea actualizada correctamente.")
                        del st.session_state.tarea_a_editar
                        st.rerun()
        
        edit_modal()


    st.divider()

    # --- SECCIÓN PARA ACTUALIZAR ESTADO Y AÑADIR COMENTARIOS ---
    st.subheader("⚙️ Actualizar Avance y Añadir Comentarios")
    
    # Nos aseguramos de trabajar solo con tareas que tienen ID
    tareas_no_terminadas = [t for t in tareas if t.get('Estado') != 'Terminada' and t.get('ID')]
    if not tareas_no_terminadas:
        st.write("No hay tareas activas para actualizar.")
    else:
        opciones_tareas = {f"{t.get('Título')} (Asignada a: {t.get('Usuario Asignado')})": t.get('ID') for t in tareas_no_terminadas}
        tarea_seleccionada_str = st.selectbox("Selecciona una tarea", options=opciones_tareas.keys())
        
        id_tarea_seleccionada = opciones_tareas[tarea_seleccionada_str]
        tarea_a_actualizar = next((t for t in tareas_no_terminadas if t.get('ID') == id_tarea_seleccionada), None)

        if tarea_a_actualizar:
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

            st.markdown("---")
            st.write(f"**Comentarios para:** {tarea_a_actualizar.get('Título')}")

            comentarios_tarea = [c for c in comentarios if c.get('ID Tarea') == id_tarea_seleccionada]
            if not comentarios_tarea:
                st.info("Aún no hay comentarios para esta tarea.")
            else:
                for comm in sorted(comentarios_tarea, key=lambda x: x['Fecha'], reverse=True):
                    st.info(f"**{comm['Usuario']}** ({comm['Fecha']}):\n> {comm['Comentario']}")

            with st.form("comentario_form", clear_on_submit=True):
                usuario_comenta = st.selectbox("Tu usuario:", options=nombres_usuarios, key="user_comment")
                nuevo_comentario = st.text_area("Añadir un comentario:")
                
                if st.form_submit_button("Publicar Comentario"):
                    if nuevo_comentario:
                        guardar_comentario(id_tarea_seleccionada, usuario_comenta, nuevo_comentario)
                        st.rerun()
