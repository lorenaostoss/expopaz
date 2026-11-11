"""Gráficas de Plotly con la paleta de Expopaz."""
import textwrap

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.estilo import AMBAR, LILA, NARANJA, NAVY, TIPO_COLOR, VERDE

CONFIG = {"displayModeBar": False}
FUENTE = dict(family="Inter, sans-serif", color=NAVY, size=14)


def _base(fig, alto):
    fig.update_layout(height=alto, margin=dict(l=0, r=10, t=10, b=0), font=FUENTE,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
    fig.update_xaxes(tickfont=dict(size=14, color=NAVY))
    fig.update_yaxes(tickfont=dict(size=14, color=NAVY))
    return fig


def _mostrar(fig):
    st.plotly_chart(fig, width="stretch", config=CONFIG)


def vacio(texto="No hay datos con los filtros elegidos."):
    st.caption(texto)


def barras_verticales(df, x, y, color, alto=380):
    if df.empty:
        return vacio()
    fig = go.Figure(go.Bar(x=df[x], y=df[y], marker_color=color, text=df[y], textposition="outside",
                           cliponaxis=False, hovertemplate="%{x}: %{y}<extra></extra>"))
    fig.update_yaxes(visible=False, range=[0, max(df[y].max() * 1.18, 1)])
    _base(fig, alto)
    fig.update_xaxes(type="category", showgrid=False, linecolor="#E3E5F1", tickangle=0, tickfont=dict(size=12, color=NAVY))
    _mostrar(fig)


def _etiqueta(texto, ancho=17):
    lineas = textwrap.wrap(str(texto), ancho) or [""]
    return "<br>".join(lineas), len(lineas)


def barras_horizontales(df, cat, val, color, alto=None, colores=None):
    """`colores`: lista de colores por barra (opcional). Las etiquetas largas se parten en varias líneas."""
    if df.empty:
        return vacio()
    d = df.iloc[::-1]
    cols = (colores[::-1] if colores else color)
    etiquetas = [_etiqueta(t) for t in d[cat]]
    fig = go.Figure(go.Bar(x=d[val], y=[e[0] for e in etiquetas], orientation="h", marker_color=cols, text=d[val],
                           textposition="outside", cliponaxis=False, customdata=d[cat],
                           hovertemplate="%{customdata}: %{x}<extra></extra>"))
    fig.update_yaxes(showgrid=False, linecolor="#E3E5F1", automargin=True)
    fig.update_xaxes(visible=False, range=[0, max(d[val].max() * 1.15, 1)])
    fig.update_layout(bargap=0.35)
    filas = sum(40 + 16 * (n - 1) for _, n in etiquetas)
    _mostrar(_base(fig, alto or max(150, filas + 20)))


def dona(df, nombres, valores, mapa_colores=None, centro="", alto=380):
    """Dona con la leyenda debajo (así se ve bien aunque la tarjeta sea angosta)."""
    if df.empty:
        return vacio()
    paleta = [NAVY, NARANJA, AMBAR, LILA, VERDE]
    cols = [(mapa_colores or {}).get(n, paleta[i % 5]) for i, n in enumerate(df[nombres])]
    fig = go.Figure(go.Pie(labels=df[nombres], values=df[valores], hole=.6, sort=False, marker=dict(colors=cols),
                           textinfo="value", textfont=dict(size=14, color="#fff"), direction="clockwise",
                           domain=dict(x=[.05, .95], y=[.30, 1]), hovertemplate="%{label}: %{value}<extra></extra>"))
    fig.add_annotation(text=f"<b>{centro}</b>", x=.5, y=.65, showarrow=False, font=dict(size=32, color=NAVY),
                       xref="paper", yref="paper")
    _base(fig, alto)
    fig.update_layout(showlegend=True, margin=dict(l=0, r=0, t=10, b=0),
                      legend=dict(orientation="h", yanchor="top", y=.26, xanchor="center", x=.5, font=dict(size=13)))
    _mostrar(fig)


def apiladas_por_semestre(df, alto=360):
    """df con columnas semestre, tipo_aliado, n."""
    if df.empty:
        return vacio()
    fig = go.Figure()
    tabla = df.pivot_table(index="semestre", columns="tipo_aliado", values="n", aggfunc="sum", fill_value=0)
    for tipo, color in TIPO_COLOR.items():
        if tipo in tabla.columns:
            fig.add_bar(x=tabla.index, y=tabla[tipo], name=tipo, marker_color=color,
                        hovertemplate="%{x} · " + tipo + ": %{y}<extra></extra>")
    fig.update_layout(barmode="stack", showlegend=True, legend=dict(orientation="h", y=-.15, font=dict(size=13)))
    fig.update_xaxes(type="category", showgrid=False, linecolor="#E3E5F1")
    fig.update_yaxes(gridcolor="#EEF0F7")
    _base(fig, alto)
    fig.update_layout(showlegend=True, margin=dict(l=0, r=10, t=10, b=10))
    _mostrar(fig)


def por_semestre(p, columna, funcion="sum"):
    """Serie por semestre lista para `barras_verticales`."""
    g = p.groupby("semestre")[columna]
    s = g.size() if funcion == "size" else g.sum()
    return s.rename("valor").reset_index()
