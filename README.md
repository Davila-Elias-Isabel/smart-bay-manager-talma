# Smart Bay Manager — Sistema de Gestión Inteligente de Bahías GSE

> Solución integral para la asignación, monitoreo en tiempo real y trazabilidad operativa de bahías de mantenimiento de equipos Ground Support Equipment (GSE) en Talma Servicios Aeroportuarios S.A.

---

## Contexto y Problemática

En las operaciones aeroportuarias de Talma, el mantenimiento preventivo y correctivo de los equipos de apoyo terrestre (GSE) se distribuye en tres talleres especializados: Taller PV1, Taller Lote Comercial y Taller Lote Carguero.

Históricamente, el seguimiento de la ocupación y disponibilidad de las bahías físicas se gestionaba mediante hojas de cálculo independientes y control manual. Esto ocasionaba demoras en la derivación de equipos, registros duplicados e inconsistentes sobre el estado de cada espacio, y falta de anticipación ante situaciones de saturación en la capacidad de los talleres.

**Smart Bay Manager** automatiza la gobernanza operativa del patio de mantenimiento mediante un panel de control interactivo con validación estricta de reglas de negocio y trazabilidad en tiempo real.

---

## Arquitectura del Sistema

El proyecto está implementado siguiendo una **arquitectura en capas**, lo que permite separar responsabilidades y facilitar el mantenimiento y la escalabilidad.

| Capa | Responsabilidad | Implementación en `app.py` |
| :--- | :--- | :--- |
| **Datos / Persistencia** | Carga y guardado de información | `load_data()`, `save_data()` |
| **Dominio / Lógica de Negocio** | Reglas de negocio y cálculos | `validar_asignacion()`, `calcular_ocupacion()`, `evaluar_alerta_capacidad()` |
| **Aplicación / Servicios** | Orquestación de casos de uso | `servicio_asignar_bahia()`, `servicio_liberar_bahia()` |
| **Presentación (UI)** | Interfaz de usuario en Streamlit | `pantalla_login()`, `pantalla_panel_disponibilidad()`, etc. |
| **Enrutador Principal** | Autenticación y navegación | `main()` |

---

## Casos de Uso Implementados

| Código | Caso de Uso | Roles con Acceso | Estado |
| :--- | :--- | :--- | :--- |
| CU-01 | Inicio de sesión seguro | Todos los roles | ✅ Implementado |
| CU-02 | Consulta de disponibilidad en tiempo real | Planificador CCO, Supervisor | ✅ Implementado |
| CU-03 | Asignación con validación de compatibilidad | Supervisor de Mantenimiento | ✅ Implementado |
| CU-04 | Configuración de umbrales de saturación | Supervisor de Mantenimiento | ✅ Implementado |
| CU-05 | Registro de ingreso físico a bahía | Técnico de Mantenimiento | ✅ Implementado |
| CU-06 | Registro de salida y liberación de bahía | Técnico de Mantenimiento | ✅ Implementado |
| CU-07 | Monitoreo de alertas tempranas de capacidad | Planificador CCO, Supervisor, Coordinador | ✅ Implementado |
| CU-08 | Exportación de reporte histórico (.csv) | Planificador CCO, Coordinador | ✅ Implementado |
| CU-09 | Gestión de usuarios y permisos | Administrador del Sistema | ✅ Implementado |

---

## Reglas de Negocio Incorporadas

1. **Restricción Estructural de Familias:** Cada bahía física admite de manera exclusiva una familia de equipo compatible: PM (Plataformas Móviles), LO (Loaders de Carga), CA/CB (Fajas y Cintas Transportadoras), TR (Tractores de Remolque).

2. **Restricción de Operación:** Asignar un equipo a una bahía termina exitosamente únicamente si la bahía se encuentra en estado **Libre** y su familia es **compatible** con la del equipo a ingresar.

3. **Regla de Estímulo y Respuesta (Alerta de Capacidad):** Cuando el total de bahías libres de un taller sea menor o igual al umbral fijado, el sistema dispara automáticamente una alerta crítica.

4. **Regla de Cálculo de Ocupación:** El porcentaje de ocupación se calcula como (Bahías Ocupadas / Total de Bahías del Taller) * 100.

---

## Estructura del Repositorio

La estructura del proyecto es la siguiente:

- **.streamlit/config.toml** — Configuración de tema visual y paleta oficial.
- **app.py** — Aplicación completa: arquitectura en capas + UI.
- **requirements.txt** — Dependencias de ejecución en la nube.
- **README.md** — Documentación técnica del proyecto.

**Nota:** Las credenciales de los usuarios se cargan de forma segura desde `st.secrets` (archivo `secrets.toml` local o configuración en Streamlit Cloud), por lo que **no están expuestas en el repositorio**.

---

## Interfaz de Usuario

La interfaz fue diseñada siguiendo los **prototipos navegables de la Figura 18** del Producto Acreditable:

- **Login:** Campos de usuario y contraseña centrados.
- **Panel de Disponibilidad:** Filtros por taller y familia, tabla con estado de bahías.
- **Asignar Bahía:** Selector de equipo, tabla de bahías compatibles y libres.
- **Registro de Ingreso / Salida:** Búsqueda por código de equipo, botones de acción.
- **Alertas y Umbrales:** Tabla de alertas, configuración de umbrales.
- **Reporte de Ocupación:** Filtros por taller y fecha, exportación a CSV.
- **Gestión de Usuarios:** Tabla de usuarios y roles, formulario de creación.

---

## Stack Tecnológico

- **Lenguaje:** Python 3.10+
- **Framework Web:** Streamlit
- **Procesamiento de Datos:** Pandas
- **Identidad Visual:** Paleta corporativa oficial de Talma (#012b6c Azul y #7ead3e Verde) con renderizado vectorial SVG nativo
- **Despliegue:** Streamlit Community Cloud (sincronizado mediante integración continua con GitHub)

---

## Enlace de Acceso

[https://davila-elias-isabel-smart-bay-manager-talma-app-cmisgb.streamlit.app/](https://davila-elias-isabel-smart-bay-manager-talma-app-cmisgb.streamlit.app/)

---

## Integrantes del Proyecto

| Nombre | Carrera |
| :--- | :--- |
| Jose Alexander Rojas Gutierrez | Ingeniería Empresarial y de Sistemas |
| Rocio Isabel Davila Elias | Ingeniería Empresarial y de Sistemas |
| Jose Christofer Arown Miranda Gallegos | Ingeniería Empresarial y de Sistemas |
| Johaira Kihara Cabello Manrique | Ingeniería Empresarial y de Sistemas |
| Ruth Noelia Huarhuache Sanchez | Ingeniería Empresarial y de Sistemas |

**Universidad San Ignacio de Loyola**
Lima — Perú, 2026

---

## Autoría de la Página Web

> La implementación de la aplicación web en Streamlit, el diseño de la interfaz alineada a los prototipos navegables (Figura 18), la refactorización del código en capas y el despliegue en Streamlit Community Cloud fueron realizados por:
>
> **Rocio Isabel Davila Elias**
> Carrera: Ingeniería Empresarial y de Sistemas
> Universidad San Ignacio de Loyola

---

## Referencias Bibliográficas

- Jacobson, I., Booch, G., & Rumbaugh, J. (1999). *The Unified Software Development Process*. Addison-Wesley.
- Kruchten, P. (2003). *The Rational Unified Process: An Introduction* (3.a ed.). Addison-Wesley.
- Object Management Group. (2017). *Unified Modeling Language (UML) Specification, Version 2.5.1*.
- Larman, C. (2004). *Applying UML and Patterns* (3.a ed.). Prentice Hall.
