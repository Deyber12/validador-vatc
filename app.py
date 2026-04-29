import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. CONFIGURACIÓN VISUAL Y BRANDING
# ---------------------------------------------------------
st.set_page_config(page_title="Validador VATC", page_icon="🔍", layout="centered")

# Truco para centrar el logo: crear columnas y usar la del centro
col1, col2, col3 = st.columns([1, 2, 1]) # Proporción de ancho: 1:2:1
with col2:
    # st.image automáticamente adapta el tamaño, pero puedes limitarlo con width=
    # Pon aquí el nombre exacto de tu archivo (ej. "logo.png")
    st.image("logo.png", width=200)

st.markdown("<br>", unsafe_allow_html=True) # Un pequeño espacio extra
# Tu título original
st.title("🔍 Consulta de Clientes")
st.write("Verifica el estatus en el archivo maestro central.")

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
# max_chars=10 bloquea físicamente que escriban más de 10 caracteres
rif_input = st.text_input("RIF A CONSULTAR (Ej: V123456789):", max_chars=10).strip().upper()

if st.button("Guardar Consulta"):
    
    # --- INICIO DEL POLICÍA DE VALIDACIÓN ---
    if rif_input == "":
        st.warning("⚠️ Por favor, ingrese un RIF.")
        
    elif len(rif_input) < 10:
        # Si tiene 9 o menos, frena la búsqueda y avisa
        st.warning("⚠️ El RIF está incompleto. Debe tener exactamente 10 caracteres (Ej: V123456789).")
        
    elif df_clientes.empty:
        st.error("⚠️ No se pudo obtener la información de la nube.")
        
    # --- FIN DEL POLICÍA. SI TODO ESTÁ BIEN, BUSCA ---
    else:
        # Lógica de validación en tu base de datos
        if rif_input in df_clientes['RIF / CEDIULA'].values:
            # Encontrado en lista negra
            fila = df_clientes[df_clientes['RIF / CEDIULA'] == rif_input]
            empresa = fila['RAZÓN SOCIAL'].iloc[0]
            st.error(f"🚨 CLIENTE EXISTE, CONTACTAR A OFICINA CENTRAL.\n\nEmpresa: **{empresa}**")
        else:
            # Cliente Limpio
            st.success("✅ Cliente no existe o no se encontró. Puede proceder con la venta.")
