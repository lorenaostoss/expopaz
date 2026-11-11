import streamlit as st

from utils import estilo, graficas
from utils.datos import aliados_unicos, mas_frecuente
from utils.estilo import AMBAR, LILA, NARANJA, NAVY, VERDE
from utils.plantilla_filtrada import preparar


def chips(p, a, f):
    u = aliados_unicos(a)
    return [(u["municipio"].nunique(), "municipios"), (u["departamento"].nunique(), "departamentos"),
            (mas_frecuente(u["municipio"]), "municipio con más aliados")]


p, a, f = preparar(chips, "Lugares",
                   "Dónde están los aliados y dónde se han desarrollado los proyectos, por municipio y departamento.")
u = aliados_unicos(a)

c1, c2 = st.columns([2, 1])
with c1, estilo.tarjeta("Aliados por municipio", f"Los {u['municipio'].nunique()} municipios donde Expopaz tiene aliados."):
    m = u["municipio"].value_counts().rename("n").rename_axis("municipio").reset_index()
    graficas.barras_horizontales(m, "municipio", "n", NAVY)
with c2, estilo.tarjeta("Aliados por departamento", f"{len(u)} aliados distintos."):
    d = u["departamento"].value_counts().rename("n").rename_axis("departamento").reset_index()
    graficas.dona(d, "departamento", "n", None, centro=str(len(u)), alto=380)

c3, c4 = st.columns(2)
with c3, estilo.tarjeta("Proyectos por municipio", "Proyectos con al menos un aliado en el municipio."):
    t = a.groupby("municipio")["id_proyecto"].nunique().sort_values(ascending=False).rename("n").reset_index().head(8)
    graficas.barras_horizontales(t, "municipio", "n", VERDE)
with c4, estilo.tarjeta("Proyectos por departamento", "Proyectos con al menos un aliado en el departamento."):
    t = a.groupby("departamento")["id_proyecto"].nunique().sort_values(ascending=False).rename("n").reset_index()
    graficas.barras_horizontales(t, "departamento", "n", LILA)
