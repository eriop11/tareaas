# app.py (Versión actualizada)

import streamlit as st

# --- 1. IMPORTACIÓN DE MÓDULOS ---
from titulos import render_header
from inicio_view import mostrar_pagina_inicio
from usuarios_view import mostrar_pagina_usuarios # <-- 1. IMPORTA LA NUEVA FUNCIÓN

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Planilla efe",
    page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQmIYsfxtzoexc8rO1axPW8mMre5YasiQfwEw&s",
    layout="wide"
)

# --- FUNCIÓN PRINCIPAL ---
def main():
    
    vista_activa = render_header()
    
    # --- LÓGICA DE NAVEGACIÓN ---
    if vista_activa == "Inicio":
        mostrar_pagina_inicio()

    elif vista_activa == "Análisis":
        st.header("📈 Vista de Análisis")
        st.info("El contenido para esta sección se construirá en su propio archivo, como `analisis_view.py`.")

    elif vista_activa == "Reportes":
        st.header("📄 Vista de Reportes")
        st.info("El contenido para esta sección se construirá en su propio archivo, como `reportes_view.py`.")
        
    elif vista_activa == "Usuarios": # <-- 2. AÑADE ESTE ELIF
        mostrar_pagina_usuarios()
        
# --- EJECUCIÓN DEL SCRIPT ---
if __name__ == "__main__":
    main()
