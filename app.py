# app.py (Versión Definitiva con Fondo Uniforme)

import streamlit as st
from titulos import render_header
from inicio_view import mostrar_pagina_inicio
from usuarios_view import mostrar_pagina_usuarios

st.set_page_config(
    page_title="Planilla efe",
    page_icon="fotos/logo1.png",
    layout="wide"
)

# --- APLICAR ESTILOS GLOBALES (MÉTODO DEFINITIVO) ---
st.markdown("""
    <style>
        /* Fondo general de la aplicación */
        body {
            background-color: #f0f2f6; /* El gris claro que te gusta */
        }
        
        /* Contenedor principal de la app */
        [data-testid="stAppViewContainer"] {
            background-color: #f0f2f6;
        }

        /* --- CAMBIO CLAVE Y DEFINITIVO --- */
        /* Forzamos el color de fondo en el contenedor principal y eliminamos sus bordes y sombras */
        [data-testid="stVerticalBlock"] {
            background-color: #f0f2f6;
        }
        .main .block-container {
            background-color: #f0f2f6;
            border: none;
            box-shadow: none;
        }
        /* -------------------------------------- */

        /* Aseguramos que el texto por defecto sea negro */
        body, p, li, h1, h2, h3, h4, h5, h6 {
            color: #111111;
        }

        /* Header de Streamlit (transparente) */
        [data-testid="stHeader"] {
            background-color: transparent;
        }

        /* Estilos para los widgets en tema claro */
        [data-testid="stTextInput"] input, 
        [data-testid="stNumberInput"] input {
            background-color: #ffffff;
            color: #111111;
            border: 1px solid #ccc;
        }
        [data-testid="stTextInput"] label,
        [data-testid="stNumberInput"] label {
            color: #111111 !important; 
        }
        [data-testid="stDivider"] > div {
            border-top: 1px solid #ccc;
        }
    </style>
""", unsafe_allow_html=True)


# --- FUNCIÓN PRINCIPAL (Sin cambios) ---
def main():
    vista_activa = render_header()
    
    if vista_activa == "Inicio":
        mostrar_pagina_inicio()
    elif vista_activa == "Análisis":
        st.header("📈 Vista de Análisis")
        st.info("El contenido para esta sección se construirá en su propio archivo, como `analisis_view.py`.")
    elif vista_activa == "Reportes":
        st.header("📄 Vista de Reportes")
        st.info("El contenido para esta sección se construirá en su propio archivo, como `reportes_view.py`.")
    elif vista_activa == "Usuarios":
        mostrar_pagina_usuarios()
        
if __name__ == "__main__":
    main()
