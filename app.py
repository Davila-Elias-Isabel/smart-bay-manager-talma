import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Configuración del documento web
st.set_page_config(
    page_title="Smart Bay Manager | Talma",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# PERSISTENCIA DE DATOS (JSON)
# -------------------------------------------------------------
DATA_FILE = "smart_bay_data.json"

def load_data():
    """Carga los datos desde el archivo JSON si existe."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            st.session_state.bahias = data.get("bahias", st.session_state.bahias)
            st.session_state.equipos_pendientes = data.get("equipos_pendientes", st.session_state.equipos_pendientes)
            st.session_state.usuarios = data.get("usuarios", st.session_state.usuarios)
            st.session_state.historial = data.get("historial", st.session_state.historial)
            st.session_state.umbrales_alerta = data.get("umbrales_alerta", st.session_state.umbrales_alerta)

def save_data():
    """Guarda los datos actuales en el archivo JSON."""
    data = {
        "bahias": st.session_state.bahias,
        "equipos_pendientes": st.session_state.equipos_pendientes,
        "usuarios": st.session_state.usuarios,
        "historial": st.session_state.historial,
        "umbrales_alerta": st.session_state.umbrales_alerta
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# -------------------------------------------------------------
# 1. ESTADO GLOBAL (SESSION STATE)
# -------------------------------------------------------------
if "usuarios" not in st.session_state:
    st.session_state.usuarios = {
        "supervisor": {"nombre": "Carlos Mendoza", "rol": "Supervisor de Mantenimiento", "pass": "TalmaSup2026!"},
        "planificador": {"nombre": "Ana Ramos", "rol": "Planificador CCO", "pass": "TalmaPlan2026!"},
        "tecnico": {"nombre": "Jorge Salinas", "rol": "Técnico de Mantenimiento", "pass": "TalmaTec2026!"},
        "coordinador": {"nombre": "Luis Paredes", "rol": "Coordinador CCO Operaciones", "pass": "TalmaCoord2026!"},
        "admin": {"nombre": "Admin General", "rol": "Administrador del Sistema", "pass": "TalmaAdmin2026!"}
    }

if "sesion_activa" not in st.session_state:
    st.session_state.sesion_activa = None

if "umbrales_alerta" not in st.session_state:
    st.session_state.umbrales_alerta = {
        "Taller PV1": 2,
        "Taller Lote Comercial": 1,
        "Taller Lote Carguero": 1
    }

if "bahias" not in st.session_state:
    st.session_state.bahias = [
        {"id": "BAY-PV1-01", "taller": "Taller PV1", "familia": "PM", "estado": "Libre", "equipo": None, "ingreso": None},
        {"id": "BAY-PV1-02", "taller": "Taller PV1", "familia": "LO", "estado": "Ocupada", "equipo": "LO-204", "ingreso": "2026-09-11 08:30"},
        {"id": "BAY-PV1-03", "taller": "Taller PV1", "familia": "CA/CB", "estado": "Libre", "equipo": None, "ingreso": None},
        {"id": "BAY-PV1-04", "taller": "Taller PV1", "familia": "TR", "estado": "Libre", "equipo": None, "ingreso": None},
        {"id": "BAY-LC-01", "taller": "Taller Lote Comercial", "familia": "PM", "estado": "Ocupada", "equipo": "PM-101", "ingreso": "2026-09-11 09:15"},
        {"id": "BAY-LC-02", "taller": "Taller Lote Comercial", "familia": "LO", "estado": "Libre", "equipo": None, "ingreso": None},
        {"id": "BAY-LC-03", "taller": "Taller Lote Comercial", "familia": "TR", "estado": "Libre", "equipo": None, "ingreso": None},
        {"id": "BAY-LCR-01", "taller": "Taller Lote Carguero", "familia": "CA/CB", "estado": "Ocupada", "equipo": "CB-305", "ingreso": "2026-09-11 07:45"},
        {"id": "BAY-LCR-02", "taller": "Taller Lote Carguero", "familia": "LO", "estado": "Libre", "equipo": None, "ingreso": None},
        {"id": "BAY-LCR-03", "taller": "Taller Lote Carguero", "familia": "PM", "estado": "Libre", "equipo": None, "ingreso": None}
    ]

if "equipos_pendientes" not in st.session_state:
    st.session_state.equipos_pendientes = [
        {"codigo": "PM-108", "familia": "PM", "tipo": "Plataforma Móvil", "ot": "OT-2026-441"},
        {"codigo": "LO-215", "familia": "LO", "tipo": "Loader de Carga", "ot": "OT-2026-442"},
        {"codigo": "TR-402", "familia": "TR", "tipo": "Tractor de Remolque", "ot": "OT-2026-443"},
        {"codigo": "CB-310", "familia": "CA/CB", "tipo": "Cinta Transportadora", "ot": "OT-2026-444"}
    ]

if "historial" not in st.session_state:
    st.session_state.historial = [
        {"timestamp": "2026-09-11 08:30", "evento": "Ingreso Equipo", "bahia": "BAY-PV1-02", "equipo": "LO-204", "taller": "Taller PV1", "usuario": "Jorge Salinas"},
        {"timestamp": "2026-09-11 09:15", "evento": "Ingreso Equipo", "bahia": "BAY-LC-01", "equipo": "PM-101", "taller": "Taller Lote Comercial", "usuario": "Jorge Salinas"},
        {"timestamp": "2026-09-11 07:45", "evento": "Ingreso Equipo", "bahia": "BAY-LCR-01", "equipo": "CB-305", "taller": "Taller Lote Carguero", "usuario": "Jorge Salinas"}
    ]

# Cargar datos persistentes si existen
load_data()

# -------------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS
# -------------------------------------------------------------
st.markdown("""
<style>
    div.stButton > button[kind="primary"] {
        background-color: #7ead3e !important;
        border-color: #7ead3e !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 6px;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #6c9934 !important;
        border-color: #6c9934 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #012b6c !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #f1f5f9 !important;
        font-weight: 500;
    }
    .bay-card {
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 14px;
        background-color: #ffffff;
        box-shadow: 0 2px 5px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
    }
    .bay-libre {
        border-left: 6px solid #7ead3e !important;
    }
    .bay-ocupada {
        border-left: 6px solid #dc2626 !important;
    }
    .badge-libre {
        background-color: #7ead3e;
        color: #ffffff;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .badge-ocupada {
        background-color: #dc2626;
        color: #ffffff;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# LOGO CORPORATIVO TALMA
# -------------------------------------------------------------
logo_talma_html = """
<div style="text-align: center; padding: 15px 0 10px 0;">
    <svg width="220" height="75" viewBox="0 0 320 110" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M72 16 L110 16 L104 35 L66 35 Z" fill="#7ead3e"/>
        <text x="32" y="78" font-family="'Arial Black', Impact, sans-serif" font-weight="900" font-size="64" fill="#ffffff" font-style="italic">Talma</text>
        <text x="32" y="98" font-family="Arial, Helvetica, sans-serif" font-size="13.5" font-weight="bold" fill="#7ead3e" letter-spacing="1.3">LÍDER EN SERVICIOS AEROPORTUARIOS</text>
    </svg>
</div>
"""

# -------------------------------------------------------------
# 2. AUTENTICACIÓN (CU-01)
# -------------------------------------------------------------
st.sidebar.markdown(logo_talma_html, unsafe_allow_html=True)
st.sidebar.markdown("<h3 style='text-align:center; margin-top:-5px;'>Smart Bay Manager</h3>", unsafe_allow_html=True)

if not st.session_state.sesion_activa:
    st.markdown("""
    <div style='background-color:#012b6c; padding:30px; border-radius:10px; margin-bottom:25px;'>
        <h1 style='color:#ffffff; margin:0;'>🛫 Smart Bay Manager</h1>
        <p style='color:#7ead3e; font-weight:bold; font-size:1.15rem; margin:8px 0 0 0;'>SISTEMA DE GESTIÓN INTELIGENTE DE BAHÍAS — TALMA SERVICIOS AEROPORTUARIOS</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_l2 = st.columns([1, 1])
    with col_l1:
        st.subheader("Acceso al Sistema (CU-01)")
        username = st.selectbox("Seleccione Usuario para Demostración", list(st.session_state.usuarios.keys()))
        
        # CORRECCIÓN DE SEGURIDAD: No pre-llenar la contraseña
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Iniciar Sesión", type="primary", use_container_width=True):
            user_data = st.session_state.usuarios[username]
            if password == user_data["pass"]:
                st.session_state.sesion_activa = {
                    "username": username,
                    "nombre": user_data["nombre"],
                    "rol": user_data["rol"]
                }
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
    with col_l2:
        st.info("""
        **Roles disponibles según el Producto Acreditable:**
        * **Supervisor de Mantenimiento:** Asignación de bahías y configuración de umbrales.
        * **Planificador CCO:** Monitoreo de disponibilidad y reportes históricos.
        * **Técnico de Mantenimiento:** Terminal de ingreso físico y liberación de bahías.
        * **Coordinador CCO Operaciones:** Supervisión de alertas de saturación.
        * **Administrador del Sistema:** Gestión centralizada de usuarios.
        """)
    st.stop()

# Menú lateral para usuario con sesión activa
usuario_act = st.session_state.sesion_activa
st.sidebar.markdown(f"👤 **Usuario:** {usuario_act['nombre']}")
st.sidebar.markdown(f"💼 **Rol:** `{usuario_act['rol']}`")

if st.sidebar.button("Cerrar Sesión"):
    st.session_state.sesion_activa = None
    st.rerun()

st.sidebar.divider()
menu = st.sidebar.radio(
    "Módulos del Sistema",
    ["📊 Tablero de Disponibilidad (CU-02)",
     "📌 Asignar Bahía a Equipo (CU-03)",
     "🛠️ Terminal Operativo de Taller (CU-05 / CU-06)",
     "⚠️ Alertas y Umbrales (CU-04 / CU-07)",
     "📈 Reporte de Ocupación (CU-08)",
     "👥 Gestión de Usuarios (CU-09)"]
)

# -------------------------------------------------------------
# 3. TABLERO DE DISPONIBILIDAD EN TIEMPO REAL (CU-02 / CU-07)
# -------------------------------------------------------------
if menu == "📊 Tablero de Disponibilidad (CU-02)":
    st.markdown("""
    <div style='border-left: 6px solid #012b6c; padding-left: 15px; margin-bottom: 20px;'>
        <h2 style='margin:0; color:#012b6c;'>Tablero Maestro de Bahías en Tiempo Real</h2>
        <span style='color:#555;'>Monitoreo centralizado para CCO y Supervisión de Mantenimiento</span>
    </div>
    """, unsafe_allow_html=True)

    for taller, umbral in st.session_state.umbrales_alerta.items():
        libres = sum(1 for b in st.session_state.bahias if b["taller"] == taller and b["estado"] == "Libre")
        if libres <= umbral:
            st.error(f"🚨 **ALERTA CRÍTICA DE CAPACIDAD ({taller.upper()}):** Solo quedan {libres} bahía(s) disponible(s). Umbral fijado: {umbral}.")

    total_b = len(st.session_state.bahias)
    libres_b = sum(1 for b in st.session_state.bahias if b["estado"] == "Libre")
    ocupadas_b = total_b - libres_b
    porcentaje_ocupacion = (ocupadas_b / total_b) * 100 if total_b > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Bahías", total_b)
    col2.metric("Bahías Ocupadas", ocupadas_b)
    col3.metric("Bahías Libres", libres_b)
    col4.metric("% Ocupación Flota", f"{porcentaje_ocupacion:.1f}%")

    st.divider()

    f_col1, f_col2 = st.columns(2)
    with f_col1:
        f_taller = st.selectbox("Filtrar por Taller", ["Todos", "Taller PV1", "Taller Lote Comercial", "Taller Lote Carguero"])
    with f_col2:
        f_familia = st.selectbox("Filtrar por Familia GSE", ["Todas", "PM", "LO", "CA/CB", "TR"])

    bahias_filtradas = st.session_state.bahias
    if f_taller != "Todos":
        bahias_filtradas = [b for b in bahias_filtradas if b["taller"] == f_taller]
    if f_familia != "Todas":
        bahias_filtradas = [b for b in bahias_filtradas if b["familia"] == f_familia]

    st.markdown("### Estado Actual de Bahías Físicas")
    cols_bahias = st.columns(3)
    for idx, b in enumerate(bahias_filtradas):
        with cols_bahias[idx % 3]:
            es_libre = b["estado"] == "Libre"
            clase_b = "bay-libre" if es_libre else "bay-ocupada"
            badge = '<span class="badge-libre">LIBRE</span>' if es_libre else f'<span class="badge-ocupada">OCUPADA ({b["equipo"]})</span>'
            
            st.markdown(f"""
            <div class="bay-card {clase_b}">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <strong style="color:#012b6c; font-size:1.15rem;">{b['id']}</strong>
                    {badge}
                </div>
                <div style="font-size:0.9rem; color:#333; line-height: 1.5;">
                    <b>Taller:</b> {b['taller']}<br>
                    <b>Familia admitida:</b> <code>{b['familia']}</code><br>
                    <b>Hora Ingreso:</b> {b['ingreso'] if b['ingreso'] else '—'}
                </div>
            </div>
            """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 4. ASIGNACIÓN DE BAHÍA A EQUIPO (CU-03)
# -------------------------------------------------------------
elif menu == "📌 Asignar Bahía a Equipo (CU-03)":
    st.markdown("""
    <div style='border-left: 6px solid #012b6c; padding-left: 15px; margin-bottom: 20px;'>
        <h2 style='margin:0; color:#012b6c;'>Asignar Bahía a Equipo GSE</h2>
        <span style='color:#555;'>Módulo restringido para el Supervisor de Mantenimiento</span>
    </div>
    """, unsafe_allow_html=True)

    if usuario_act["rol"] not in ["Supervisor de Mantenimiento", "Administrador del Sistema"]:
        st.warning("⚠️ Acceso reservado exclusivamente para la Supervisión de Mantenimiento.")
        st.stop()

    if not st.session_state.equipos_pendientes:
        st.success("✅ No existen equipos GSE pendientes en cola.")
    else:
        col_as1, col_as2 = st.columns(2)
        with col_as1:
            st.subheader("1. Equipo con Orden de Trabajo")
            opciones_eq = {f"{eq['codigo']} ({eq['tipo']}) | Familia: {eq['familia']} | {eq['ot']}": eq for eq in st.session_state.equipos_pendientes}
            seleccion_eq_label = st.selectbox("Seleccione Equipo GSE", list(opciones_eq.keys()))
            eq_sel = opciones_eq[seleccion_eq_label]

            st.info(f"**Regla de Negocio:** El equipo `{eq_sel['codigo']}` requiere una bahía compatible con la familia `{eq_sel['familia']}`.")

        with col_as2:
            st.subheader("2. Bahía Compatible y Libre")
            compatibles = [
                b for b in st.session_state.bahias 
                if b["estado"] == "Libre" and b["familia"] == eq_sel["familia"]
            ]

            if not compatibles:
                st.error(f"No hay bahías disponibles para la familia {eq_sel['familia']} en ningún taller.")
            else:
                opciones_b = {f"{b['id']} — {b['taller']}": b for b in compatibles}
                sel_b_label = st.selectbox("Bahías Habilitadas", list(opciones_b.keys()))
                b_sel = opciones_b[sel_b_label]

                if st.button("Confirmar Asignación", type="primary", use_container_width=True):
                    for b in st.session_state.bahias:
                        if b["id"] == b_sel["id"]:
                            b["estado"] = "Ocupada"
                            b["equipo"] = eq_sel["codigo"]
                            b["ingreso"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    
                    st.session_state.equipos_pendientes = [
                        eq for eq in st.session_state.equipos_pendientes if eq["codigo"] != eq_sel["codigo"]
                    ]

                    st.session_state.historial.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "evento": "Asignación e Ingreso",
                        "bahia": b_sel["id"],
                        "equipo": eq_sel["codigo"],
                        "taller": b_sel["taller"],
                        "usuario": usuario_act["nombre"]
                    })
                    
                    save_data() # Guardar cambios
                    st.success(f"Equipo {eq_sel['codigo']} asignado exitosamente a la bahía {b_sel['id']}.")
                    st.rerun()

# -------------------------------------------------------------
# 5. TERMINAL OPERATIVO DE TALLER (CU-05 / CU-06)
# -------------------------------------------------------------
elif menu == "🛠️ Terminal Operativo de Taller (CU-05 / CU-06)":
    st.markdown("""
    <div style='border-left: 6px solid #012b6c; padding-left: 15px; margin-bottom: 20px;'>
        <h2 style='margin:0; color:#012b6c;'>Terminal de Taller — Registro en Patio</h2>
        <span style='color:#555;'>Operado por Técnicos de Mantenimiento en estaciones de taller</span>
    </div>
    """, unsafe_allow_html=True)

    taller_sel = st.selectbox("Seleccione su Taller de Operación", ["Taller PV1", "Taller Lote Comercial", "Taller Lote Carguero"])
    bahias_taller = [b for b in st.session_state.bahias if b["taller"] == taller_sel]

    st.markdown(f"#### Bahías en {taller_sel}")
    for b in bahias_taller:
        with st.container(border=True):
            col_b1, col_b2, col_b3 = st.columns([2, 2, 2])
            with col_b1:
                st.markdown(f"**Bahía:** `{b['id']}` (Familia: `{b['familia']}`)")
                badge = '<span class="badge-libre">LIBRE</span>' if b['estado'] == 'Libre' else '<span class="badge-ocupada">OCUPADA</span>'
                st.markdown(f"**Estado:** {badge}", unsafe_allow_html=True)
            with col_b2:
                st.markdown(f"**Equipo en atención:** `{b['equipo'] if b['equipo'] else 'Ninguno'}`")
                st.markdown(f"**Hora Ingreso:** {b['ingreso'] if b['ingreso'] else '—'}")
            with col_b3:
                if b["estado"] == "Ocupada":
                    # CORRECCIÓN UX: Confirmación antes de liberar
                    if st.button(f"Liberar Bahía / Salida", key=f"lib_{b['id']}", type="primary"):
                        st.session_state[f"confirmar_liberacion_{b['id']}"] = True
                    
                    if st.session_state.get(f"confirmar_liberacion_{b['id']}", False):
                        st.warning("¿Está seguro de liberar esta bahía?")
                        col_conf1, col_conf2 = st.columns(2)
                        with col_conf1:
                            if st.button("Sí, liberar", key=f"si_{b['id']}"):
                                eq_salida = b["equipo"]
                                b["estado"] = "Libre"
                                b["equipo"] = None
                                b["ingreso"] = None

                                st.session_state.historial.append({
                                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "evento": "Salida / Liberación",
                                    "bahia": b["id"],
                                    "equipo": eq_salida,
                                    "taller": b["taller"],
                                    "usuario": usuario_act["nombre"]
                                })
                                save_data() # Guardar cambios
                                st.session_state[f"confirmar_liberacion_{b['id']}"] = False
                                st.success(f"Bahía {b['id']} liberada y disponible en patio.")
                                st.rerun()
                        with col_conf2:
                            if st.button("Cancelar", key=f"no_{b['id']}"):
                                st.session_state[f"confirmar_liberacion_{b['id']}"] = False
                                st.rerun()
                else:
                    st.caption("Bahía disponible para asignación")

# -------------------------------------------------------------
# 6. CONFIGURACIÓN DE UMBRALES Y ALERTAS (CU-04 / CU-07)
# -------------------------------------------------------------
elif menu == "⚠️ Alertas y Umbrales (CU-04 / CU-07)":
    st.markdown("""
    <div style='border-left: 6px solid #012b6c; padding-left: 15px; margin-bottom: 20px;'>
        <h2 style='margin:0; color:#012b6c;'>Gestión de Alertas de Capacidad Crítica</h2>
        <span style='color:#555;'>Configuración de parámetros y supervisión en tiempo real</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("1. Umbral Mínimo de Bahías Libres (CU-04)")
    if usuario_act["rol"] in ["Supervisor de Mantenimiento", "Administrador del Sistema"]:
        col_u1, col_u2, col_u3 = st.columns(3)
        with col_u1:
            u_pv1 = st.number_input("Umbral Taller PV1", min_value=0, max_value=5, value=st.session_state.umbrales_alerta["Taller PV1"])
        with col_u2:
            u_lc = st.number_input("Umbral Lote Comercial", min_value=0, max_value=5, value=st.session_state.umbrales_alerta["Taller Lote Comercial"])
        with col_u3:
            u_lcr = st.number_input("Umbral Lote Carguero", min_value=0, max_value=5, value=st.session_state.umbrales_alerta["Taller Lote Carguero"])

        if st.button("Guardar Nuevos Umbrales", type="primary"):
            st.session_state.umbrales_alerta["Taller PV1"] = u_pv1
            st.session_state.umbrales_alerta["Taller Lote Comercial"] = u_lc
            st.session_state.umbrales_alerta["Taller Lote Carguero"] = u_lcr
            save_data() # Guardar cambios
            st.success("Umbrales actualizados exitosamente.")
    else:
        st.info("Solo el Supervisor de Mantenimiento o Administrador pueden configurar umbrales.")

    st.divider()
    st.subheader("2. Estado Actual de Alertas (CU-07)")
    for taller, umbral in st.session_state.umbrales_alerta.items():
        libres = sum(1 for b in st.session_state.bahias if b["taller"] == taller and b["estado"] == "Libre")
        total = sum(1 for b in st.session_state.bahias if b["taller"] == taller)
        if libres <= umbral:
            st.error(f"🚨 **ALERTA CRÍTICA EN {taller.upper()}** — Bahías libres: {libres}/{total} (Umbral: <= {umbral})")
        else:
            st.success(f"✅ **{taller}:** Capacidad adecuada ({libres}/{total} bahías libres)")

# -------------------------------------------------------------
# 7. REPORTE HISTÓRICO DE OCUPACIÓN (CU-08)
# -------------------------------------------------------------
elif menu == "📈 Reporte de Ocupación (CU-08)":
    st.markdown("""
    <div style='border-left: 6px solid #012b6c; padding-left: 15px; margin-bottom: 20px;'>
        <h2 style='margin:0; color:#012b6c;'>Reporte Histórico de Ocupación de Bahías</h2>
        <span style='color:#555;'>Trazabilidad de movimientos para CCO y Jefatura GSE</span>
    </div>
    """, unsafe_allow_html=True)

    df_hist = pd.DataFrame(st.session_state.historial)
    st.dataframe(df_hist, use_container_width=True)

    csv_data = df_hist.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Descargar Reporte (.CSV)",
        data=csv_data,
        file_name="reporte_ocupacion_talma_smartbay.csv",
        mime="text/csv",
        type="primary"
    )

# -------------------------------------------------------------
# 8. GESTIÓN DE USUARIOS Y ROLES (CU-09)
# -------------------------------------------------------------
elif menu == "👥 Gestión de Usuarios (CU-09)":
    st.markdown("""
    <div style='border-left: 6px solid #012b6c; padding-left: 15px; margin-bottom: 20px;'>
        <h2 style='margin:0; color:#012b6c;'>Gestión de Usuarios y Roles de Acceso</h2>
        <span style='color:#555;'>Módulo restringido para el Administrador del Sistema</span>
    </div>
    """, unsafe_allow_html=True)

    if usuario_act["rol"] != "Administrador del Sistema":
        st.warning("⚠️ Acceso restringido exclusivamente para el Administrador del Sistema.")
        st.stop()

    col_u1, col_u2 = st.columns([1, 1])
    with col_u1:
        st.subheader("Registrar Nuevo Usuario")
        nuevo_user = st.text_input("Nombre de Usuario (Login)")
        nuevo_nom = st.text_input("Nombre Completo")
        nuevo_rol = st.selectbox("Rol Asignado", [
            "Supervisor de Mantenimiento", 
            "Planificador CCO", 
            "Técnico de Mantenimiento", 
            "Coordinador CCO Operaciones",
            "Administrador del Sistema"
        ])
        nuevo_pass = st.text_input("Contraseña Temporal", type="password")

        if st.button("Crear Usuario", type="primary"):
            if nuevo_user and nuevo_nom and nuevo_pass:
                if nuevo_user in st.session_state.usuarios:
                    st.error("El usuario ya se encuentra registrado.")
                else:
                    st.session_state.usuarios[nuevo_user] = {
                        "nombre": nuevo_nom,
                        "rol": nuevo_rol,
                        "pass": nuevo_pass
                    }
                    save_data() # Guardar cambios
                    st.success(f"Usuario {nuevo_user} registrado correctamente.")
                    st.rerun()
            else:
                st.error("Complete todos los campos obligatorios.")

    with col_u2:
        st.subheader("Usuarios Activos en el Sistema")
        tabla_users = [{"Usuario": k, "Nombre": v["nombre"], "Rol": v["rol"]} for k, v in st.session_state.usuarios.items()]
        st.table(pd.DataFrame(tabla_users))


