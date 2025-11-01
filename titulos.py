# titulos.py

import streamlit as st
from streamlit_option_menu import option_menu

def render_header():
    """
    Renderiza el header completo con un diseño mejorado:
    - Fondo de contenedor gris-azulado oscuro.
    - Título "Planilla de trabajo" más grande.
    - "efe" aún más grande y en cursiva (bastardilla).
    
    Devuelve:
        str: El nombre de la vista seleccionada en el menú de navegación.
    """
    
    # 1. CSS mejorado para el nuevo estilo
    #    - Se agrega un fondo, padding y bordes redondeados al contenedor.
    #    - Se ajustan los tamaños de fuente y se añade una clase para 'efe'.
    #    - 'align-items: baseline' alinea el texto grande y el más grande por la base.
    st.markdown("""
        <style>
            .header-container {
                display: flex;
                align-items: baseline; /* Alinea textos de distinto tamaño por la base */
                background-color: #262730; /* Fondo gris-azulado oscuro */
                padding: 20px 25px;
                border-radius: 10px;
                margin-bottom: 1.5rem; /* Más separación con el menú */
            }
            .header-icon svg {
                width: 45px; /* Ícono ligeramente más grande */
                height: 45px;
                margin-right: 20px;
                color: #5DADE2; /* Un azul más brillante que contrasta con el fondo */
                flex-shrink: 0; /* Evita que el ícono se encoja si el texto es largo */
            }
            .header-title {
                font-size: 2.3rem; /* Tamaño agrandado para "Planilla de trabajo de" */
                font-weight: 700;
                color: #EAECEE; /* Un blanco suave para mejor lectura */
                padding: 0;
                margin: 0;
                line-height: 1; /* Ajusta la altura de línea */
            }
            .efe-style {
                font-size: 3.5rem; /* 'efe' mucho más grande */
                font-style: italic; /* Estilo bastardilla (cursiva) */
                font-weight: 800; /* Más grueso */
                margin-left: 10px; /* Pequeño espacio para separar */
                line-height: 1;
            }
        </style>
    """, unsafe_allow_html=True)

    # 2. HTML actualizado para usar las nuevas clases de CSS
    #    - El texto "efe" ahora está envuelto en un span con la clase 'efe-style'.
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
                    <span class="efe-style">
                        <span style="color: white;">e</span><span style="color: orange;">f</span><span style="color: white;">e</span>
                    </span>
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 3. El menú de navegación se mantiene igual
    selected_view = option_menu(
        menu_title=None,
        options=["Inicio", "Análisis", "Reportes"],
        icons=['house-door-fill', 'bar-chart-line-fill', 'file-earmark-text-fill'],
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
    
    # La línea divisoria ya no es tan necesaria gracias al fondo del header, pero se puede mantener si se desea.
    # st.markdown("---") # Puedes descomentar esto si quieres la línea de vuelta
    
    return selected_view
