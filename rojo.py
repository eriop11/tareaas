import streamlit as st

def fondo_rojo():
    """
    Cambia el fondo de toda la página de Streamlit a rojo.
    """
    st.markdown(
        """
        <style>
        body {
            background-color: red;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
