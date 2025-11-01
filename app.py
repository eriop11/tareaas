# app.py

import streamlit as st
# Importamos la única función que necesitamos desde nuestro módulo de UI
from titulos import render_header

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Planilla efe",
    page_icon="📊",
    layout="wide"
)

# --- FUNCIÓN PRINCIPAL ---
def main():
    
    # 1. RENDERIZAR HEADER Y OBTENER LA VISTA ACTIVA
    #    Toda la complejidad está oculta en la función render_header()
    vista_activa = render_header()
    
    # 2. MOSTRAR CONTENIDO BASADO EN LA SELECCIÓN
    #    Aquí es donde llamas a las funciones específicas de cada sección.
    
    if vista_activa == "Inicio":
        # --- SECCIÓN INICIO ---
        st.header("🏠 Vista de Inicio")
        # Llama aquí a tus funciones para la página de inicio
        # ej: mostrar_kpis_generales()

    elif vista_activa == "Análisis":
        # --- SECCIÓN ANÁLISIS ---
        st.header("📈 Vista de Análisis")
        # Llama aquí a tus funciones de gráficos y análisis
        # ej: mostrar_grafico_ventas()
        # ej: mostrar_analisis_correlacion()

    elif vista_activa == "Reportes":
        # --- SECCIÓN REPORTES ---
        st.header("📄 Vista de Reportes")
        # Llama aquí a tus funciones para generar reportes
        # ej: generar_reporte_pdf()
        
# --- EJECUCIÓN ---
if __name__ == "__main__":
    main()
