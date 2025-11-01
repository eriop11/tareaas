import streamlit as st
from titulos import mostrar_titulo_principal #genera el titulo
st.set_page_config(
    page_title="Dashboard Principal",
    page_icon="🚀",
    layout="wide"
)

def main():
     mostrar_titulo_principal()

if __name__ == "__main__":
    main()
