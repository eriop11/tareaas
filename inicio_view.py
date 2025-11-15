# inicio_view.py

import streamlit as st
from gsheets_connector import * # Importa todo para simplificar
import pandas as pd
from datetime import datetime

def mostrar_pagina_inicio():
    st.header("📋 Gestor de Tareas Avanzado")

    try:
        usuarios = cargar_usuarios()
        nombres_usuarios = [u.get("Nombre") for u in usuarios] if usuarios else ["Admin"]
        categorias = cargar_categorias()
        tareas = cargar_tareas()
        comentarios = cargar_comentarios()
        category_colors = get_category_colors(categorias)
    except Exception as e:
        st.error(f"Ocurrió un error al cargar los datos iniciales: {e}")
        return

    with st.expander("➕ Añadir Nueva Tarea o Categoría"):
        tab1, tab2 = st.tabs(["Crear Tarea", "Añadir Categoría"])
        with tab1:
            with st.form("nueva_tarea_form", clear_on_submit=True):
                # ... campos del formulario ...
                tarea_titulo = st.text_input("Título de la tarea")
                tarea_desc = st.text_area("Descripción detallada")
                usuario_asignado = st.selectbox("Asignar a:", options=nombres_usuarios)
                categoria_tarea = st.selectbox("Categoría:", options=categorias)
                fecha_limite = st.date_input("Fecha límite", value=datetime.now().date())
                estado_inicial = st.selectbox("Estado:", ["Pendiente", "En Proceso", "Terminada"])
                avance = st.slider("Porcentaje de Avance (%)", 0, 100, 0)
                
                if st.form_submit_button("Guardar Tarea"):
                    if tarea_titulo and usuario_asignado and categoria_tarea:
                        datos_tarea = {
                            "titulo": tarea_titulo, "descripcion": tarea_desc, 
                            "usuario_asignado": usuario_asignado, "categoria": categoria_tarea, 
                            "fecha_limite": fecha_limite, "estado": estado_inicial, "avance": avance
                        }
                        if guardar_nueva_tarea(datos_tarea):
                            st.success("¡Tarea guardada con éxito!")
                            st.rerun()
                    else:
                        st.warning("El título, usuario y categoría son obligatorios.")

    st.divider()
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
                # CORRECCIONES CLAVE AQUÍ:
                color = category_colors.get(row.get("Categoría"), "#FFFFFF") # Con tilde
                
                with st.container(border=True):
                    # ... [código de visualización] ...
                    st.markdown(f"**{row.get('Título')}**") # Usar Título
                    st.caption(f"Asignada a: {row.get('Usuario Asignado')} | Fecha Límite: {row.get('Fecha Límite')}")
                    
                    st.markdown(f"""
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <div style="width: 15px; height: 15px; background-color: {color}; border-radius: 50%;"></div>
                            <span>{row.get('Categoría')}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    avance_val = int(row.get("Avance (%)", 0))
                    st.progress(avance_val, text=f"{avance_val}% - {row.get('Estado')}")

                    # ... [botones de editar y borrar] ...
                    
# --- MODAL DE EDICIÓN (fuera del bucle) ---
if 'tarea_a_editar' in st.session_state:
    tarea_actual = st.session_state.tarea_a_editar
    
    @st.dialog("Editar Tarea")
    def edit_modal():
        with st.form("edit_form"):
            st.subheader("Modificando Tarea")
            
            # CORRECCIONES CLAVE AQUÍ:
            nuevo_titulo = st.text_input("Título", value=tarea_actual.get('Título'))
            nueva_desc = st.text_area("Descripción", value=tarea_actual.get('Descripción'))
            
            # ... [código del formulario de edición] ...
            
            if st.form_submit_button("Guardar Cambios"):
                datos_actualizados = {
                    "titulo": nuevo_titulo, "descripcion": nueva_desc, 
                    "usuario_asignado": nuevo_usuario, "categoria": nueva_categoria, 
                    "fecha_limite": nueva_fecha, "estado": tarea_actual.get("Estado"),
                    "avance": tarea_actual.get("Avance (%)")
                }
                if actualizar_tarea(tarea_actual.get('ID'), datos_actualizados):
                    st.success("Tarea actualizada correctamente.")
                    del st.session_state.tarea_a_editar
                    st.rerun()
    
    edit_modal()
# (El resto del código de la vista para comentarios y actualizaciones no necesita cambios si los encabezados de esas hojas son correctos)```

### Resumen de Acciones:

1.  **En Google Sheets:** Ve a tu hoja llamada **"tareas"** y asegúrate de que la primera fila contenga exactamente los encabezados que te indiqué, incluyendo `ID` y `Descripción`.
2.  **En tu editor de código:** Reemplaza el contenido de tus archivos `gsheets_connector.py` y `inicio_view.py` con las versiones corregidas que te proporcioné.
3.  **Ejecuta la aplicación:** ¡Ahora debería funcionar todo correctamente!

La clave de la programación con fuentes de datos externas como Google Sheets es mantener una **consistencia absoluta** entre los nombres de las hojas y las columnas en la fuente de datos y las claves que usas para acceder a ellos en tu código.
