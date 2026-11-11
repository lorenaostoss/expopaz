"""Colores, CSS y componentes visuales (barra de título, tarjetas, proyectos)."""
from contextlib import contextmanager
from html import escape

import streamlit as st

NAVY, NARANJA, AMBAR, LILA, VERDE = "#11173B", "#FE623C", "#F8B327", "#C28DF7", "#09403B"
TIPO_COLOR = {
    "Institución educativa": NAVY,
    "Comunidad o población": NARANJA,
    "Organización social": AMBAR,
    "Empresa o negocio privado": LILA,
    "Entidad pública": VERDE,
}

TITULO = "Expopaz: Proyectos de investigación cualitativa con impacto social desde el aula"
SUBTITULO = "Facultad de Ciencias del Comportamiento: Departamento de Estudios Sociales, Políticos y Culturales"
AUTORAS = ["Lorena Ostos", "Catalina Troncoso"]
PROFESORES = ["Pilar Baracaldo", "Laura Fonseca", "Mónica González", "Carlos Monroy", "Camilo Rincón"]

QUE_ES = ("EXPOPAZ es una feria académica que reúne los proyectos desarrollados por estudiantes de "
          "Investigación Cualitativa y Psicología Social. La feria celebra el trabajo y los aprendizajes "
          "del semestre y permite a los estudiantes compartir cómo, a través de la investigación y el "
          "diálogo con distintas comunidades, fortalecen sus habilidades investigativas, desarrollan "
          "sensibilidad social y reflexionan sobre la justicia social y la construcción de paz.")

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp {{ font-family: 'Inter', sans-serif; }}
#MainMenu, footer {{ visibility: hidden; }}
[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ padding-top: 1.2rem; padding-bottom: 3rem; max-width: 1500px; }}
[data-testid="stSidebar"] {{ background: #FFFFFF; box-shadow: 2px 0 16px rgba(17,23,59,.06); }}
[data-testid="stSidebar"] > div:first-child {{ padding-top: 1rem; }}
[data-testid="stSidebarNav"] {{ display: none; }}
.filtros-titulo {{ font-size: 1.15rem; font-weight: 800; color: {NAVY}; margin: 1.2rem 0 .2rem; border-top: 1px solid #E3E5F1; padding-top: 1rem; }}
[class*="st-key-card_"] {{ background: #FFFFFF; border-radius: 22px; box-shadow: 0 2px 16px rgba(17,23,59,.07); padding: 1.3rem 1.5rem 1rem; }}
.st-key-menu [data-testid="stPageLink-NavLink"] {{ border-radius: 12px; padding: .55rem .8rem; }}
.st-key-menu [data-testid="stPageLink-NavLink"]:hover {{ background: #EEF0F7; }}
.ct {{ margin: 0 0 .15rem; font-size: 1.25rem; font-weight: 700; color: {NAVY}; }}
.cs {{ margin: 0 0 .6rem; font-size: .9rem; color: #5B6180; }}
.hero {{ position: relative; overflow: hidden; background: {NAVY}; color: #fff; border-radius: 24px; padding: 2.4rem 2.6rem 2.7rem; margin-bottom: 1.4rem; }}
.hero .c1 {{ position:absolute; right:-70px; top:-110px; width:320px; height:320px; border-radius:50%; background:{LILA}; opacity:.22; }}
.hero .c2 {{ position:absolute; right:230px; bottom:-130px; width:230px; height:230px; border-radius:50%; background:{NARANJA}; opacity:.20; }}
.hero .c3 {{ position:absolute; left:52%; top:-60px; width:130px; height:130px; border-radius:50%; background:{AMBAR}; opacity:.18; }}
.hero-in {{ position: relative; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 1.6rem; }}
.eyebrow {{ font-size: 1rem; font-weight: 700; letter-spacing: 6px; color: {AMBAR}; margin-bottom: .5rem; }}
.hero h1 {{ margin: 0; padding: 0; font-size: 2.2rem; font-weight: 800; letter-spacing: -.5px; line-height: 1.2; max-width: 820px; color: #fff; }}
.subt {{ margin: .6rem 0 0; font-size: 1.2rem; font-weight: 600; color: {AMBAR}; }}
.names {{ margin: 1rem 0 0; font-size: .98rem; color: #fff; }}
.names.autoras {{ margin-top: .35rem; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 14px; }}
.chip {{ background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.25); border-radius: 16px; padding: .8rem 1.3rem; min-width: 140px; }}
.chip b {{ display: block; font-size: 1.7rem; font-weight: 800; line-height: 1.15; }}
.chip span {{ font-size: .85rem; color: #D9DCF0; }}
.strip {{ position:absolute; left:0; right:0; bottom:0; height:8px; display:flex; }}
.strip div {{ flex:1; }}
h2.pagina {{ margin: 0; padding: 0; font-size: 2.1rem; font-weight: 800; color: {NAVY}; }}
p.desc {{ margin: .4rem 0 1.1rem; font-size: 1.08rem; color: #5B6180; max-width: 1000px; line-height: 1.5; }}
.grid4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 1rem; }}
.grid3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 1rem; }}
@media (max-width: 1500px) {{ .grid4 {{ grid-template-columns: repeat(2, 1fr); }} .kv.txt {{ font-size: 1.15rem; }} }}
@media (max-width: 1000px) {{ .grid3 {{ grid-template-columns: 1fr; }} }}
.kpi {{ background:#fff; border-radius:22px; padding:1.3rem 1.4rem; box-shadow:0 2px 16px rgba(17,23,59,.07); display:flex; align-items:center; gap:18px; }}
.kicon {{ width:58px; height:58px; border-radius:18px; display:grid; place-items:center; flex:none; }}
.kl {{ font-size:.95rem; color:#5B6180; }}
.kv {{ font-size:2.5rem; font-weight:800; line-height:1.1; color:{NAVY}; }}
.kv.txt {{ font-size:1.45rem; line-height:1.25; }}
.info {{ background:#fff; border-radius:22px; padding:1.4rem 1.7rem; box-shadow:0 2px 16px rgba(17,23,59,.07); border-left:8px solid {VERDE}; margin-bottom:1rem; }}
.info h3 {{ margin:0 0 .4rem; font-size:1.25rem; color:{NAVY}; }}
.info p {{ margin:0; font-size:1.05rem; line-height:1.65; color:{NAVY}; }}
.proy-grid {{ display:grid; grid-template-columns:repeat(3, 1fr); gap:16px; }}
@media (max-width: 1100px) {{ .proy-grid {{ grid-template-columns: 1fr; }} }}
.proy {{ border:1.5px solid #E3E5F1; border-radius:16px; padding:1.1rem 1.2rem; display:flex; flex-direction:column; gap:.6rem; background:#fff; }}
.proy .n {{ font-weight:700; font-size:1.05rem; line-height:1.35; color:{NAVY}; }}
.proy .t {{ font-size:.92rem; color:#5B6180; }}
.proy .a {{ font-size:.85rem; color:#5B6180; }}
.tag {{ display:inline-block; font-size:.82rem; font-weight:600; padding:4px 11px; border-radius:999px; margin:0 6px 6px 0; color:{NAVY}; background:#EEF0F7; }}
.btn {{ display:inline-block; font-size:.9rem; font-weight:700; padding:9px 16px; border-radius:12px; background:{NAVY}; color:#fff !important; text-decoration:none !important; align-self:flex-start; }}
.sinlink {{ font-size:.9rem; color:#5B6180; }}
</style>
"""

ICONOS = {
    "proyectos": '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "estudiantes": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5"/>',
    "personas": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14c2.2.6 3.5 2.4 3.5 6"/>',
    "lugares": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "aliados": '<path d="M8 12l3 3 5-6"/><circle cx="12" cy="12" r="9"/>',
    "producto": '<path d="M21 8l-9-5-9 5 9 5z"/><path d="M3 8v8l9 5 9-5V8"/>',
}


def fmt(n):
    return f"{int(n):,}".replace(",", ".")


def aplicar_estilo():
    st.session_state["_n_tarjeta"] = 0
    st.markdown(CSS, unsafe_allow_html=True)


def encabezado(chips):
    """Barra azul grande con el título, las autoras y tres cifras clave."""
    ch = "".join(f'<div class="chip"><b>{escape(str(a))}</b><span>{escape(str(b))}</span></div>' for a, b in chips)
    autoras = " &nbsp;·&nbsp; ".join(f"<b>{escape(n)}</b>" for n in AUTORAS)
    profesores = " &nbsp;·&nbsp; ".join(escape(n) for n in PROFESORES)
    franja = "".join(f'<div style="background:{c}"></div>' for c in (NARANJA, AMBAR, LILA, VERDE))
    st.markdown(
        f'<div class="hero"><div class="c1"></div><div class="c2"></div><div class="c3"></div>'
        f'<div class="hero-in"><div><h1>{escape(TITULO)}</h1>'
        f'<p class="subt">{escape(SUBTITULO)}</p>'
        f'<p class="names">Profesores a cargo: {profesores}</p>'
        f'<p class="names autoras">Autoras: {autoras}</p></div><div class="chips">{ch}</div></div>'
        f'<div class="strip">{franja}</div></div>',
        unsafe_allow_html=True)


def titulo_pagina(titulo, descripcion):
    st.markdown(f'<h2 class="pagina">{escape(titulo)}</h2><p class="desc">{escape(descripcion)}</p>', unsafe_allow_html=True)


def _kpi(etiqueta, valor, color, suave, icono, texto=False):
    clase = "kv txt" if texto else "kv"
    return (f'<div class="kpi" style="border-top:6px solid {color}"><div class="kicon" style="background:{suave}">'
            f'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="{NAVY}" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONOS[icono]}</svg></div>'
            f'<div><div class="kl">{escape(etiqueta)}</div><div class="{clase}">{escape(str(valor))}</div></div></div>')


def tarjetas_generales(p, a):
    """Proyectos, estudiantes, personas impactadas y lugares (municipios distintos)."""
    lugares = a["municipio"].replace("Sin dato", None).dropna().nunique()
    html = (_kpi("Proyectos", fmt(len(p)), NARANJA, "#FFE3DB", "proyectos")
            + _kpi("Estudiantes", fmt(p["estudiantes"].sum()), AMBAR, "#FEEFC9", "estudiantes")
            + _kpi("Personas impactadas", fmt(p["personas_impactadas"].sum()), LILA, "#EEDDFC", "personas")
            + _kpi("Lugares (municipios)", fmt(lugares), VERDE, "#CFE3E0", "lugares"))
    st.markdown(f'<div class="grid4">{html}</div>', unsafe_allow_html=True)


def tarjetas_destacadas(p, a):
    """Aliados distintos, tipo de aliado más frecuente y tipo de producto más frecuente."""
    from utils.datos import SIN_PRODUCTO, aliados_unicos, mas_frecuente
    u = aliados_unicos(a)
    tipo_al = mas_frecuente(u["tipo_aliado"])
    prod = mas_frecuente(p.loc[p["tipo_producto"] != SIN_PRODUCTO, "tipo_producto"])
    html = (_kpi("Aliados distintos", fmt(len(u)), NAVY, "#DADCEB", "aliados")
            + _kpi("Tipo de aliado más frecuente", tipo_al, AMBAR, "#FEEFC9", "aliados", True)
            + _kpi("Tipo de producto más frecuente", prod, NARANJA, "#FFE3DB", "producto", True))
    st.markdown(f'<div class="grid3">{html}</div>', unsafe_allow_html=True)


@contextmanager
def tarjeta(titulo, subtitulo=""):
    """Tarjeta blanca con título (cada gráfica lleva el suyo)."""
    st.session_state["_n_tarjeta"] = st.session_state.get("_n_tarjeta", 0) + 1
    with st.container(key=f"card_{st.session_state['_n_tarjeta']}"):
        st.markdown(f'<div class="ct">{escape(titulo)}</div><div class="cs">{escape(subtitulo)}</div>', unsafe_allow_html=True)
        yield


def lista_proyectos(p, a, limite=12):
    """Tarjetas con descripción y enlace de cada proyecto."""
    orden = p.sort_values(["semestre", "id_proyecto"], ascending=[False, True])
    todos = True
    if len(orden) > limite:
        todos = st.toggle(f"Mostrar los {len(orden)} proyectos (ahora se ven {limite})", key="ver_todos")
    muestra = orden if todos else orden.head(limite)
    aliados = a.groupby("id_proyecto")["aliado"].apply(lambda s: ", ".join(dict.fromkeys(s)))
    tarjetas = []
    for r in muestra.itertuples():
        tema = escape(str(r.tematica_proyecto)) if str(r.tematica_proyecto) not in ("<NA>", "nan") else ""
        prod = r.nombre_producto
        prod_txt = f" · «{escape(str(prod))}»" if isinstance(prod, str) and prod.strip() else ""
        al = aliados.get(r.id_proyecto, "")
        al_html = f'<div class="a">Aliados: {escape(al)}</div>' if al else ""
        boton = (f'<a class="btn" href="{escape(r.link)}" target="_blank" rel="noopener">Ver producto</a>'
                 if r.tiene_link else '<span class="sinlink">Sin enlace disponible</span>')
        tarjetas.append(
            f'<div class="proy"><div class="n">{escape(str(r.nombre_proyecto))}</div>'
            f'<div class="t">{tema}{prod_txt}</div>'
            f'<div><span class="tag">{escape(r.semestre)}</span><span class="tag">{escape(r.tipo_producto)}</span>'
            f'<span class="tag">{r.estudiantes} estudiantes</span>'
            f'<span class="tag">{fmt(r.personas_impactadas)} personas impactadas</span></div>'
            f'{al_html}{boton}</div>')
    st.markdown(f'<div class="proy-grid">{"".join(tarjetas)}</div>', unsafe_allow_html=True)
