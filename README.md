# Smart Bay Manager — Sistema de Gestión Inteligente de Bahías GSE

> Solución integral para la asignación, monitoreo en tiempo real y trazabilidad operativa de bahías de mantenimiento de equipos Ground Support Equipment (GSE) en Talma Servicios Aeroportuarios S.A.

---

## Contexto y Problemática

En las operaciones aeroportuarias de Talma, el mantenimiento preventivo y correctivo de los equipos de apoyo terrestre (GSE) se distribuye en tres talleres especializados:
- Taller PV1
- Taller Lote Comercial
- Taller Lote Carguero

Históricamente, el seguimiento de la ocupación y disponibilidad de las bahías físicas se gestionaba mediante hojas de cálculo independientes y control manual. Esto ocasionaba demoras en la derivación de equipos, registros duplicados e inconsistentes sobre el estado de cada espacio, y falta de anticipación ante situaciones de saturación en la capacidad de los talleres.

Smart Bay Manager automatiza la gobernanza operativa del patio de mantenimiento mediante un panel de control interactivo con validación estricta de reglas de negocio y trazabilidad en tiempo real.

---

## Arquitectura y Casos de Uso del Sistema

El sistema implementa de forma íntegra los requerimientos funcionales derivados del análisis RUP y UML:

| Código | Caso de Uso | Rol Autorizado |
| :--- | :--- | :--- |
| CU-01 | Iniciar Sesión (Control de Acceso basado en Roles) | Planificador CCO, Supervisor, Técnico, Coordinador CCO, Administrador |
| CU-02 | Consultar Disponibilidad de Bahías en Tiempo Real | Planificador CCO, Supervisor de Mantenimiento |
| CU-03 | Asignar Bahía a Equipo (con validación de compatibilidad) | Supervisor de Mantenimiento |
| CU-04 | Configurar Umbral de Alerta de Capacidad | Supervisor de Mantenimiento |
| CU-05 | Registrar Ingreso Físico de Equipo en Bahía | Técnico de Mantenimiento |
| CU-06 | Registrar Salida de Equipo / Liberar Bahía | Técnico de Mantenimiento |
| CU-07 | Visualizar Alertas Tempranas de Saturación | Planificador CCO, Supervisor, Coordinador CCO |
| CU-08 | Generar Reporte Histórico de Ocupación (.CSV) | Planificador CCO, Coordinador CCO Operaciones |
| CU-09 | Gestionar Usuarios y Roles del Sistema | Administrador del Sistema |

---

## Reglas de Negocio Incorporadas

1. Restricción Estructural de Familias: Cada bahía física admite de manera exclusiva una familia de equipo compatible:
   - PM: Plataformas Móviles
   - LO: Loaders de Carga
   - CA/CB: Fajas y Cintas Transportadoras
   - TR: Tractores de Remolque
2. Restricción de Operación: Asignar un equipo a una bahía termina exitosamente únicamente si la bahía se encuentra en estado Libre y su familia es compatible con la del equipo a ingresar.
3. Regla de Estímulo y Respuesta (Alerta de Capacidad): Cuando el total de bahías libres de un taller sea menor o igual al umbral fijado, el sistema dispara automáticamente una alerta crítica para prevenir demoras en la operación de rampa.
4. Regla de Cálculo de Ocupación: El porcentaje de ocupación se calcula dividiendo el total de bahías ocupadas entre el total de bahías del taller y multiplicándolo por cien.

---

## Stack Tecnológico

- Lenguaje: Python 3.10+
- Framework Web: Streamlit
- Procesamiento de Datos: Pandas
- Identidad Visual: Paleta corporativa oficial de Talma (#012b6c Azul y #7ead3e Verde) con renderizado vectorial SVG nativo
- Despliegue: Streamlit Community Cloud (sincronizado mediante integración continua con GitHub)

---


🔗 Enlace de Acceso
(https://smart-bay-manager-talma.streamlit.app)



## Estructura del Repositorio

```text
smart-bay-manager/
├── .streamlit/
│   └── config.toml      # Configuración de tema visual y paleta oficial
├── app.py               # Lógica de negocio, interfaz interactiva y estado global
├── requirements.txt     # Dependencias de ejecución en la nube
└── README.md            # Documentación técnica del proyecto


Autor de Prototipo:

Rocio Isabel Davila Elias
