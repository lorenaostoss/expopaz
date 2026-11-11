import pandas as pd
import streamlit as st

from utils import estilo, graficas
from utils.datos import SIN_PRODUCTO, mas_frecuente
from utils.estilo import AMBAR, VERDE
from utils.plantilla_filtrada import preparar


def chips(p, a, f):
    con = p[p["tipo_producto"] != SIN_PRODUCTO]
    return [(mas_frecuente(con["tipo_producto"]), "producto más frecuente"), (con["tipo_producto"].nunique(), "tipos de producto"),
            (int(p["tiene_link"].sum()), "proyectos con enlace")]


p, a, f = preparar(chips, "Productos",
                   "Qué han creado los proyectos para devolverle a las comunidades lo aprendido: cartillas, juegos, libros, páginas web y más, con el enlace para verlos.")

c1, c2 = st.columns([2, 1])
with c1, estilo.tarjeta("Proyectos por tipo de producto", "Los 12 productos más frecuentes."):
    t = p[p["tipo_producto"] != SIN_PRODUCTO]["tipo_producto"].value_counts().head(12).rename("n").rename_axis("tipo").reset_index()
    graficas.barras_horizontales(t, "tipo", "n", VERDE)
with c2, estilo.tarjeta("Proyectos con enlace al producto", "Cuántos proyectos tienen enlace disponible."):
    con = int(p["tiene_link"].sum())
    d = pd.DataFrame({"estado": ["Con enlace", "Sin enlace"], "n": [con, len(p) - con]})
    d = d[d["n"] > 0]
    graficas.dona(d, "estado", "n", {"Con enlace": VERDE, "Sin enlace": AMBAR}, centro=str(len(p)), alto=380)

with estilo.tarjeta("Productos de los proyectos", f"Descripción y enlace de cada producto ({len(p)} proyectos)."):
    estilo.lista_proyectos(p, a)
