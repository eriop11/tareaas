# titulos.py (Versión con logo en el header)

import streamlit as st
from streamlit_option_menu import option_menu
import base64 # Importamos la librería para codificar la imagen

def render_header():
    """
    Renderiza el header completo con un logo en lugar del texto "efe".
    """
    
    # --- FUNCIÓN PARA CARGAR Y CODIFICAR LA IMAGEN LOCAL ---
    # Esto es necesario para que la imagen se muestre en el HTML personalizado.
    def get_image_as_base64(path):
        try:
            with open(path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
        except FileNotFoundError:
            # Devuelve un placeholder si no encuentra la imagen para evitar errores
            return None

    # Codificamos nuestro logo.png a Base64
    logo_base64 = get_image_as_base64("fotos/logo.png")

    # 1. CSS Modificado para el logo
    st.markdown(f"""
        <style>
            .header-container {{
                display: flex;
                align-items: center; /* Centrar verticalmente es mejor para imagen y texto */
                background-color: #262730;
                padding: 15px 25px; /* Ajustamos un poco el padding vertical */
                border-radius: 10px;
                margin-bottom: 1.5rem;
            }}
            .header-icon svg {{
                width: 45px;
                height: 45px;
                margin-right: 20px;
                color: #5DADE2;
                flex-shrink: 0;
            }}
            .header-title {{
                font-size: 2.3rem;
                font-weight: 700;
                color: #EAECEE;
                padding: 0;
                margin: 0;
                line-height: 1;
            }}
            /* Nueva clase para la imagen del logo */
            .header-logo-img {{
                height: 50px; /* Define la altura del logo, el ancho será automático */
                margin-left: 15px; /* Espacio entre "de" y el logo */
                vertical-align: middle; /* Ayuda a alinear mejor con el texto */
            }}
        </style>
    """, unsafe_allow_html=True)

    # 2. HTML Modificado para usar la etiqueta <img>
    #    - Se reemplaza el <span> de "efe" por una etiqueta <img>.
    #    - La fuente de la imagen (src) usa el formato de datos Base64 que preparamos.
    if logo_base64:
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
                        <img src="data:image/png;base64,{logo_base64}" class="header-logo-img">
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Mensaje de error si el logo no se encuentra, para facilitar la depuración
        st.error("No se encontró el archivo del logo en 'fotos/logo.png'.")


    # 3. El menú de navegación se mantiene igual
    selected_view = option_menu(
        menu_title=None,
        options=["Inicio", "Análisis", "Reportes", "Usuarios"],
        icons=['house-door-fill', 'bar-chart-line-fill', 'file-earmark-text-fill', 'people-fill'],
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
    
    return selected_view```

### **Explicación de los Cambios Clave:**

1.  **Codificación a Base64:** No podemos simplemente poner una ruta de archivo local (`fotos/logo.png`) en el código HTML. El navegador no sabría cómo encontrarla. Para solucionar esto, leemos el archivo de imagen, lo convertimos en una larga cadena de texto (formato Base64) y la incrustamos directamente en el HTML. La función `get_image_as_base64` se encarga de esto.
2.  **Nuevo CSS (`.header-logo-img`):** Creamos un estilo específico para la imagen del logo, definiendo su altura y espaciado. Puedes ajustar el valor `height: 50px;` para hacer tu logo más grande o más pequeño.
3.  **Nuevo HTML (`<img>`):** Reemplazamos el `<span>` que contenía "efe" por una etiqueta `<img src="...">`. La parte `src="data:image/png;base64,{logo_base64}"` es la forma estándar de decirle al navegador "la fuente de esta imagen son estos datos Base64".

### **Qué hacer ahora:**

1.  Reemplaza todo el contenido de tu archivo `titulos.py` con el código de arriba.
2.  Asegúrate de que tu logo esté en `fotos/logo.png`.
3.  Sube los cambios a GitHub:
    ```bash
    git add .
    git commit -m "Reemplaza texto 'efe' en header por imagen del logo"
    git push
    ```

Tu aplicación ahora mostrará tu logo directamente en el header, ¡dándole un aspecto mucho más profesional y personalizado
