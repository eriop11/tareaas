import streamlit as st

st.title("Mi primera app con Streamlit")
st.write("Hola Erich 👋, esta es una interfaz web hecha con Python.")

valor = st.slider("Seleccioná un número", 0, 100, 50)
st.write("El valor elegido es:", valor)
