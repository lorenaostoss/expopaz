"""Carga y preparación de la base de datos de Expopaz (Excel)."""
from pathlib import Path
import re

import pandas as pd
import streamlit as st

RUTA_EXCEL = Path(__file__).resolve().parent.parent / "data" / "expopaz_base_final.xlsx"
SIN_PRODUCTO = "Sin tipo de producto"


def _clave(nombre: str) -> str:
    """Nombre normalizado para contar aliados únicos."""
    return re.sub(r"\s+", " ", str(nombre)).strip().lower()


@st.cache_data
def cargar():
    """Devuelve (proyectos, aliados) listos para usar."""
    p = pd.read_excel(RUTA_EXCEL, sheet_name="Proyectos")
    a = pd.read_excel(RUTA_EXCEL, sheet_name="Aliados")

    for col in p.select_dtypes(include=["object", "string"]).columns:
        p[col] = p[col].astype("string").str.strip()
    for col in a.select_dtypes(include=["object", "string"]).columns:
        a[col] = a[col].astype("string").str.strip()

    p["anio"] = p["anio"].astype(int)
    p["semestre"] = p["semestre"].astype(str)
    p["estudiantes"] = pd.to_numeric(p["estudiantes"], errors="coerce").fillna(0).astype(int)
    p["personas_impactadas"] = pd.to_numeric(p["personas_impactadas"], errors="coerce").fillna(0).astype(int)
    p["tipo_producto"] = p["tipo_producto"].fillna(SIN_PRODUCTO).astype(str)

    link = p["link"].fillna("").astype(str)
    p["tiene_link"] = link.str.lower().str.startswith("http")
    p["link"] = link.where(p["tiene_link"], "")

    a = a.dropna(subset=["aliado"]).copy()
    a["clave"] = a["aliado"].map(_clave)
    for col in ("tipo_aliado", "municipio", "departamento"):
        a[col] = a[col].fillna("Sin dato").astype(str)
    a = a.merge(p[["id_proyecto", "anio", "semestre"]], on="id_proyecto", how="inner")
    return p, a


def aplicar_filtros(p, a, f):
    """Aplica los filtros (diccionario `f`) y devuelve (proyectos, aliados) filtrados.

    - Año, semestre y tipo de producto filtran proyectos.
    - Tipo de aliado, departamento y municipio filtran aliados; los proyectos que
      quedan son los que tienen al menos un aliado que cumple, y solo se cuentan
      esos aliados.
    """
    pf = p
    if f["anio"] != "Todos":
        pf = pf[pf["anio"] == int(f["anio"])]
    if f["semestre"] != "Todos":
        pf = pf[pf["semestre"] == f["semestre"]]
    if f["productos"]:
        pf = pf[pf["tipo_producto"].isin(f["productos"])]

    af = a[a["id_proyecto"].isin(pf["id_proyecto"])]
    hay_filtro_aliado = bool(f["tipos_aliado"] or f["departamentos"] or f["municipios"])
    if f["tipos_aliado"]:
        af = af[af["tipo_aliado"].isin(f["tipos_aliado"])]
    if f["departamentos"]:
        af = af[af["departamento"].isin(f["departamentos"])]
    if f["municipios"]:
        af = af[af["municipio"].isin(f["municipios"])]
    if hay_filtro_aliado:
        pf = pf[pf["id_proyecto"].isin(af["id_proyecto"])]
    return pf, af


def aliados_unicos(a):
    return a.drop_duplicates("clave")


def mas_frecuente(serie):
    """Valor más frecuente de una serie (o '—' si está vacía)."""
    s = serie.dropna()
    return s.value_counts().idxmax() if len(s) else "—"
