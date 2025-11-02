# titulos.py (Versión Corregida con Sintaxis Válida)

import streamlit as st
from streamlit_option_menu import option_menu
import base64

# --- FUNCIÓN AUXILIAR (Ahora está fuera de render_header) ---
# Se cachea para que solo se ejecute una vez y sea más eficiente.
@st.cache_data
def get_image_as_base64(path):
    """
    Lee un archivo de imagen local y lo convierte a formato Base64.
    """
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        # Devuelve None si no encuentra la imagen para que podamos manejar el error.
        return None

# --- FUNCIÓN PRINCIPAL ---
def render_header():
    """
    Renderiza el header completo con un logo en lugar del texto "efe".
    """
    # Obtenemos la imagen codificada llamando a nuestra función auxiliar
    logo_base64 = get_image_as_base64("fotos/logo1.png")

    # 1. CSS (sin cambios)
    st.markdown("""
        <style>
            .header-container {
                display: flex;
                align-items: center;
                background-color: #262730;
                padding: 15px 25px;
                border-radius: 10px;
                margin-bottom: 1.5rem;
            }
            .header-icon svg {
                width: 45px;
                height: 45px;
                margin-right: 20px;
                color: #5DADE2;
                flex-shrink: 0;
            }
            .header-title {
                font-size: 2.3rem;
                font-weight: 700;
                color: #EAECEE;
                padding: 0;
                margin: 0;
                line-height: 1;
            }
            .header-logo-img {
                height: 50px;
                margin-left: 15px;
                vertical-align: middle;
            }
        </style>
    """, unsafe_allow_html=True)

    # 2. HTML que muestra el logo
    if logo_base64:
        st.markdown(f"""
            <div class="header-container">
                <div class="header-icon">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                    </svg>
                </div>
                <div>
                    <p class="header-title">
                        Planilla de trabajo de 
                        <img src="data:image/png;base64,{logo_base64}" class="header-logo-img">
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Mensaje de error si el logo no se encuentra, para facilitar la depuración
        st.error("Error: No se encontró el archivo del logo en la ruta 'fotos/logo.png'.")

    # 3. Menú de navegación (sin cambios)
    selected_view = option_menu(
        menu_title=None,
        options=["Inicio", "Análisis", "Reportes", "Usuarios"],
        icons=['house-door-fill', 'bar-chart-line-fill', 'file-earmark-text-fill', 'people-fill'],
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "orange", "font-size": "18px"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "center",
                "margin": "0px 5px",
                "--hover-color": "#3e4249"
            },
            "nav-link-selected": {"background-color": "#2F80ED"},
        }
    )
    
    return selected_view
