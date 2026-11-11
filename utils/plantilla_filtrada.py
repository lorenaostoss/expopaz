"""Pasos comunes de las pestañas con filtros."""
import streamlit as st

from utils import estilo
from utils.datos import aplicar_filtros, cargar
from utils.filtros import barra_filtros, menu_lateral


def preparar(chips_fn, titulo, descripcion):
    """Dibuja barra lateral, encabezado y tarjetas. Devuelve (p, a, filtros) o detiene la página si no hay datos."""
    estilo.aplicar_estilo()
    menu_lateral()
    p_all, a_all = cargar()
    f = barra_filtros(p_all, a_all)
    p, a = aplicar_filtros(p_all, a_all, f)
    estilo.encabezado(chips_fn(p, a, f))
    estilo.titulo_pagina(titulo, descripcion)
    if p.empty:
        st.info("No hay proyectos con esta combinación de filtros. Prueba quitando alguno desde la barra lateral.")
        st.stop()
    estilo.tarjetas_generales(p, a)
    estilo.tarjetas_destacadas(p, a)
    return p, a, f


def periodo_texto(f):
    if f["semestre"] != "Todos":
        return f["semestre"]
    if f["anio"] != "Todos":
        return f"Año {f['anio']}"
    return "Todos"
