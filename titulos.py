# titulos.py (Versión con Menú Espaciado)

import streamlit as st
from streamlit_option_menu import option_menu
import base64

@st.cache_data
def get_image_as_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        return None

def render_header():
    logo_base64 = get_image_as_base64("fotos/logo1.png")

    st.markdown("""
        <style>
            .header-container {
                display: flex; align-items: center; background-color: #010101;
                padding: 15px 25px; border-radius: 10px; margin-bottom: 1.5rem;
            }
            .header-icon svg {
                width: 45px; height: 45px; margin-right: 20px;
                color: #cb6012; flex-shrink: 0;
            }
            .header-title {
                font-size: 2.3rem; font-weight: 700; color: #EAECEE;
                padding: 0; margin: 0; line-height: 1;
            }
            .header-logo-img {
                height: 80px; margin-left: 15px; vertical-align: middle;
            }
        </style>
    """, unsafe_allow_html=True)

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
        st.error("Error: No se encontró el archivo del logo en la ruta 'fotos/logo1.png'.")

    selected_view = option_menu(
        menu_title=None,
        options=["Inicio", "Análisis", "Reportes", "Usuarios"],
        icons=['house-door-fill', 'bar-chart-line-fill', 'file-earmark-text-fill', 'people-fill'],
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#cb6012", "font-size": "18px"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "center",
                # --- CAMBIO CLAVE AQUÍ ---
                "margin": "0px 15px",  # Aumentamos el margen horizontal de 5px a 15px
                "padding": "8px 25px", # Añadimos padding para hacer los botones más grandes
                # -------------------------
                "--hover-color": "#4a4a4a"
            },
            "nav-link-selected": {"background-color": "#cb6012"},
        }
    )
    
    return selected_view
