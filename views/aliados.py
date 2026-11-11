import streamlit as st

from utils import estilo, graficas
from utils.datos import aliados_unicos, mas_frecuente
from utils.estilo import AMBAR, NAVY, TIPO_COLOR
from utils.plantilla_filtrada import preparar


def chips(p, a, f):
    u = aliados_unicos(a)
    tipo = mas_frecuente(u["tipo_aliado"])
    return [(len(u), "aliados distintos"), (int((u["tipo_aliado"] == tipo).sum()) if len(u) else 0, f"{tipo}" if len(u) else "—"),
            (tipo, "tipo más frecuente")]


p, a, f = preparar(chips, "Aliados",
                   "Quiénes han trabajado con los estudiantes: instituciones, comunidades, organizaciones, empresas y entidades públicas, y en cuántos proyectos participó cada uno.")
u = aliados_unicos(a)

c1, c2 = st.columns([2, 1])
with c1, estilo.tarjeta("Aliados por tipo y semestre", "Cuántos aliados distintos participaron en cada semestre, según su rol."):
    d = a.drop_duplicates(["clave", "semestre"]).groupby(["semestre", "tipo_aliado"]).size().rename("n").reset_index()
    graficas.apiladas_por_semestre(d)
with c2, estilo.tarjeta("Aliados por tipo", f"{len(u)} aliados distintos en total."):
    t = u["tipo_aliado"].value_counts().reindex(list(TIPO_COLOR)).dropna().astype(int).rename("n").reset_index()
    graficas.dona(t, "tipo_aliado", "n", TIPO_COLOR, centro=str(len(u)), alto=380)

c3, c4 = st.columns(2)
with c3, estilo.tarjeta("Aliados con más proyectos", "Número de proyectos en los que ha participado cada aliado."):
    g = a.groupby("clave").agg(aliado=("aliado", "first"), n=("id_proyecto", "nunique")).sort_values("n", ascending=False).head(8)
    graficas.barras_horizontales(g.reset_index(drop=True), "aliado", "n", AMBAR)
with c4, estilo.tarjeta("Aliados por municipio", "Dónde están los aliados."):
    m = u["municipio"].value_counts().rename("n").rename_axis("municipio").reset_index().head(8)
    graficas.barras_horizontales(m, "municipio", "n", NAVY)
