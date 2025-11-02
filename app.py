# app.py (Versión con Header Oscuro y Contenido Claro)

import streamlit as st
from titulos import render_header
from inicio_view import mostrar_pagina_inicio
from usuarios_view import mostrar_pagina_usuarios

st.set_page_config(
    page_title="Planilla efe",
    page_icon="fotos/logo1.png",
    layout="wide"
)

# --- APLICAR ESTILOS GLOBALES (Header Oscuro, Contenido Claro) ---
st.markdown("""
    <style>
        /* Fondo general de la aplicación */
        [data-testid="stAppViewContainer"] {
            background-color: #f0f2f6; /* Un gris muy claro, más suave que el blanco puro */
        }
        
        /* Aseguramos que el texto por defecto sea negro */
        body, p, li {
            color: #111111;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #111111;
        }

        /* Header de Streamlit (transparente para que se vea el fondo) */
        [data-testid="stHeader"] {
            background-color: transparent;
        }

        /* Área de contenido principal (fondo blanco) */
        .main .block-container {
            background-color: #ffffff; /* Blanco puro */
            color: #111111; /* Aseguramos que el texto dentro sea negro */
            padding: 2rem;
            border-radius: 10px;
            border: 1px solid #e6e9ef; /* Un borde sutil para definir el área */
        }

        /* --- ESTILOS PARA QUE LOS WIDGETS SE VEAN BIEN EN TEMA CLARO --- */

        /* Estilo para los campos de texto y número */
        [data-testid="stTextInput"] input, 
        [data-testid="stNumberInput"] input {
            background-color: #ffffff;
            color: #111111;
            border: 1px solid #ccc; /* Borde gris estándar */
        }

        /* Color del texto de las etiquetas de los inputs */
        [data-testid="stTextInput"] label,
        [data-testid="stNumberInput"] label {
            color: #111111 !important; 
        }

        /* Hacer visible la línea divisoria */
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
        
# --- EJECUCIÓN DEL SCRIPT ---
if __name__ == "__main__":
    main()
