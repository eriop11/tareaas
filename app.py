# app.py

import streamlit as st

# --- 1. IMPORTACIÓN DE MÓDULOS ---
# Importamos las funciones de nuestros archivos separados.
# Cada archivo se encarga de una parte específica de la app.
from titulos import render_header
from inicio_view import mostrar_pagina_inicio  # <-- ESTA ES LA CONEXIÓN IMPORTANTE

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Planilla efe",
    page_icon="📊",
    layout="wide"
)

# --- FUNCIÓN PRINCIPAL ---
def main():
    
    # El header nos dice qué vista quiere ver el usuario.
    vista_activa = render_header()
    
    # --- LÓGICA DE NAVEGACIÓN ---
    # Usamos la respuesta del header para decidir qué función llamar.
    
    if vista_activa == "Inicio":
        # Si el usuario eligió "Inicio", llamamos a la función
        # que construye esa página.
        mostrar_pagina_inicio()  # <-- AQUÍ SE "ACTIVA" TU CÓDIGO NUEVO

    elif vista_activa == "Análisis":
        # Placeholder para la vista de Análisis
        st.header("📈 Vista de Análisis")
        st.info("El contenido para esta sección se construirá en su propio archivo, como `analisis_view.py`.")
        # Aquí llamarías a: mostrar_pagina_analisis()

    elif vista_activa == "Reportes":
        # Placeholder para la vista de Reportes
        st.header("📄 Vista de Reportes")
        st.info("El contenido para esta sección se construirá en su propio archivo, como `reportes_view.py`.")
        # Aquí llamarías a: mostrar_pagina_reportes()
        
# --- EJECUCIÓN DEL SCRIPT ---
if __name__ == "__main__":
    main()
