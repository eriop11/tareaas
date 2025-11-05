# inicio_view.py (Versión Corregida)

import streamlit as st
# Importamos TODAS las funciones necesarias desde el conector
from gsheets_connector import (
    cargar_usuarios, # Suponiendo que esta función también está en tu conector o en usuarios_view
    cargar_categorias,
    cargar_tareas,
    cargar_comentarios,
    get_category_colors,
    guardar_nueva_tarea,
    guardar_nueva_categoria,
    eliminar_tarea,
    actualizar_tarea,
    actualizar_estado_tarea,
    guardar_comentario
)
# Si cargar_usuarios está en otro archivo, mantenemos la importación original
# from usuarios_view import cargar_usuarios 
import pandas as pd
from datetime import datetime

# --- VISTA PRINCIPAL ---

def mostrar_pagina_inicio():
    st.header("📋 Gestor de Tareas Avanzado")

    # --- Carga de datos ---
    # NOTA: Asegúrate de que la función cargar_usuarios() está definida donde corresponde.
    # Por ahora, la comentaré para evitar errores si no la tienes.
    # usuarios = cargar_usuarios() 
    # nombres_usuarios = [u.get("Nombre") for u in usuarios]
    
    # Usaremos una lista temporal de usuarios si la función no existe aún
    nombres_usuarios = ["Usuario A", "Usuario B", "Admin"]

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
                    if tarea_titulo:
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
        tareas_validas = [t for t in tareas if t.get('ID')]
        
        if not tareas_validas:
             st.info("No hay tareas válidas con ID para mostrar.")
        else:
            df_tareas = pd.DataFrame(tareas_validas)
            df_activas = df_tareas[df_tareas['Estado'] != 'Terminada']

            if df_activas.empty:
                st.success("🎉 ¡Felicidades! No hay tareas pendientes.")
            else:
                for index, row in df_activas.iterrows():
                    color = category_colors.get(row.get("Categoria"), "#FFFFFF") # Corregido a "Categoria" si así se llama en tu GSheet
                    
                    with st.container(border=True):
                        col_info, col_actions = st.columns([0.8, 0.2])
                        
                        with col_info:
                            st.markdown(f"**{row.get('Título')}**")
                            st.caption(f"Asignada a: {row.get('Usuario Asignado')} | Fecha Límite: {row.get('Fecha Límite')}")
                            
                            st.markdown(f"""
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <div style="width: 15px; height: 15px; background-color: {color}; border-radius: 50%;"></div>
                                    <span>{row.get('Categoria')}</span>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            avance_val = int(row.get("Avance (%)", 0))
                            st.progress(avance_val, text=f"{avance_val}% - {row.get('Estado')}")

                        with col_actions:
                            if st.button("✏️ Editar", key=f"edit_{row.get('ID')}_{index}"):
                                st.session_state.tarea_a_editar = row.to_dict()

                            if st.button("🗑️ Borrar", key=f"del_{row.get('ID')}_{index}"):
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
                    fecha_val = datetime.strptime(str(tarea_actual.get('Fecha Límite')), "%Y-%m-%d").date()
                except (TypeError, ValueError):
                    fecha_val = datetime.now().date()
                    
                nueva_fecha = st.date_input("Fecha Límite", value=fecha_val)
                
                user_index = nombres_usuarios.index(tarea_actual.get('Usuario Asignado')) if tarea_actual.get('Usuario Asignado') in nombres_usuarios else 0
                cat_index = categorias.index(tarea_actual.get('Categoria')) if tarea_actual.get('Categoria') in categorias else 0
                
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
    
    tareas_no_terminadas = [t for t in tareas if t.get('Estado') != 'Terminada' and t.get('ID')]
    if not tareas_no_terminadas:
        st.write("No hay tareas activas para actualizar.")
    else:
        opciones_tareas = {f"{t.get('Título')} (Asignada a: {t.get('Usuario Asignado')})": t.get('ID') for t in tareas_no_terminadas}
        tarea_seleccionada_str = st.selectbox("Selecciona una tarea", options=opciones_tareas.keys())
        
        id_tarea_seleccionada = opciones_tareas[tarea_seleccionada_str]
        tarea_a_actualizar = next((t for t in tareas_no_terminadas if t.get('ID') == id_tarea_seleccionada), None)

        if tarea_a_actualizar:
            with st.form("actualizar_estado_form", key=f"update_form_{id_tarea_seleccionada}"):
                st.write(f"**Actualizando:** {tarea_a_actualizar.get('Título')}")
                
                avance_actual = int(tarea_a_actualizar.get("Avance (%)", 0))
                
                estados = ["Pendiente", "En Proceso", "Terminada"]
                estado_actual_idx = estados.index(tarea_a_actualizar.get("Estado")) if tarea_a_actualizar.get("Estado") in estados else 0

                nuevo_estado = st.selectbox(
                    "Nuevo Estado", estados, index=estado_actual_idx
                )
                nuevo_avance = st.slider("Nuevo Porcentaje de Avance (%)", 0, 100, avance_actual)
                
                if st.form_submit_button("Actualizar Estado"):
                    if actualizar_estado_tarea(id_tarea_seleccionada, nuevo_estado, nuevo_avance):
                        st.success("¡Estado de la tarea actualizado!")
                        st.rerun()

            st.markdown("---")
            st.write(f"**Comentarios para:** {tarea_a_actualizar.get('Título')}")

            comentarios_tarea = [c for c in comentarios if str(c.get('ID Tarea')) == str(id_tarea_seleccionada)]
            if not comentarios_tarea:
                st.info("Aún no hay comentarios para esta tarea.")
            else:
                for comm in sorted(comentarios_tarea, key=lambda x: x.get('Fecha', ''), reverse=True):
                    st.info(f"**{comm.get('Usuario')}** ({comm.get('Fecha')}):\n> {comm.get('Comentario')}")

            with st.form("comentario_form", clear_on_submit=True, key=f"comment_form_{id_tarea_seleccionada}"):
                usuario_comenta = st.selectbox("Tu usuario:", options=nombres_usuarios, key="user_comment")
                nuevo_comentario = st.text_area("Añadir un comentario:")
                
                if st.form_submit_button("Publicar Comentario"):
                    if nuevo_comentario:
                        guardar_comentario(id_tarea_seleccionada, usuario_comenta, nuevo_comentario)
                        st.rerun()```
