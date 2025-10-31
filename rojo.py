import streamlit as st
st.write("Me matooooooooooooo😢")
def fondo_rojo():
    st.write("Me matooooooooooooo😢")
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
