import streamlit as st
from rojo import fondo_rojo 
fondo_rojo()
valor = st.slider("Selecciona cuánto me amas del 1 al 100", 0, 100, 0)

# Mensajes según el valor
if valor == 0:
    st.write("Me mato😢")
elif valor <= 20:
    st.write("Echo es muy poquito😅")
elif valor <= 40:
    st.write("Dale culo no seas malo 😏")
elif valor <= 60:
    st.write("Me pareche medio mal pero eshta bien💛")
elif valor <= 80:
    st.write("AAA un poquito mashhh💖")
elif valor < 100:
    st.write("chi chi tu puedesh mass😍")
else:  # valor == 100
    st.write("¡Yo tambien preciosa! 🥰💯")
    fondo_rojo()


