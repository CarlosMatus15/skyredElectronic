import streamlit as st
import sqlite3
from datetime import datetime
import os

# --- Función para verificar el estado de la gestión de mensajes ---
def verificar_gestion_habilitada():
    ruta_archivo = os.path.expanduser("~/Downloads/skyred.txt")
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, "r") as f:
            contenido = f.read().strip()
            return contenido == "skyred=1"
    return False

# --- Función para guardar mensajes en SQLite ---
def guardar_mensaje(nombre, email, mensaje, telefono):
    conn = sqlite3.connect('mensajes.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS mensajes (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, email TEXT, mensaje TEXT, telefono TEXT, fecha_hora TEXT, leido INTEGER DEFAULT 0)")
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO mensajes (nombre, email, mensaje, telefono, fecha_hora) VALUES (?, ?, ?, ?, ?)", (nombre, email, mensaje, telefono, fecha_hora))
    conn.commit()
    conn.close()

# --- Función para mostrar y gestionar mensajes ---
def mostrar_mensajes():
    st.header("Gestión de Mensajes")
    conn = sqlite3.connect('mensajes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, mensaje, telefono, fecha_hora, leido FROM mensajes ORDER BY fecha_hora DESC")
    mensajes = cursor.fetchall()
    conn.close()

    if mensajes:
        for id_mensaje, nombre, email, mensaje_texto, telefono, fecha_hora, leido in mensajes:
            with st.expander(f"De: {nombre} ({email}) - {fecha_hora} ({'Leído' if leido else 'No Leído'})"):
                st.write(f"**Mensaje:** {mensaje_texto}")
                st.write(f"**Teléfono:** {telefono if telefono else 'No proporcionado'}") # Mostrar el teléfono
                col_leido, col_eliminar = st.columns(2)
                with col_leido:
                    if not leido:
                        if st.button(f"Marcar como Leído", key=f"leido_{id_mensaje}"):
                            marcar_leido(id_mensaje)
                            st.rerun()
                with col_eliminar:
                    if st.button(f"Eliminar Mensaje", key=f"eliminar_{id_mensaje}"):
                        eliminar_mensaje(id_mensaje)
                        st.rerun()
    else:
        st.info("No hay mensajes recibidos.")

def marcar_leido(id_mensaje):
    conn = sqlite3.connect('mensajes.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE mensajes SET leido = 1 WHERE id = ?", (id_mensaje,))
    conn.commit()
    conn.close()

def eliminar_mensaje(id_mensaje):
    conn = sqlite3.connect('mensajes.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mensajes WHERE id = ?", (id_mensaje,))
    conn.commit()
    conn.close()

# --- Configuración de la página ---
st.set_page_config(
    page_title="Skyred Electronic",
    page_icon=":iphone:",
    layout="wide",
)

# --- Estilos CSS Personalizados ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap');

    .stApp {
        background-color: #e0e0e0 !important; /* Gris claro tecnológico */
        font-family: 'Open Sans', sans-serif !important;
    }
    .st-emotion-cache-container {
        max-width: 1200px !important; /* Limitar el ancho del contenido para mejor lectura */
        padding: 1rem;
        margin: 0 auto; /* Centrar el contenido */
    }
    .st-header {
        background-color: rgba(240, 248, 255, 0.8); /* Fondo semitransparente para el header */
        padding: 1rem;
        border-radius: 5px;
    }
    .st-subheader {
        color: #336699; /* Un tono de azul más oscuro para los subheaders */
    }
    .social-buttons {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }
    .social-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-decoration: none;
        color: white;
    }
    .facebook {
        background-color: #1877F2;
    }
    .instagram {
        background: linear-gradient(45deg, #405de6, #5851db, #833ab4, #c13584, #e1306c, #fd1d1d);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Encabezado ---
st.title("Skyred Electronic: Soluciones Integrales para tus Dispositivos Móviles")
st.subheader("Tu aliado en soluciones para celulares, tablets y laptops en Hermosillo")

st.markdown("En **Skyred Electronic**, nos especializamos en ofrecer soluciones integrales para tus dispositivos móviles. Nuestra amplia gama de servicios y productos te brinda la tranquilidad de saber que tus dispositivos están en buenas manos.", True)
st.markdown("📍 **Visítanos en Hermosillo, Sonora**", True)

st.divider()

# --- Venta de Celulares ---
st.header("Venta de Celulares")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Venta al mayoreo y menudeo")
    st.markdown("Ofrecemos una amplia variedad de celulares de alta calidad a precios competitivos, tanto para ventas al mayoreo como al menudeo.")
    st.image("Assets/Samsung.jpeg", caption="Celulares al Mayoreo", use_container_width=True)
with col2:
    st.subheader("Crédito celular")
    st.markdown("Tenemos opciones de crédito celular para que puedas adquirir el dispositivo que necesitas sin tener que pagar el precio total de contado.")
    st.image("Assets/Credito.jpeg", caption="Opciones de Crédito", use_container_width=True)

st.divider()

# --- Opciones de Crédito ---
st.header("Opciones de Crédito")
st.markdown("Facilitamos la adquisición de tu nuevo dispositivo con diversas opciones de crédito:")
st.markdown("- **PAYJOY:** Adquiere tu dispositivo móvil de manera fácil y rápida.")
st.markdown("- **Valetodo:** Compra tu celular con mayor flexibilidad.")
st.markdown("- **Crédito Plata:** Plan de pago personalizado para tu nuevo celular.")
st.markdown("- **Convenio con Banbajío:** Opciones de financiamiento exclusivas.")
st.image("Assets/Credito2.jpeg", caption="Facilidades de Pago", use_container_width=True)

st.divider()

# --- Meses sin Intereses ---
st.header("Meses sin Intereses")
st.markdown("Aprovecha nuestras promociones para que tu compra sea aún más accesible:")
st.markdown("- **Meses sin intereses con MasterCard:** Compra tus dispositivos móviles sin preocupaciones.")
st.image("Assets/Credito3.jpeg", caption="Meses sin Intereses con MasterCard", width=200)

st.divider()

# --- Reparación de Dispositivos ---
st.header("Reparación de Dispositivos")
st.markdown("Nuestro equipo de expertos está listo para solucionar cualquier problema con tus dispositivos:")

col3, col4 = st.columns(2)
with col3:
    st.subheader("Reparamos:")
    st.markdown("- Celulares")
    st.markdown("- Tablets")
    st.markdown("- Laptops")
    st.markdown("- **Especialistas en reparación de iPhone:** Software, pantallas rotas y más.")
    st.image("Assets/reparacion_Pantallas.jpeg", caption="Expertos en Reparación", use_container_width=True)
with col4:
    st.subheader("Nuestros servicios incluyen:")
    st.markdown("- Reparación de software y hardware")
    st.markdown("- Desbloqueo de iPhone")
    st.markdown("- Cambio de ESIM a SIM física")
    st.markdown("- Reparación de equipos mojados")
    st.markdown("- Cambio de batería y centro de carga")
    st.image("Assets/Cambio_de_SIM.jpeg", caption="Servicios Especializados", width=150)

st.divider()

# --- Venta de Accesorios ---
st.header("Venta de Accesorios")
st.markdown("Complementa tus dispositivos con nuestros accesorios de calidad:")
st.markdown("- **Venta de pantallas para celulares:** Amplia variedad de modelos.")
st.image("Assets/AirPods.jpeg", caption="Venta de Pantallas", use_container_width=True)
st.markdown("- **Accesorios para celulares:** Cargadores de iPhone y mucho más.")
st.image("Assets/MagSafeCase.jpeg", caption="Accesorios para tu Móvil", use_container_width=True)

st.divider()

# --- Contacto y Ubicación ---
st.header("¡Contáctanos o Visítanos!")

col_contacto, col_mapa = st.columns(2)

with col_contacto:
    st.subheader("Formulario de Contacto")
    with st.form("contacto"):
        nombre = st.text_input("Nombre")
        email = st.text_input("Correo Electrónico")
        telefono = st.text_input("Número de Móvil (opcional)") # Marcamos como opcional
        mensaje = st.text_area("Mensaje")
        submitted = st.form_submit_button("Enviar Mensaje")
        if submitted:
            guardar_mensaje(nombre, email, mensaje, telefono)
            st.success("¡Gracias por tu mensaje! Lo hemos recibido y te contactaremos pronto.")

    st.subheader("Síguenos en Redes Sociales")
    st.markdown(
        f"""
        <div class="social-buttons">
            <a href="https://www.facebook.com/tu_pagina_de_facebook" target="_blank" class="social-button facebook">
                <i class="fab fa-facebook-f"></i> Facebook
            </a>
            <a href="https://www.instagram.com/tu_pagina_de_instagram" target="_blank" class="social-button instagram">
                <i class="fab fa-instagram"></i> Instagram
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_mapa:
    st.subheader("Ubicación en Hermosillo")
    map_data = {
        "lat": [29.0968],
        "lon": [-110.9656],
    }
    st.map(data=map_data, latitude="lat", longitude="lon", zoom=16)
    st.markdown("Nayarit 246, Hermosillo, Sonora")

st.divider()

# --- Gestión de Mensajes (Condicional) ---
if verificar_gestion_habilitada():
    mostrar_mensajes()
else:
    st.info("La gestión de mensajes no está habilitada.")

# --- Pie de Página ---
st.markdown("---")
st.markdown("© 2025 Skyred Electronic - Todos los derechos reservados")
