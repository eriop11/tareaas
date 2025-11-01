# usuarios_view.py (Versión con Edición y Eliminación)

import streamlit as st
from gsheets_connector import get_sheet

# --- LÓGICA DE DATOS (Añadimos funciones de actualizar y eliminar) ---

@st.cache_data(ttl=300)
def cargar_usuarios():
    """
    Carga todos los usuarios desde la pestaña 'Usuarios' de Google Sheets.
    """
    worksheet = get_sheet("Usuarios")
    if worksheet:
        usuarios = worksheet.get_all_records()
        return usuarios
    return []

def guardar_nuevo_usuario(nombre: str, edad: int, url_foto: str):
    """
    Guarda un nuevo usuario en la hoja de cálculo.
    """
    worksheet = get_sheet("Usuarios")
    if worksheet:
        nueva_fila = [nombre, edad, url_foto]
        worksheet.append_row(nueva_fila)
        st.cache_data.clear()
        return True
    return False

def actualizar_usuario(nombre_original: str, nuevos_datos: dict):
    """
    Encuentra un usuario por su nombre original y actualiza sus datos.
    """
    worksheet = get_sheet("Usuarios")
    if worksheet:
        # get_all_records() es una lista de diccionarios
        registros = worksheet.get_all_records()
        # Buscamos la fila correcta. Empezamos en 2 porque las filas de gspread son 1-indexadas y la 1 es el header.
        for i, registro in enumerate(registros, start=2):
            if registro.get("Nombre") == nombre_original:
                # Encontramos la fila, ahora actualizamos las celdas
                worksheet.update_cell(i, 1, nuevos_datos['nombre']) # Columna 1 es Nombre
                worksheet.update_cell(i, 2, nuevos_datos['edad'])   # Columna 2 es Edad
                worksheet.update_cell(i, 3, nuevos_datos['url_foto']) # Columna 3 es URL_Foto_Perfil
                st.cache_data.clear()
                return True
    return False

def eliminar_usuario(nombre_a_eliminar: str):
    """
    Encuentra un usuario por su nombre y elimina la fila completa.
    """
    worksheet = get_sheet("Usuarios")
    if worksheet:
        registros = worksheet.get_all_records()
        for i, registro in enumerate(registros, start=2):
            if registro.get("Nombre") == nombre_a_eliminar:
                # Encontramos la fila, la eliminamos
                worksheet.delete_rows(i)
                st.cache_data.clear()
                return True
    return False


# --- LÓGICA DE LA INTERFAZ (VISTA CON SECCIÓN DE ADMINISTRACIÓN) ---

def mostrar_pagina_usuarios():
    st.header("👥 Gestión de Usuarios")
    st.write("Aquí puedes ver la lista de usuarios, añadir nuevos, editarlos o eliminarlos.")
    
    # --- SECCIÓN PARA AÑADIR NUEVO USUARIO (Usando un expander) ---
    with st.expander("➕ Añadir Nuevo Usuario"):
        with st.form("nuevo_usuario_form", clear_on_submit=True):
            nombre = st.text_input("Nombre completo del usuario")
            edad = st.number_input("Edad", min_value=1, max_value=120, step=1)
            url_foto = st.text_input("URL de la foto de perfil", placeholder="https://ejemplo.com/imagen.png")
            
            submitted_add = st.form_submit_button("Guardar Usuario")
            
            if submitted_add:
                if nombre and edad and url_foto:
                    if guardar_nuevo_usuario(nombre, edad, url_foto):
                        st.success(f"¡Usuario '{nombre}' guardado con éxito!")
                        st.rerun() # Recarga la página para mostrar los cambios al instante
                else:
                    st.warning("Por favor, completa todos los campos.")

    st.divider()

    # --- SECCIÓN PARA EDITAR O ELIMINAR USUARIOS EXISTENTES ---
    st.subheader("⚙️ Administrar Usuarios Existentes")
    
    usuarios_cargados = cargar_usuarios()
    
    if not usuarios_cargados:
        st.info("No hay usuarios para administrar.")
    else:
        # Menú desplegable para seleccionar un usuario
        nombres_usuarios = [usuario.get("Nombre") for usuario in usuarios_cargados]
        usuario_a_editar_nombre = st.selectbox(
            "Selecciona un usuario para editar o eliminar",
            options=nombres_usuarios
        )
        
        # Obtenemos los datos completos del usuario seleccionado
        usuario_seleccionado = next(
            (u for u in usuarios_cargados if u.get("Nombre") == usuario_a_editar_nombre), None
        )

        if usuario_seleccionado:
            # Formulario para editar los datos del usuario seleccionado
            with st.form("editar_usuario_form"):
                st.write(f"Editando el perfil de **{usuario_seleccionado.get('Nombre')}**")
                
                nuevo_nombre = st.text_input("Nombre", value=usuario_seleccionado.get("Nombre"))
                nueva_edad = st.number_input("Edad", min_value=1, max_value=120, step=1, value=usuario_seleccionado.get("Edad"))
                nueva_url_foto = st.text_input("URL de la foto de perfil", value=usuario_seleccionado.get("URL_Foto_Perfil"))

                submitted_edit = st.form_submit_button("Guardar Cambios")

                if submitted_edit:
                    nuevos_datos = {"nombre": nuevo_nombre, "edad": nueva_edad, "url_foto": nueva_url_foto}
                    if actualizar_usuario(usuario_a_editar_nombre, nuevos_datos):
                        st.success(f"¡Perfil de '{nuevo_nombre}' actualizado!")
                        st.rerun() # Recarga la página para reflejar los cambios
                    else:
                        st.error("No se pudo actualizar el usuario.")

            # Botón para eliminar (fuera del formulario de edición)
            st.warning(f"**Atención:** La siguiente acción es irreversible.", icon="⚠️")
            if st.button(f"Eliminar a {usuario_a_editar_nombre}", type="primary"):
                if eliminar_usuario(usuario_a_editar_nombre):
                    st.success(f"Usuario '{usuario_a_editar_nombre}' eliminado correctamente.")
                    st.rerun() # Recarga la página
                else:
                    st.error("No se pudo eliminar el usuario.")
    
    st.divider()

    # --- MOSTRAR LISTA DE USUARIOS EN UNA CUADRÍCULA (Sin cambios) ---
    st.subheader("Listado de Usuarios")
    
    # Recargamos por si hubo cambios
    usuarios_actualizados = cargar_usuarios()
    
    if not usuarios_actualizados:
        st.info("Aún no hay usuarios registrados.")
    else:
        num_columnas = 4
        cols = st.columns(num_columnas)
        for i, usuario in enumerate(usuarios_actualizados):
            columna_actual = cols[i % num_columnas]
            with columna_actual:
                with st.container(border=True):
                    st.image(
                        usuario.get("URL_Foto_Perfil") or "https://static.streamlit.io/examples/cat.jpg",
                        use_column_width='always'
                    )
                    st.subheader(f"{usuario.get('Nombre')}")
                    st.text(f"Edad: {usuario.get('Edad')}")
