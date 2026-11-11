# Dashboard Expopaz

Repositorio de estadísticas de los proyectos de Expopaz (Streamlit).

## Ejecutar en tu computador
```
pip install -r requirements.txt
streamlit run app.py
```

## Actualizar los datos
Reemplaza `data/expopaz_base_final.xlsx` (hojas `Proyectos` y `Aliados`, mismas columnas) y vuelve a ejecutar.

## Dónde cambiar los textos
`utils/estilo.py`: `TITULO`, `AUTORAS` y `QUE_ES`. La descripción de cada pestaña está al inicio de su archivo en `views/`.
