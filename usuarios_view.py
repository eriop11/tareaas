# usuarios_view.py (Versión Corregida con conversión de tipo)

import streamlit as st
from gsheets_connector import get_sheet

# --- LÓGICA DE DATOS (Sin cambios) ---

@st.cache_data(ttl=300)
def cargar_usuarios():
    worksheet = get_sheet("Usuarios")
    if worksheet:
        usuarios = worksheet.get_all_records()
        return usuarios
    return []

def guardar_nuevo_usuario(nombre: str, edad: int, url_foto: str):
    worksheet = get_sheet("Usuarios")
    if worksheet:
        nueva_fila = [nombre, edad, url_foto]
        worksheet.append_row(nueva_fila)
        st.cache_data.clear()
        return True
    return False

def actualizar_usuario(nombre_original: str, nuevos_datos: dict):
    worksheet = get_sheet("Usuarios")
    if worksheet:
        registros = worksheet.get_all_records()
        for i, registro in enumerate(registros, start=2):
            if registro.get("Nombre") == nombre_original:
                worksheet.update_cell(i, 1, nuevos_datos['nombre'])
                worksheet.update_cell(i, 2, nuevos_datos['edad'])
                worksheet.update_cell(i, 3, nuevos_datos['url_foto'])
                st.cache_data.clear()
                return True
    return False

def eliminar_usuario(nombre_a_eliminar: str):
    worksheet = get_sheet("Usuarios")
    if worksheet:
        registros = worksheet.get_all_records()
        for i, registro in enumerate(registros, start=2):
            if registro.get("Nombre") == nombre_a_eliminar:
                worksheet.delete_rows(i)
                st.cache_data.clear()
                return True
    return False


# --- LÓGICA DE LA INTERFAZ ---

def mostrar_pagina_usuarios():
    st.header("👥 Gestión de Usuarios")
    st.write("Aquí puedes ver la lista de usuarios, añadir nuevos, editarlos o eliminarlos.")
    
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
                        st.rerun()
                else:
                    st.warning("Por favor, completa todos los campos.")

    st.divider()

    st.subheader("⚙️ Administrar Usuarios Existentes")
    
    usuarios_cargados = cargar_usuarios()
    
    if not usuarios_cargados:
        st.info("No hay usuarios para administrar.")
    else:
        nombres_usuarios = [usuario.get("Nombre") for usuario in usuarios_cargados]
        usuario_a_editar_nombre = st.selectbox(
            "Selecciona un usuario para editar o eliminar",
            options=nombres_usuarios
        )
        
        usuario_seleccionado = next(
            (u for u in usuarios_cargados if u.get("Nombre") == usuario_a_editar_nombre), None
        )

        if usuario_seleccionado:
            with st.form("editar_usuario_form"):
                st.write(f"Editando el perfil de **{usuario_seleccionado.get('Nombre')}**")
                
                nuevo_nombre = st.text_input("Nombre", value=usuario_seleccionado.get("Nombre"))
                
                # ----- LÍNEA CORREGIDA AQUÍ -----
                # Convertimos el valor de la edad a entero (int) antes de pasarlo al widget
                try:
                    edad_actual = int(usuario_seleccionado.get("Edad"))
                except (ValueError, TypeError):
                    edad_actual = 1 # Un valor por defecto si la edad no es un número válido

                nueva_edad = st.number_input("Edad", min_value=1, max_value=120, step=1, value=edad_actual)
                # ---------------------------------
                
                nueva_url_foto = st.text_input("URL de la foto de perfil", value=usuario_seleccionado.get("URL_Foto_Perfil"))

                submitted_edit = st.form_submit_button("Guardar Cambios")

                if submitted_edit:
                    nuevos_datos = {"nombre": nuevo_nombre, "edad": nueva_edad, "url_foto": nueva_url_foto}
                    if actualizar_usuario(usuario_a_editar_nombre, nuevos_datos):
                        st.success(f"¡Perfil de '{nuevo_nombre}' actualizado!")
                        st.rerun()
                    else:
                        st.error("No se pudo actualizar el usuario.")

            st.warning(f"**Atención:** La siguiente acción es irreversible.", icon="⚠️")
            if st.button(f"Eliminar a {usuario_a_editar_nombre}", type="primary"):
                if eliminar_usuario(usuario_a_editar_nombre):
                    st.success(f"Usuario '{usuario_a_editar_nombre}' eliminado correctamente.")
                    st.rerun()
                else:
                    st.error("No se pudo eliminar el usuario.")
    
    st.divider()

    st.subheader("Listado de Usuarios")
    
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
