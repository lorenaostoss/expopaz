import pandas as pd

from utils import estilo, graficas
from utils.datos import SIN_PRODUCTO, aliados_unicos
from utils.estilo import NARANJA, NAVY, TIPO_COLOR, VERDE
from utils.plantilla_filtrada import periodo_texto, preparar
import streamlit as st

p, a, f = preparar(
    lambda p, a, f: [(periodo_texto(f), "periodo mostrado"), (len(p), "proyectos"), (f"{p['personas_impactadas'].sum():,}".replace(",", "."), "personas impactadas")],
    "Por periodo",
    "Elige un año o semestre y combínalo con los filtros para ver sus proyectos, aliados y productos, con la descripción y el enlace de cada uno.")

u = aliados_unicos(a)
c1, c2, c3 = st.columns(3)
with c1, estilo.tarjeta("Aliados por tipo", f"{len(u)} aliados en este periodo."):
    t = u["tipo_aliado"].value_counts().rename("n").rename_axis("tipo").reset_index()
    graficas.barras_horizontales(t, "tipo", "n", NAVY, colores=[TIPO_COLOR.get(x, NAVY) for x in t["tipo"]])
with c2, estilo.tarjeta("Proyectos por tipo de producto", "Qué se produjo en este periodo."):
    t = p["tipo_producto"].value_counts().rename("n").rename_axis("tipo").reset_index().head(8)
    graficas.barras_horizontales(t, "tipo", "n", VERDE)
with c3, estilo.tarjeta("Proyectos por municipio", "Dónde se realizaron (según sus aliados)."):
    t = a.groupby("municipio")["id_proyecto"].nunique().sort_values(ascending=False).rename("n").reset_index().head(8)
    graficas.barras_horizontales(t, "municipio", "n", NAVY)

with estilo.tarjeta("Proyectos del periodo", f"Descripción y enlace de cada proyecto ({len(p)} en total)."):
    estilo.lista_proyectos(p, a)
