# app.py (Versión Corregida con Fondo Corporativo)

import streamlit as st
from titulos import render_header
from inicio_view import mostrar_pagina_inicio
from usuarios_view import mostrar_pagina_usuarios

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Planilla efe",
    page_icon="fotos/logo1.png",
    layout="wide"
)

# --- APLICAR EL FONDO DE PANTALLA (MÉTODO CORREGIDO) ---
st.markdown("""
    <style>
        /* Selecciona el contenedor principal de la aplicación y el header */
        [data-testid="stAppViewContainer"] {
            background-color: #1c1c1c; /* El gris más oscuro para el fondo general */
        }
        
        [data-testid="stHeader"] {
            background-color: transparent; /* Hace que el header de Streamlit sea transparente */
        }

        /* Puedes mantener un color de fondo diferente para el área de contenido si lo deseas */
        /* Si quieres que TODO sea del mismo color, puedes comentar o eliminar este bloque */
        .main .block-container {
            background-color: #2E2E2E; 
            padding: 2rem;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)


# --- FUNCIÓN PRINCIPAL ---
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
        
# --- EJECUCIÓN DEL SCRIPT ---
if __name__ == "__main__":
    main()
