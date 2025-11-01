# titulos.py
import streamlit as st

def mostrar_titulo_principal():
    """
    Muestra el título principal de la aplicación con colores personalizados
    utilizando HTML y CSS dentro de st.markdown.
    """
    # Usamos HTML para poder dar estilo a letras individuales.
    # El tag <h1> le da el tamaño de un título principal.
    # El tag <span> nos permite aplicar estilos (como el color) a segmentos de texto.
    titulo_html = """
    <style>
        .titulo-principal {
            font-size: 2.5rem; /* Tamaño del título */
            font-weight: bold; /* Negrita */
        }
    </style>
    
    <p class="titulo-principal">
        Planilla de trabajo de 
        <span style="color: white;">e</span><span style="color: orange;">f</span><span style="color: white;">e</span>
    </p>
    """
    
    # unsafe_allow_html=True es necesario para que Streamlit renderice el HTML.
    st.markdown(titulo_html, unsafe_allow_html=True)
