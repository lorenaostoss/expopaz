"""Dashboard de Expopaz. Ejecutar con:  streamlit run app.py"""
import streamlit as st

st.set_page_config(page_title="Expopaz", page_icon="assets/logo.png", layout="wide")

paginas = [
    st.Page("views/panorama.py", title="Panorama general", default=True),
    st.Page("views/periodo.py", title="Por periodo", url_path="periodo"),
    st.Page("views/aliados.py", title="Aliados", url_path="aliados"),
    st.Page("views/productos.py", title="Productos", url_path="productos"),
    st.Page("views/lugares.py", title="Lugares", url_path="lugares"),
]
# El menú lo dibujamos nosotros en la barra lateral (así el logo queda arriba, encima de los filtros).
actual = st.navigation(paginas, position="hidden")
st.session_state["_activo"] = actual.title
actual.run()
