# =====================================================================
# SMART BAY MANAGER — TALMA SERVICIOS AEROPORTUARIOS
# Arquitectura en Capas (Presentación, Servicios, Dominio, Datos)
# Interfaz alineada al Prototipo Navegable (Figura 18)
# =====================================================================

# ---------------------------------------------------------------------
# 0. IMPORTACIONES Y CONFIGURACIÓN INICIAL
# ---------------------------------------------------------------------
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os

st.set_page_config(
    page_title="Smart Bay Manager | Talma",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# CAPA DE DATOS / PERSISTENCIA (Repositories)
# =====================================================================
DATA_FILE = "smart_bay_data.json"

def load_data():
    """Carga los datos desde el archivo JSON (Repositorio)."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            st.session_state.bahias = data.get("bahias", st.session_state.bahias)
            st.session_state.equipos_pendientes = data.get("equipos_pendientes", st.session_state.equipos_pendientes)
            st.session_state.historial = data.get("historial", st.session_state.historial)
            st.session_state.umbrales_alerta = data.get("umbrales_alerta", st.session_state.umbrales_alerta)

def save_data():
    """Guarda los datos actuales en el archivo JSON (Repositorio)."""
    data = {
        "bahias": st.session_state.bahias,
        "equipos_pendientes": st.session_state.equipos_pendientes,
        "historial": st.session_state.historial,
        "umbrales_alerta": st.session_state.umbrales_alerta
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# =====================================================================
# CAPA DE DOMINIO / LÓGICA DE NEGOCIO (Domain)
# =====================================================================
def validar_asignacion(bahia, equipo):
    """Regla de Negocio: La bahía debe estar libre y ser compatible."""
    if bahia["estado"] != "Libre":
        return False, f"La bahía {bahia['id']} no está libre."
    if bahia["familia"] != equipo["familia"]:
        return False, f"Familia incompatible: equipo {equipo['familia']} vs bahía {bahia['familia']}."
    return True, "Validación exitosa."

def calcular_ocupacion(bahias, taller=None):
    """Regla de Cálculo: (bahías ocupadas / total) * 100."""
    if taller:
        bahias = [b for b in bahias if b["taller"] == taller]
    total = len(bahias)
    if total == 0:
        return 0
    ocupadas = sum(1 for b in bahias if b["estado"] == "Ocupada")
    return (ocupadas / total) * 100

def evaluar_alerta_capacidad(taller, bahias, umbral):
    """Regla de Estímulo y Respuesta: alerta si libres <= umbral."""
    libres = sum(1 for b in bahias if b["taller"] == taller and b["estado"] == "Libre")
    total = sum(1 for b in bahias if b["taller"] == taller)
    if libres <= umbral:
        return True, libres, total
    return False, libres, total

# =====================================================================
# CAPA DE APLICACIÓN / SERVICIOS (Services)
# =====================================================================
def servicio_asignar_bahia(equipo_codigo, bahia_id, usuario):
    """Orquesta la asignación de una bahía a un equipo."""
    equipo = next((e for e in st.session_state.equipos_pendientes if e["codigo"] == equipo_codigo), None)
    bahia = next((b for b in st.session_state.bahias if b["id"] == bahia_id), None)
    
    if not equipo or not bahia:
        return False, "Equipo o bahía no encontrados."
    
    valido, mensaje = validar_asignacion(bahia, equipo)
    if not valido:
        return False, mensaje
    
    bahia["estado"] = "Ocupada"
    bahia["equipo"] = equipo["codigo"]
    bahia["ingreso"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    st.session_state.equipos_pendientes = [
        e for e in st.session_state.equipos_pendientes if e["codigo"] != equipo_codigo
    ]
    
    st.session_state.historial.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "evento": "Asignación e Ingreso",
        "bahia": bahia_id,
        "equipo": equipo_codigo,
        "taller": bahia["taller"],
        "usuario": usuario
    })
    
    save_data()
    return True, f"Equipo {equipo_codigo} asignado a la bahía {bahia_id}."

def servicio_liberar_bahia(bahia_id, usuario):
    """Orquesta la liberación de una bahía."""
    bahia = next((b for b in st.session_state.bahias if b["id"] == bahia_id), None)
    if not bahia or bahia["estado"] != "Ocupada":
        return False, "La bahía no está ocupada."
    
    equipo_salida = bahia["equipo"]
    bahia["estado"] = "Libre"
    bahia["equipo"] = None
    bahia["ingreso"] = None
    
    st.session_state.historial.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "evento": "Salida / Liberación",
        "bahia": bahia_id,
        "equipo": equipo_salida,
        "taller": bahia["taller"],
        "usuario": usuario
    })
    
    save_data()
    return True, f"Bahía {bahia_id} liberada."

# =====================================================================
# CAPA DE PRESENTACIÓN (UI - Streamlit)
# =====================================================================

def cargar_estilos():
    st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #012b6c;
            font-weight: 700;
            margin-bottom: 25px;
        }
        .prototype-header {
            background-color: #012b6c;
            color: white;
            padding: 8px 15px;
            border-radius: 4px 4px 0 0;
            font-weight: 600;
            margin-bottom: 0;
        }
        .prototype-body {
            border: 1px solid #e2e8f0;
            border-top: none;
            border-radius: 0 0 4px 4px;
            padding: 20px;
            background-color: #ffffff;
        }
        .alert-text {
            color: #dc2626;
            font-weight: 600;
            font-size: 0.9rem;
        }
        div.stButton > button {
            border-radius: 4px;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)

LOGO_TALMA_HTML = """
<div style="text-align: center; padding: 15px 0 10px 0;">
    <svg width="220" height="75" viewBox="0 0 320 110" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M72 16 L110 16 L104 35 L66 35 Z" fill="#7ead3e"/>
        <text x="32" y="78" font-family="'Arial Black', Impact, sans-serif" font-weight="900" font-size="64" fill="#ffffff" font-style="italic">Talma</text>
        <text x="32" y="98" font-family="Arial, Helvetica, sans-serif" font-size="13.5" font-weight="bold" fill="#7ead3e" letter-spacing="1.3">LÍDER EN SERVICIOS AEROPORTUARIOS</text>
    </svg>
</div>
"""

def inicializar_estado():
    if "usuarios" not in st.session_state:
        st.session_state.usuarios = {
            "supervisor": {"nombre": "Carlos Mendoza", "rol": "Supervisor de Mantenimiento", "pass": st.secrets["passwords"]["supervisor"]},
            "planificador": {"nombre": "Ana Ramos", "rol": "Planificador CCO", "pass": st.secrets["passwords"]["planificador"]},
            "tecnico": {"nombre": "Jorge Salinas", "rol": "Técnico de Mantenimiento", "pass": st.secrets["passwords"]["tecnico"]},
            "coordinador": {"nombre": "Luis Paredes", "rol": "Coordinador CCO Operaciones", "pass": st.secrets["passwords"]["coordinador"]},
            "admin": {"nombre": "Admin General", "rol": "Administrador del Sistema", "pass": st.secrets["passwords"]["admin"]}
        }
    if "sesion_activa" not in st.session_state:
        st.session_state.sesion_activa = None
    if "umbrales_alerta" not in st.session_state:
        st.session_state.umbrales_alerta = {"Taller PV1": 2, "Taller Lote Comercial": 1, "Taller Lote Carguero": 1}
    if "bahias" not in st.session_state:
        st.session_state.bahias = [
            {"id": "B-101", "taller": "PV1", "familia": "PM", "estado": "Libre", "equipo": None, "ingreso": None},
            {"id": "B-102", "taller": "PV1", "familia": "LO", "estado": "Ocupada", "equipo": "LO-204", "ingreso": "2026-09-11 08:30"},
            {"id": "B-201", "taller": "L. Comercial", "familia": "CA/CB", "estado": "Libre", "equipo": None, "ingreso": None},
            {"id": "B-202", "taller": "L. Comercial", "familia": "PM", "estado": "Ocupada", "equipo": "PM-101", "ingreso": "2026-09-11 09:15"},
            {"id": "B-301", "taller": "L. Carguero", "familia": "TR", "estado": "Libre", "equipo": None, "ingreso": None},
            {"id": "B-302", "taller": "L. Carguero", "familia": "CA/CB", "estado": "Ocupada", "equipo": "CB-305", "ingreso": "2026-09-11 07:45"}
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
            {"timestamp": "2026-09-11 08:30", "evento": "Ingreso Equipo", "bahia": "B-102", "equipo": "LO-204", "taller": "PV1", "usuario": "Jorge Salinas"},
            {"timestamp": "2026-09-11 09:15", "evento": "Ingreso Equipo", "bahia": "B-202", "equipo": "PM-101", "taller": "L. Comercial", "usuario": "Jorge Salinas"},
            {"timestamp": "2026-09-11 07:45", "evento": "Ingreso Equipo", "bahia": "B-302", "equipo": "CB-305", "taller": "L. Carguero", "usuario": "Jorge Salinas"}
        ]

# --- PANTALLAS (Casos de Uso) ---

def pantalla_login():
    """CU-01: Iniciar Sesión - Prototipo Figura 18"""
    st.markdown("<h1 class='main-title'>Smart Bay Manager</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<h3 style='text-align:center;'>Iniciar Sesión</h3>", unsafe_allow_html=True)
        username = st.text_input("Usuario", placeholder="Ingrese su usuario")
        password = st.text_input("Contraseña", type="password", placeholder="Ingrese su contraseña")
        
        if st.button("Ingresar", type="primary", use_container_width=True):
            if username in st.session_state.usuarios:
                user_data = st.session_state.usuarios[username]
                if password == user_data["pass"]:
                    st.session_state.sesion_activa = {
                        "username": username,
                        "nombre": user_data["nombre"],
                        "rol": user_data["rol"]
                    }
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta")
            else:
                st.error("Usuario no encontrado")

def pantalla_panel_disponibilidad(usuario_act):
    """CU-02: Panel de Disponibilidad - Prototipo Figura 18"""
    st.markdown("<h2 class='main-title'>Panel de Disponibilidad</h2>", unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
    with col_f1:
        f_taller = st.selectbox("Taller", ["Todos", "PV1", "L. Comercial", "L. Carguero"])
    with col_f2:
        f_familia = st.selectbox("Familia", ["Todas", "PM", "LO", "CA/CB", "TR"])
    with col_f3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Consultar", type="primary", use_container_width=True):
            pass

    bahias_filtradas = st.session_state.bahias
    if f_taller != "Todos":
        bahias_filtradas = [b for b in bahias_filtradas if b["taller"] == f_taller]
    if f_familia != "Todas":
        bahias_filtradas = [b for b in bahias_filtradas if b["familia"] == f_familia]

    if bahias_filtradas:
        df = pd.DataFrame(bahias_filtradas)[["id", "taller", "familia", "estado"]]
        df.columns = ["Bahía", "Taller", "Familia", "Estado"]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No hay bahías que coincidan con los filtros seleccionados.")

def pantalla_asignar_bahia(usuario_act):
    """CU-03: Asignar Bahía a Equipo - Prototipo Figura 18"""
    st.markdown("<h2 class='main-title'>Asignar Bahía a Equipo</h2>", unsafe_allow_html=True)

    if usuario_act["rol"] not in ["Supervisor de Mantenimiento", "Administrador del Sistema"]:
        st.warning("Acceso reservado para el Supervisor de Mantenimiento.")
        st.stop()

    if not st.session_state.equipos_pendientes:
        st.success("No existen equipos pendientes en cola.")
        return

    opciones_eq = {f"{eq['codigo']} ({eq['tipo']})": eq for eq in st.session_state.equipos_pendientes}
    seleccion_eq_label = st.selectbox("Equipo GSE", list(opciones_eq.keys()))
    eq_sel = opciones_eq[seleccion_eq_label]

    st.markdown("**Bahías compatibles y libres:**")
    compatibles = [b for b in st.session_state.bahias if b["estado"] == "Libre" and b["familia"] == eq_sel["familia"]]

    if not compatibles:
        st.error(f"No hay bahías disponibles para la familia {eq_sel['familia']}.")
    else:
        df_comp = pd.DataFrame(compatibles)[["id", "taller"]]
        df_comp.columns = ["Bahía", "Taller"]
        st.dataframe(df_comp, use_container_width=True, hide_index=True)

        opciones_b = {f"{b['id']} — {b['taller']}": b for b in compatibles}
        sel_b_label = st.selectbox("Seleccione Bahía", list(opciones_b.keys()))
        b_sel = opciones_b[sel_b_label]

        if st.button("Confirmar Asignación", type="primary", use_container_width=True):
            exito, mensaje = servicio_asignar_bahia(eq_sel["codigo"], b_sel["id"], usuario_act["nombre"])
            if exito:
                st.success(mensaje)
                st.rerun()
            else:
                st.error(mensaje)

def pantalla_terminal_taller(usuario_act):
    """CU-05 / CU-06: Registro de Ingreso / Salida - Prototipo Figura 18"""
    st.markdown("<h2 class='main-title'>Registro de Ingreso / Salida</h2>", unsafe_allow_html=True)

    buscar = st.text_input("Buscar equipo / escanear código", placeholder="Ej: LO-204")

    if buscar:
        bahia_encontrada = next((b for b in st.session_state.bahias if b["equipo"] == buscar), None)
        
        if bahia_encontrada:
            st.markdown(f"**Equipo:** {bahia_encontrada['equipo']} → **Bahía:** {bahia_encontrada['id']}")
            st.markdown(f"**Hora ingreso:** {bahia_encontrada['ingreso']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Reg. Ingreso", type="primary", use_container_width=True):
                    st.info("El equipo ya se encuentra registrado en la bahía.")
            with col2:
                if st.button("Reg. Salida", type="secondary", use_container_width=True):
                    exito, mensaje = servicio_liberar_bahia(bahia_encontrada["id"], usuario_act["nombre"])
                    if exito:
                        st.success(mensaje)
                        st.rerun()
                    else:
                        st.error(mensaje)
        else:
            bahia_libre = next((b for b in st.session_state.bahias if b["estado"] == "Libre"), None)
            if bahia_libre:
                st.markdown(f"**Equipo:** {buscar} → **Bahía:** {bahia_libre['id']} (disponible)")
                st.markdown("**Hora ingreso:** --:--")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Reg. Ingreso", type="primary", use_container_width=True):
                        bahia_libre["estado"] = "Ocupada"
                        bahia_libre["equipo"] = buscar
                        bahia_libre["ingreso"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        save_data()
                        st.success(f"Ingreso registrado para {buscar} en {bahia_libre['id']}.")
                        st.rerun()
                with col2:
                    if st.button("Reg. Salida", type="secondary", use_container_width=True):
                        st.warning("El equipo no tiene un ingreso registrado.")
            else:
                st.error("No hay bahías libres disponibles.")

def pantalla_alertas_umbrales(usuario_act):
    """CU-04 / CU-07: Alertas y Umbrales - Prototipo Figura 18"""
    st.markdown("<h2 class='main-title'>Alertas de Capacidad</h2>", unsafe_allow_html=True)

    datos_alertas = []
    for taller, umbral in st.session_state.umbrales_alerta.items():
        alerta, libres, total = evaluar_alerta_capacidad(taller, st.session_state.bahias, umbral)
        datos_alertas.append({"Taller": taller, "Libres": libres, "Umbral": umbral, "Alerta": alerta})

    df_alertas = pd.DataFrame(datos_alertas)[["Taller", "Libres", "Umbral"]]
    st.dataframe(df_alertas, use_container_width=True, hide_index=True)

    num_alertas = sum(1 for d in datos_alertas if d["Alerta"])
    if num_alertas > 0:
        st.markdown(f"<p class='alert-text'>⚠ {num_alertas} alertas activas requieren atención</p>", unsafe_allow_html=True)
    else:
        st.success("No hay alertas activas en este momento.")

    st.divider()
    st.markdown("<h3 style='text-align:center;'>Configurar Umbral de Alerta</h3>", unsafe_allow_html=True)

    if usuario_act["rol"] in ["Supervisor de Mantenimiento", "Administrador del Sistema"]:
        taller_sel = st.selectbox("Taller", list(st.session_state.umbrales_alerta.keys()))
        umbral_actual = st.session_state.umbrales_alerta[taller_sel]
        st.text_input("Umbral actual", value=str(umbral_actual), disabled=True)
        nuevo_umbral = st.number_input("Nuevo umbral", min_value=0, max_value=5, value=umbral_actual, step=1)

        if st.button("Guardar", type="primary", use_container_width=True):
            st.session_state.umbrales_alerta[taller_sel] = nuevo_umbral
            save_data()
            st.success(f"Umbral de {taller_sel} actualizado a {nuevo_umbral}.")
            st.rerun()
    else:
        st.info("Solo el Supervisor de Mantenimiento puede configurar umbrales.")

def pantalla_reporte_ocupacion(usuario_act):
    """CU-08: Reporte de Ocupación - Prototipo Figura 18"""
    st.markdown("<h2 class='main-title'>Reporte de Ocupación</h2>", unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns([1, 1, 1])
    with col_f1:
        f_taller = st.selectbox("Taller", ["Todos", "PV1", "L. Comercial", "L. Carguero"])
    with col_f2:
        f_fecha = st.date_input("Rango fechas", value=datetime.now().date())
    with col_f3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Generar Reporte", type="primary", use_container_width=True):
            pass

    df_hist = pd.DataFrame(st.session_state.historial)
    if not df_hist.empty:
        df_hist = df_hist[["timestamp", "bahia"]]
        df_hist.columns = ["Fecha", "Bahía"]
        st.dataframe(df_hist, use_container_width=True, hide_index=True)

    csv_data = df_hist.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Exportar a Excel",
        data=csv_data,
        file_name="reporte_ocupacion_talma.csv",
        mime="text/csv",
        type="primary",
        use_container_width=True
    )

def pantalla_gestion_usuarios(usuario_act):
    """CU-09: Gestión de Usuarios - Prototipo Figura 18"""
    st.markdown("<h2 class='main-title'>Gestión de Usuarios y Roles</h2>", unsafe_allow_html=True)

    if usuario_act["rol"] != "Administrador del Sistema":
        st.warning("Acceso restringido al Administrador del Sistema.")
        st.stop()

    tabla_users = [{"Usuario": k, "Rol": v["rol"]} for k, v in st.session_state.usuarios.items()]
    df_users = pd.DataFrame(tabla_users)
    st.dataframe(df_users, use_container_width=True, hide_index=True)

    with st.expander("Nuevo Usuario"):
        nuevo_user = st.text_input("Nombre de Usuario (Login)")
        nuevo_nom = st.text_input("Nombre Completo")
        nuevo_rol = st.selectbox("Rol Asignado", [
            "Supervisor de Mantenimiento", "Planificador CCO", "Técnico de Mantenimiento",
            "Coordinador CCO Operaciones", "Administrador del Sistema"
        ])
        nuevo_pass = st.text_input("Contraseña Temporal", type="password")

        if st.button("Crear Usuario", type="primary"):
            if nuevo_user and nuevo_nom and nuevo_pass:
                if nuevo_user in st.session_state.usuarios:
                    st.error("El usuario ya existe.")
                else:
                    st.session_state.usuarios[nuevo_user] = {"nombre": nuevo_nom, "rol": nuevo_rol, "pass": nuevo_pass}
                    save_data()
                    st.success(f"Usuario {nuevo_user} registrado.")
                    st.rerun()
            else:
                st.error("Complete todos los campos.")

# =====================================================================
# ENRUTADOR PRINCIPAL (Main)
# =====================================================================
def main():
    cargar_estilos()
    inicializar_estado()
    load_data()

    st.sidebar.markdown(LOGO_TALMA_HTML, unsafe_allow_html=True)
    st.sidebar.markdown("<h3 style='text-align:center; margin-top:-5px;'>Smart Bay Manager</h3>", unsafe_allow_html=True)

    if not st.session_state.sesion_activa:
        pantalla_login()
        st.stop()

    usuario_act = st.session_state.sesion_activa
    st.sidebar.markdown(f"**Usuario:** {usuario_act['nombre']}")
    st.sidebar.markdown(f"**Rol:** `{usuario_act['rol']}`")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.sesion_activa = None
        st.rerun()

    st.sidebar.divider()
    menu = st.sidebar.radio(
        "Módulos del Sistema",
        ["Panel de Disponibilidad (CU-02)",
         "Asignar Bahía a Equipo (CU-03)",
         "Registro de Ingreso / Salida (CU-05 / CU-06)",
         "Alertas y Umbrales (CU-04 / CU-07)",
         "Reporte de Ocupación (CU-08)",
         "Gestión de Usuarios (CU-09)"]
    )

    if menu == "Panel de Disponibilidad (CU-02)":
        pantalla_panel_disponibilidad(usuario_act)
    elif menu == "Asignar Bahía a Equipo (CU-03)":
        pantalla_asignar_bahia(usuario_act)
    elif menu == "Registro de Ingreso / Salida (CU-05 / CU-06)":
        pantalla_terminal_taller(usuario_act)
    elif menu == "Alertas y Umbrales (CU-04 / CU-07)":
        pantalla_alertas_umbrales(usuario_act)
    elif menu == "Reporte de Ocupación (CU-08)":
        pantalla_reporte_ocupacion(usuario_act)
    elif menu == "Gestión de Usuarios (CU-09)":
        pantalla_gestion_usuarios(usuario_act)

if __name__ == "__main__":
    main()
