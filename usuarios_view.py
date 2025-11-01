# usuarios_view.py

import streamlit as st
from gsheets_connector import get_sheet

# --- LÓGICA DE DATOS ---

@st.cache_data(ttl=300) # Cachear por 5 minutos
def cargar_usuarios():
    """
    Carga todos los usuarios desde la pestaña 'Usuarios' de Google Sheets.
    """
    worksheet = get_sheet("Usuarios")
    if worksheet:
        # get_all_records convierte la hoja en una lista de diccionarios
        usuarios = worksheet.get_all_records()
        return usuarios
    return [] # Devuelve una lista vacía si hay un error

def guardar_nuevo_usuario(nombre: str, edad: int, url_foto: str):
    """
    Guarda un nuevo usuario en la hoja de cálculo.
    """
    worksheet = get_sheet("Usuarios")
    if worksheet:
        # La lista debe tener el mismo orden que las columnas: Nombre, Edad, URL_Foto_Perfil
        nueva_fila = [nombre, edad, url_foto]
        worksheet.append_row(nueva_fila)
        st.cache_data.clear() # Limpia la caché para que la lista se actualice al instante
        return True
    return False

# --- LÓGICA DE LA INTERFAZ (VISTA) ---

def mostrar_pagina_usuarios():
    """
    Construye la página completa de gestión de usuarios.
    """
    st.header("👥 Gestión de Usuarios")
    st.write("Aquí puedes ver la lista de usuarios y añadir nuevos perfiles.")
    
    st.divider()

    # --- MOSTRAR LISTA DE USUARIOS EXISTENTES ---
    st.subheader("Listado de Usuarios")
    
    usuarios_cargados = cargar_usuarios()
    
    if not usuarios_cargados:
        st.info("Aún no hay usuarios registrados. ¡Añade el primero!")
    else:
        # Crear columnas para una visualización más ordenada
        for usuario in usuarios_cargados:
            col1, col2 = st.columns([1, 4]) # La columna 2 es 4 veces más ancha que la 1
            with col1:
                # Usar un placeholder si la URL de la foto está vacía
                st.image(
                    usuario.get("URL_Foto_Perfil") or "https://static.streamlit.io/examples/cat.jpg",
                    width=100,
                    caption=usuario.get("Nombre")
                )
            with col2:
                st.subheader(usuario.get("Nombre"))
                st.write(f"**Edad:** {usuario.get('Edad')}")
            
            st.divider()

    # --- FORMULARIO PARA AÑADIR NUEVO USUARIO ---
    st.subheader("Añadir Nuevo Usuario")
    
    with st.form("nuevo_usuario_form", clear_on_submit=True):
        nombre = st.text_input("Nombre completo del usuario")
        edad = st.number_input("Edad", min_value=1, max_value=120, step=1)
        url_foto = st.text_input("URL de la foto de perfil", placeholder="https://ejemplo.com/imagen.png")
        
        submitted = st.form_submit_button("Guardar Usuario")
        
        if submitted:
            if nombre and edad and url_foto:
                if guardar_nuevo_usuario(nombre, edad, url_foto):
                    st.success(f"¡Usuario '{nombre}' guardado con éxito!")
                else:
                    st.error("No se pudo guardar el usuario. Revisa la conexión.")
            else:
                st.warning("Por favor, completa todos los campos.")
