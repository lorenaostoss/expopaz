"""Barra lateral: logo, menú y filtros desplegables."""
from pathlib import Path

import streamlit as st

from utils.datos import SIN_PRODUCTO

LOGO = Path(__file__).resolve().parent.parent / "assets" / "logo.png"

PAGINAS = [
    ("views/panorama.py", "Panorama general"),
    ("views/periodo.py", "Por periodo"),
    ("views/aliados.py", "Aliados"),
    ("views/productos.py", "Productos"),
    ("views/lugares.py", "Lugares"),
]
CLAVES = ["f_anio", "f_semestre", "f_productos", "f_tipos", "f_deptos", "f_munis"]


def _mantener_estado():
    """Streamlit olvida los widgets que no se dibujan; esto conserva los filtros al cambiar de pestaña."""
    for k in CLAVES:
        if k in st.session_state:
            st.session_state[k] = st.session_state[k]


def _validar(clave, opciones, multiple):
    if clave not in st.session_state:
        return
    if multiple:
        st.session_state[clave] = [v for v in st.session_state[clave] if v in opciones]
    elif st.session_state[clave] not in opciones:
        st.session_state[clave] = "Todos"


def menu_lateral():
    if LOGO.exists():
        st.sidebar.image(str(LOGO), width="stretch")
    activo = next((i for i, (_, e) in enumerate(PAGINAS) if e == st.session_state.get("_activo")), 0)
    # Resalta en naranja la pestaña actual.
    st.markdown(
        f"<style>.st-key-menu .stElementContainer:nth-child({activo + 1}) [data-testid='stPageLink-NavLink'] "
        f"{{ background: #FE623C !important; }} .st-key-menu .stElementContainer:nth-child({activo + 1}) p "
        f"{{ font-weight: 700; }}</style>", unsafe_allow_html=True)
    with st.sidebar.container(key="menu"):
        for ruta, etiqueta in PAGINAS:
            st.page_link(ruta, label=etiqueta)


def barra_filtros(p, a):
    """Dibuja los filtros y devuelve el diccionario con la selección actual."""
    _mantener_estado()
    st.sidebar.markdown("<div class='filtros-titulo'>Filtros</div>", unsafe_allow_html=True)

    anios = ["Todos"] + [str(x) for x in sorted(p["anio"].unique())]
    _validar("f_anio", anios, False)
    anio = st.sidebar.selectbox("Año", anios, key="f_anio")

    sems = sorted(p["semestre"].unique())
    if anio != "Todos":
        sems = [s for s in sems if s.startswith(anio)]
    sems = ["Todos"] + sems
    _validar("f_semestre", sems, False)
    semestre = st.sidebar.selectbox("Semestre", sems, key="f_semestre")

    productos_op = list(p["tipo_producto"].value_counts().index)
    _validar("f_productos", productos_op, True)
    productos = st.sidebar.multiselect("Tipo de producto", productos_op, key="f_productos", placeholder="Todos")

    tipos_op = list(a.drop_duplicates("clave")["tipo_aliado"].value_counts().index)
    _validar("f_tipos", tipos_op, True)
    tipos = st.sidebar.multiselect("Tipo de aliado", tipos_op, key="f_tipos", placeholder="Todos")

    deptos_op = sorted(a["departamento"].unique())
    _validar("f_deptos", deptos_op, True)
    deptos = st.sidebar.multiselect("Departamento", deptos_op, key="f_deptos", placeholder="Todos")

    base = a[a["departamento"].isin(deptos)] if deptos else a
    munis_op = sorted(base["municipio"].unique())
    _validar("f_munis", munis_op, True)
    munis = st.sidebar.multiselect("Municipio", munis_op, key="f_munis", placeholder="Todos")

    if st.sidebar.button("Limpiar filtros", width="stretch"):
        for k in CLAVES:
            st.session_state.pop(k, None)
        st.rerun()

    return {"anio": anio, "semestre": semestre, "productos": productos,
            "tipos_aliado": tipos, "departamentos": deptos, "municipios": munis}
