# titulos.py

import streamlit as st
from streamlit_option_menu import option_menu

def render_header():
    """
    Renderiza el header completo: Título con ícono y colores, y la barra de navegación.
    
    Devuelve:
        str: El nombre de la vista seleccionada en el menú de navegación 
             ("Inicio", "Análisis", o "Reportes").
    """
    
    # Inyectamos CSS para el estilo del título y el ícono
    st.markdown("""
        <style>
            .header-container {
                display: flex;
                align-items: center;
                margin-bottom: 1rem;
            }
            .header-icon svg {
                width: 40px;
                height: 40px;
                margin-right: 15px;
                color: #2F80ED; /* Azul */
            }
            .header-title {
                font-size: 2.5rem;
                font-weight: bold;
                padding: 0;
                margin: 0;
            }
        </style>
    """, unsafe_allow_html=True)

    # Renderizamos el HTML del título con el ícono y los colores personalizados
    st.markdown(f"""
        <div class="header-container">
            <div class="header-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
            </div>
            <p class="header-title">
                Planilla de trabajo de 
                <span style="color: white;">e</span><span style="color: orange;">f</span><span style="color: white;">e</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Creamos el menú de navegación y guardamos la opción seleccionada
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
    
    # Línea divisoria para separar el header del contenido
    st.markdown("---")
    
    # Devolvemos la opción que el usuario seleccionó para que el main sepa qué mostrar
    return selected_view
