# Smart Bay Manager — Gestión Inteligente de Bahías GSE

> Asignación, monitoreo en tiempo real y trazabilidad operativa de bahías de mantenimiento Ground Support Equipment (GSE) para Talma Servicios Aeroportuarios S.A.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://davila-elias-isabel-smart-bay-manager-talma-app-cmisgb.streamlit.app/)

---

## 📌 Problemática y Solución

El mantenimiento preventivo y correctivo en los talleres **PV1**, **Lote Comercial** y **Lote Carguero** dependía de registros manuales y hojas de cálculo dispersas. Esto generaba demoras operativas, estados inconsistentes y falta de alertas ante saturación de capacidad.

**Smart Bay Manager** centraliza la gobernanza del patio de mantenimiento mediante un panel de control con validación estricta de compatibilidad, cálculo dinámico de ocupación y alertas automáticas de saturación en rampa.

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.10+
* **Framework Web:** Streamlit
* **Procesamiento de Datos:** Pandas
* **Diseño / UI:** Paleta corporativa de Talma (`#012b6c` / `#7ead3e`) con renderizado SVG
* **Despliegue:** Streamlit Community Cloud (CI/CD vía GitHub)

---

## 🏗️ Arquitectura del Sistema

Implementación modular en capas dentro de `app.py`:

| Capa | Responsabilidad | Funciones Clave |
| :--- | :--- | :--- |
| **Persistencia** | Entrada/salida y persistencia de datos | `load_data()`, `save_data()` |
| **Lógica de Negocio** | Validaciones, cálculos y reglas operativas | `validar_asignacion()`, `calcular_ocupacion()`, `evaluar_alerta_capacidad()` |
| **Servicios** | Orquestación de casos de uso | `servicio_asignar_bahia()`, `servicio_liberar_bahia()` |
| **Presentación (UI)** | Vistas y paneles interactivos en Streamlit | `pantalla_login()`, `pantalla_panel_disponibilidad()` |
| **Enrutador** | Control de acceso y navegación por roles | `main()` |

---

## ⚙️ Reglas de Negocio Clave

* **Compatibilidad Estructural:** Restricción estricta por familia de equipo:
  * `PM`: Plataformas Móviles
  * `LO`: Loaders de Carga
  * `CA/CB`: Fajas y Cintas Transportadoras
  * `TR`: Tractores de Remolque
* **Transición de Estado:** La asignación únicamente procede si la bahía está **Libre** y coincide con la familia técnica del equipo.
* **Alertas Tempranas:** Notificación crítica automática cuando las bahías libres del taller sean menores o iguales al umbral configurado.
* **Cálculo de Ocupación:** 
  $$\text{Ocupación (\%)} = \left( \frac{\text{Bahías Ocupadas}}{\text{Total Bahías del Taller}} \right) \times 100$$

---

## 📋 Casos de Uso (RBAC)

| Código | Caso de Uso | Roles con Acceso |
| :---: | :--- | :--- |
| **CU-01** | Inicio de sesión seguro | Todos los roles |
| **CU-02** | Consulta de disponibilidad en tiempo real | Planificador CCO, Supervisor |
| **CU-03** | Asignación con validación de compatibilidad | Supervisor de Mantenimiento |
| **CU-04** | Configuración de umbrales de saturación | Supervisor de Mantenimiento |
| **CU-05** | Registro de ingreso físico a bahía | Técnico de Mantenimiento |
| **CU-06** | Registro de salida y liberación de bahía | Técnico de Mantenimiento |
| **CU-07** | Monitoreo de alertas tempranas de capacidad | Planificador CCO, Supervisor, Coordinador |
| **CU-08** | Exportación de reportería histórica (`.csv`) | Planificador CCO, Coordinador |
| **CU-09** | Gestión de usuarios y permisos | Administrador del Sistema |

---

## 📂 Estructura del Repositorio

```text
smart-bay-manager-talma/
├── .streamlit/
│   └── config.toml      # Configuración visual y paleta oficial
├── app.py               # Aplicación completa: capas de negocio + UI
├── requirements.txt     # Dependencias de ejecución
└── README.md


Seguridad: Las credenciales de acceso se gestionan de forma aislada mediante st.secrets (secrets.toml en local o secrets en Streamlit Cloud), evitando su exposición en el repositorio.

👥 Equipo y Créditos
Universidad San Ignacio de Loyola — 2026

Carrera: Ingeniería Empresarial y de Sistemas

Jose Alexander Rojas Gutierrez

Rocio Isabel Davila Elias

Jose Christofer Arown Miranda Gallegos

Johaira Kihara Cabello Manrique

Ruth Noelia Huarhuache Sanchez

Desarrollo y Despliegue:

Implementación web en Streamlit, arquitectura modular, diseño UI y puesta en producción a cargo de Rocio Isabel Davila Elias.

📚 Referencias Bibliográficas
Jacobson, I., Booch, G., & Rumbaugh, J. (1999). The Unified Software Development Process. Addison-Wesley.

Kruchten, P. (2003). The Rational Unified Process: An Introduction (3.ª ed.). Addison-Wesley.

Larman, C. (2004). Applying UML and Patterns (3.ª ed.). Prentice Hall.

Object Management Group. (2017). Unified Modeling Language (UML) Specification, Version 2.5.1.
