import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit.components.v1 as components

# --- CONFIGURACIÓN GENERAL ---
st.set_page_config(page_title="Sentinela QR Móvil", layout="centered")
st.title("📱 Sentinela QR desde Celular")

# --- CONECTAR A GOOGLE SHEETS ---
json_path = "registro-eventos-hugo-bf4035e53377.json"
sheet_id = "1yWJoHTzHRwxCPQCnthm2MCgD2DFO--fQEgqMq0_fbCM"
sheet_name = "DatosQR"

@st.cache_resource
def conectar_hoja():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
    client = gspread.authorize(creds)
    hoja = client.open_by_key(sheet_id).worksheet(sheet_name)
    return hoja

hoja, connection_message = conectar_hoja(), ""
if hoja is None:
    st.error("❌ No se pudo conectar a Google Sheets")
    st.stop()
else:
    st.success("✅ Conectado a Google Sheets correctamente")

# --- ESCANEO QR DESDE CELULAR ---
st.subheader("📸 Escanea el código QR desde tu celular:")

html_code = """
<script src=\"https://unpkg.com/html5-qrcode\"></script>
<div id=\"reader\" style=\"width:300px; margin:auto;\"></div>
<script>
function onScanSuccess(decodedText, decodedResult) {
    const url = new URL(window.location.origin + window.location.pathname);
    url.searchParams.set("codigo", decodedText);
    window.location.href = url.toString();
}
let html5QrcodeScanner = new Html5QrcodeScanner("reader", { fps: 10, qrbox: 250 });
html5QrcodeScanner.render(onScanSuccess);
</script>
"""

components.html(html_code, height=450)

# --- PROCESAR RESULTADO ---
codigo = st.query_params.get("codigo")

if codigo:
    st.success(f"📥 Código recibido automáticamente: {codigo}")
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [codigo, fecha, "Escaneado", "Lugar Desconocido", "Posición Desconocida", 1, "Usuario Desconocido"]

    try:
        hoja.append_row(data)
        st.success("✅ Código registrado automáticamente en Google Sheets")
        st.balloons()
    except Exception as e:
        st.error(f"❌ Error al registrar en Google Sheets: {e}")
else:
    st.warning("📷 Escanea un código QR para comenzar.")

