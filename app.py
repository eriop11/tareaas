# app.py (Versión Restaurada al Tema Claro Original)

import streamlit as st
from titulos import render_header
from inicio_view import mostrar_pagina_inicio
from usuarios_view import mostrar_pagina_usuarios

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Planilla efe",
    page_icon="📊",  # Volvemos a un emoji simple
    layout="wide"
)

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
