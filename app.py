import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. CONFIGURACIÓN VISUAL
# ---------------------------------------------------------
st.set_page_config(page_title="Validador VATC", page_icon="☁️", layout="centered")

st.title("☁️ Consulta en Vivo (Cloud)")
st.write("Conectado directamente a Google Sheets.")

# ---------------------------------------------------------
# 2. EL ENLACE MÁGICO
# ---------------------------------------------------------
# PEGA AQUÍ el enlace que copiaste en el paso anterior (el que termina en .csv)
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSeBSF5vsJPH6pVfyL0phuk-oN3QDJcymB9mfq-WYRD77BOfBDb7vDBXxanGtDWLd8k9uyLMZVVkln6/pub?gid=0&single=true&output=csv"


@st.cache_data(ttl=60) # ttl=60 hace que la app refresque los datos cada minuto
def cargar_datos_nube():
    try:
        # Python lee el enlace de internet directamente
        df = pd.read_csv(GOOGLE_SHEET_URL)
        
        # Limpiamos los datos para evitar errores de mayúsculas o espacios
        df['RIF / CEDIULA'] = df['RIF / CEDIULA'].astype(str).str.strip().str.upper()
        return df
    except Exception as e:
        st.error(f"⚠️ Error al conectar con la nube: {e}")
        return pd.DataFrame()

# Cargamos la data
df_clientes = cargar_datos_nube()

# ---------------------------------------------------------
# 3. INTERFAZ Y BÚSQUEDA
# ---------------------------------------------------------
rif_input = st.text_input("RIF A CONSULTAR:").strip().upper()

if st.button("Guardar Consulta"):
    if rif_input == "":
        st.warning("⚠️ Ingrese un RIF.")
    elif df_clientes.empty:
        st.error("⚠️ No se pudo obtener la información de la nube.")
    else:
        # Lógica de validación
        if rif_input in df_clientes['RIF / CEDIULA'].values:
            # Encontrado en lista negra
            fila = df_clientes[df_clientes['RIF / CEDIULA'] == rif_input]
            empresa = fila['RAZÓN SOCIAL'].iloc[0]
            st.error(f"🚨 CLIENTE EXISTE, CONTACTAR CON OFICINA CENTRAL.\n\nEmpresa: **{empresa}**")
        else:
            # Cliente Limpio
            st.success("✅ Cliente no existe o no se encontró. Puede proceder.")