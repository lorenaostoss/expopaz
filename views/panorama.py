import streamlit as st

from utils import estilo, graficas
from utils.datos import SIN_PRODUCTO, aliados_unicos, cargar
from utils.estilo import AMBAR, LILA, NARANJA, NAVY, TIPO_COLOR, VERDE
from utils.filtros import menu_lateral

estilo.aplicar_estilo()
menu_lateral()
p, a = cargar()

u = aliados_unicos(a)
estilo.encabezado([(len(p), "proyectos"), (p["semestre"].nunique(), f"semestres · {p['semestre'].min()} a {p['semestre'].max()}"),
                   (len(u), "aliados distintos")])
estilo.titulo_pagina("Panorama general",
                     "Una mirada a todo Expopaz: cuántos proyectos, estudiantes, aliados y personas impactadas ha reunido la feria "
                     f"desde {p['semestre'].min()} hasta {p['semestre'].max()}.")
st.markdown(f'<div class="info"><h3>¿Qué es Expopaz?</h3><p>{estilo.QUE_ES}</p></div>', unsafe_allow_html=True)
estilo.tarjetas_generales(p, a)
estilo.tarjetas_destacadas(p, a)

c1, c2 = st.columns([2, 1])
with c1, estilo.tarjeta("Proyectos por semestre", "Cuántos proyectos se presentaron en cada semestre."):
    graficas.barras_verticales(graficas.por_semestre(p, "id_proyecto", "size"), "semestre", "valor", NARANJA)
with c2, estilo.tarjeta("Aliados por tipo", f"{len(u)} aliados distintos, según su rol."):
    t = u["tipo_aliado"].value_counts().reindex(list(TIPO_COLOR)).dropna().astype(int).rename("n").reset_index()
    graficas.dona(t, "tipo_aliado", "n", TIPO_COLOR, centro=str(len(u)))

c3, c4 = st.columns(2)
with c3, estilo.tarjeta("Estudiantes por semestre", "Inscripciones de estudiantes en cada semestre."):
    graficas.barras_verticales(graficas.por_semestre(p, "estudiantes"), "semestre", "valor", AMBAR)
with c4, estilo.tarjeta("Personas impactadas por semestre", "Personas que participaron en los proyectos de cada semestre."):
    graficas.barras_verticales(graficas.por_semestre(p, "personas_impactadas"), "semestre", "valor", LILA)

c5, c6 = st.columns(2)
with c5, estilo.tarjeta("Proyectos por tipo de producto", "Los 7 productos más frecuentes."):
    t = p[p["tipo_producto"] != SIN_PRODUCTO]["tipo_producto"].value_counts().head(7).rename("n").rename_axis("tipo").reset_index()
    graficas.barras_horizontales(t, "tipo", "n", VERDE)
with c6, estilo.tarjeta("Aliados por municipio", "Dónde están los aliados."):
    m = u["municipio"].value_counts().rename("n").rename_axis("municipio").reset_index()
    if len(m) > 5:
        m = m.head(4).copy()
        otros = len(u) - m["n"].sum()
        import pandas as pd
        m = pd.concat([m, pd.DataFrame([{"municipio": f"Otros {u['municipio'].nunique() - 4} municipios", "n": otros}])])
    graficas.barras_horizontales(m, "municipio", "n", NAVY)
