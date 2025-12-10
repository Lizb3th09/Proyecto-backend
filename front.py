import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
import plotly.express as px
from folium.plugins import MarkerCluster

st.set_page_config(layout="wide")
st.title("Mapa de Gimnasios en Ensenada")

# --- URL del backend ---
BACKEND_URL = "http://127.0.0.1:5000/api/datos_negocios"

# --- Hacer request al backend ---
try:
    response = requests.get(BACKEND_URL)
    if response.status_code == 429:
        st.warning("Has alcanzado el límite de 300 requests por día. 🐣")
        st.stop()
    response.raise_for_status()
    df = pd.DataFrame(response.json())
except requests.exceptions.RequestException as e:
    st.error(f"No se pudo obtener datos del backend: {e}")
    st.stop()

# --- Filtrar datos válidos ---
df = df[(df['latitud'].notna()) & (df['longitud'].notna())]

if df.empty:
    st.warning("No hay gimnasios dentro de Ensenada para mostrar.")
    st.stop()

# --- Función para limpiar valores ---
def limpio(valor):
    return bool(valor) and valor != "-" and valor != "0"

# --- Contadores de contactos ---
contactos = {
    "Solo Teléfono": 0,
    "Solo Correo": 0,
    "Solo Web": 0,
    "Ninguno": 0,
    "Múltiples": 0,
}

# --- Crear mapa con clusters ---
m = folium.Map(location=[31.82, -116.7], zoom_start=12, tiles="CartoDB positron")
marker_cluster = MarkerCluster().add_to(m)

for _, row in df.iterrows():
    tiene_telefono = limpio(row.get("telefono"))
    tiene_correo = limpio(row.get("correoelec"))
    tiene_web = limpio(row.get("web"))
    total_datos = int(tiene_telefono) + int(tiene_correo) + int(tiene_web)

    if total_datos == 0:
        contactos["Ninguno"] += 1
    elif total_datos == 1:
        if tiene_telefono:
            contactos["Solo Teléfono"] += 1
        elif tiene_correo:
            contactos["Solo Correo"] += 1
        elif tiene_web:
            contactos["Solo Web"] += 1
    else:
        contactos["Múltiples"] += 1

    popup_content = f"""
    <div style="font-size:14px;">
    <b>{row.get('nom_estab')}</b><br>
    Tel: {row.get('telefono') or '-'}<br>
    Email: {row.get('correoelec') or '-'}<br>
    Web: {row.get('web') or '-'}
    </div>
    """
    folium.Marker(
        location=[row["latitud"], row["longitud"]],
        popup=popup_content
    ).add_to(marker_cluster)

# Mostrar mapa
st_folium(m, width=1000, height=600)

# --- Crear gráfica de contactos ---
fig = px.bar(
    x=list(contactos.keys()),
    y=list(contactos.values()),
    labels={"x": "Tipo de contacto", "y": "Cantidad de gimnasios"},
    color=list(contactos.keys()),
    color_discrete_map={
        "Solo Teléfono": "#34db69",
        "Solo Correo": "#9b59b6",
        "Solo Web": "#ff1c82",
        "Ninguno": "#fffb00",
        "Múltiples": "#f39c12",
    },
)
fig.update_layout(
    title="Gimnasios según medios de contacto",
    title_x=0.5,
    margin=dict(l=10, r=10, t=40, b=10),
    height=400,
)

# Mostrar gráfica
st.plotly_chart(fig, use_container_width=True)
