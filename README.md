# Smart Bay Manager — Sistema de Gestión Inteligente de Bahías GSE

> Solución integral para la asignación, monitoreo en tiempo real y trazabilidad operativa de bahías de mantenimiento de equipos Ground Support Equipment (GSE) en **Talma Servicios Aeroportuarios S.A.**

---

## 📌 Contexto y Problemática

En las operaciones aeroportuarias de Talma, el mantenimiento preventivo y correctivo de los equipos de apoyo terrestre (GSE) se distribuye en tres talleres especializados:
* **Taller PV1**
* **Taller Lote Comercial**
* **Taller Lote Carguero**

Históricamente, el seguimiento de la ocupación y disponibilidad de las bahías físicas se gestionaba mediante hojas de cálculo independientes y control manual. Esto ocasionaba demoras en la derivación de equipos, registros duplicados e inconsistentes sobre el estado de cada espacio, y falta de anticipación ante cuellos de botella en la capacidad de los talleres.

**Smart Bay Manager** automatiza la gobernanza operativa del patio de mantenimiento mediante un panel de control interactivo con validación estricta de reglas de negocio y trazabilidad en tiempo real.

---

## 🚀 Arquitectura y Casos de Uso del Sistema

El sistema implementa de forma íntegra los requerimientos funcionales derivados del análisis RUP/UML:

| Código | Caso de Uso | Rol / Actor Autorizado |
| :--- | :--- | :--- |
| **CU-01** | Iniciar Sesión (Control de Acceso basado en Roles) | Planificador CCO, Supervisor, Técnico, Coordinador CCO, Administrador |
| **CU-02** | Consultar Disponibilidad de Bahías en Tiempo Real | Planificador CCO, Supervisor de Mantenimiento |
| **CU-03** | Asignar Bahía a Equipo (con validación de compatibilidad) | Supervisor de Mantenimiento |
| **CU-04** | Configurar Umbral de Alerta de Capacidad | Supervisor de Mantenimiento |
| **CU-05** | Registrar Ingreso Físico de Equipo en Bahía | Técnico de Mantenimiento |
| **CU-06** | Registrar Salida de Equipo / Liberar Bahía | Técnico de Mantenimiento |
| **CU-07** | Visualizar Alertas Tempranas de Saturación | Planificador CCO, Supervisor, Coordinador CCO |
| **CU-08** | Generar Reporte Histórico de Ocupación (.CSV) | Planificador CCO, Coordinador CCO Operaciones |
| **CU-09** | Gestionar Usuarios y Roles del Sistema | Administrador del Sistema |

---

## ⚙️ Reglas de Negocio Incorporadas

1. **Restricción Estructural de Familias:** Cada bahía física admite de manera exclusiva una familia de equipo compatible:
   * `PM`: Plataformas Móviles
   * `LO`: Loaders de Carga
   * `CA/CB`: Fajas y Cintas Transportadoras
   * `TR`: Tractores de Remolque
2. **Restricción de Operación:** Asignar un equipo a una bahía termina exitosamente únicamente si la bahía se encuentra en estado `Libre` y su familia es compatible con la del equipo a ingresar.
3. **Regla de Estímulo y Respuesta (Alerta de Capacidad):** Cuando el total de bahías libres de un taller sea menor o igual al umbral fijado, el sistema dispara automáticamente una alerta crítica para prevenir demoras en la operación de rampa.
4. **Regla de Cálculo de Ocupación:**
   $$\text{\% Ocupación} = \left( \frac{\text{Bahías Ocupadas}}{\text{Total Bahías del Taller}} \right) \times 100$$

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.10+
* **Framework Web:** Streamlit
* **Tratamiento de Datos:** Pandas
* **Identidad Visual:** Paleta corporativa oficial de Talma (`#012b6c` Azul / `#7ead3e` Verde) con renderizado vectorial SVG.
* **Infraestructura de Despliegue:** Streamlit Community Cloud (sincronizado mediante CI/CD directo con GitHub).

---

## 📦 Estructura del Repositorio

```text
smart-bay-manager/
├── .streamlit/
│   └── config.toml      # Configuración de tema visual y paleta oficial
├── app.py               # Lógica de negocio, interfaz interactiva y estado global
├── requirements.txt     # Dependencias de ejecución en la nube
└── README.md            # Documentación técnica del proyecto



📄 Autor


Rocío Isabel Dávila Elias



El archivo **`README.md`** es la carta de presentación técnica del repositorio en GitHub, permitiendo que el docente o evaluador comprenda de inmediato el sustento de ingeniería, el mapeo de casos de uso y la forma de probar la aplicación.

---

### Contenido para tu archivo `README.md`

Crea en la raíz del repositorio el archivo **`README.md`** y pega este contenido:

```markdown
# Smart Bay Manager — Sistema de Gestión Inteligente de Bahías GSE

> Solución integral para la asignación, monitoreo en tiempo real y trazabilidad operativa de bahías de mantenimiento de equipos Ground Support Equipment (GSE) en **Talma Servicios Aeroportuarios S.A.**

---

## 📌 Contexto y Problemática

En las operaciones aeroportuarias de Talma, el mantenimiento preventivo y correctivo de los equipos de apoyo terrestre (GSE) se distribuye en tres talleres especializados:
* **Taller PV1**
* **Taller Lote Comercial**
* **Taller Lote Carguero**

Históricamente, el seguimiento de la ocupación y disponibilidad de las bahías físicas se gestionaba mediante hojas de cálculo independientes y control manual. Esto ocasionaba demoras en la derivación de equipos, registros duplicados e inconsistentes sobre el estado de cada espacio, y falta de anticipación ante cuellos de botella en la capacidad de los talleres.

**Smart Bay Manager** automatiza la gobernanza operativa del patio de mantenimiento mediante un panel de control interactivo con validación estricta de reglas de negocio y trazabilidad en tiempo real.

---

## 🚀 Arquitectura y Casos de Uso del Sistema

El sistema implementa de forma íntegra los requerimientos funcionales derivados del análisis RUP/UML:

| Código | Caso de Uso | Rol / Actor Autorizado |
| :--- | :--- | :--- |
| **CU-01** | Iniciar Sesión (Control de Acceso basado en Roles) | Planificador CCO, Supervisor, Técnico, Coordinador CCO, Administrador |
| **CU-02** | Consultar Disponibilidad de Bahías en Tiempo Real | Planificador CCO, Supervisor de Mantenimiento |
| **CU-03** | Asignar Bahía a Equipo (con validación de compatibilidad) | Supervisor de Mantenimiento |
| **CU-04** | Configurar Umbral de Alerta de Capacidad | Supervisor de Mantenimiento |
| **CU-05** | Registrar Ingreso Físico de Equipo en Bahía | Técnico de Mantenimiento |
| **CU-06** | Registrar Salida de Equipo / Liberar Bahía | Técnico de Mantenimiento |
| **CU-07** | Visualizar Alertas Tempranas de Saturación | Planificador CCO, Supervisor, Coordinador CCO |
| **CU-08** | Generar Reporte Histórico de Ocupación (.CSV) | Planificador CCO, Coordinador CCO Operaciones |
| **CU-09** | Gestionar Usuarios y Roles del Sistema | Administrador del Sistema |

---

## ⚙️ Reglas de Negocio Incorporadas

1. **Restricción Estructural de Familias:** Cada bahía física admite de manera exclusiva una familia de equipo compatible:
   * `PM`: Plataformas Móviles
   * `LO`: Loaders de Carga
   * `CA/CB`: Fajas y Cintas Transportadoras
   * `TR`: Tractores de Remolque
2. **Restricción de Operación:** Asignar un equipo a una bahía termina exitosamente únicamente si la bahía se encuentra en estado `Libre` y su familia es compatible con la del equipo a ingresar.
3. **Regla de Estímulo y Respuesta (Alerta de Capacidad):** Cuando el total de bahías libres de un taller sea menor o igual al umbral fijado, el sistema dispara automáticamente una alerta crítica para prevenir demoras en la operación de rampa.
4. **Regla de Cálculo de Ocupación:**
   $$\text{\% Ocupación} = \left( \frac{\text{Bahías Ocupadas}}{\text{Total Bahías del Taller}} \right) \times 100$$

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.10+
* **Framework Web:** Streamlit
* **Tratamiento de Datos:** Pandas
* **Identidad Visual:** Paleta corporativa oficial de Talma (`#012b6c` Azul / `#7ead3e` Verde) con renderizado vectorial SVG.
* **Infraestructura de Despliegue:** Streamlit Community Cloud (sincronizado mediante CI/CD directo con GitHub).

---

## 📦 Estructura del Repositorio

```text
smart-bay-manager/
├── .streamlit/
│   └── config.toml      # Configuración de tema visual y paleta oficial
├── app.py               # Lógica de negocio, interfaz interactiva y estado global
├── requirements.txt     # Dependencias de ejecución en la nube
└── README.md            # Documentación técnica del proyecto

```

---

## 👥 Credenciales de Prueba Preconfiguradas

| Usuario | Contraseña | Rol Asignado | Alcance Principal |
| --- | --- | --- | --- |
| `supervisor` | `sup123` | Supervisor de Mantenimiento | Asignación y control de umbrales |
| `planificador` | `plan123` | Planificador CCO | Monitoreo general y reportes |
| `tecnico` | `tec123` | Técnico de Mantenimiento | Ingreso físico y liberación de bahías |
| `coordinador` | `coord123` | Coordinador CCO Operaciones | Supervisión de alertas de capacidad |
| `admin` | `admin123` | Administrador del Sistema | Creación y administración de cuentas |

---

## 📄 Autores

* José Alexander Rojas Gutierrez
* Rocío Isabel Dávila Elias
* José Crhistofer Arown Miranda Gallegos
* Johaira Kihara Cabello Manrique
* Ruth Noelia Huarhuache Sanchez

*Universidad San Ignacio de Loyola (USIL) — 2026*

```

---

### Explicación a detalle del proyecto: Cómo funciona y qué hace cada componente

**1. Persistencia y simulación concurrente (`st.session_state`):**
* Al ser un prototipo para entrega académica, el backend almacena los datos de las bahías, equipos en cola e historial en la memoria de la sesión activa del usuario[cite: 1, 2]. 
* Esto permite interactuar con la aplicación de forma dinámica (asignar, liberar o modificar umbrales) sin requerir todavía una base de datos SQL externa pesada[cite: 1, 2].

**2. Autenticación y Matriz de Permisos (RBAC):**
* El archivo `app.py` valida la sesión activa antes de renderizar la aplicación[cite: 2].
* Si un usuario ingresa como **Técnico de Mantenimiento**, el menú lateral y las vistas restringen el acceso a los formularios de asignación estratégica y de gestión de usuarios, dirigiéndolo directamente a la pantalla de patio para registrar entradas y salidas[cite: 2].
* Si ingresa el **Supervisor**, se desbloquea el motor de asignación y la edición de umbrales[cite: 2].

**3. Algoritmo de Asignación y Prevención de Inconsistencias:**
* En el módulo `CU-03`, cuando se selecciona un equipo GSE en espera, el sistema lee su familia (`PM`, `LO`, `CA/CB`, `TR`)[cite: 2].
* Automáticamente aplica un filtro de dos capas sobre el catálogo de bahías:
  1. Que la propiedad `estado` sea igual a `"Libre"`[cite: 2].
  2. Que la propiedad `familia` de la bahía sea idéntica a la del equipo[cite: 2].
* Esto elimina por diseño cualquier error humano de asignación errónea o duplicidad de equipos en una misma bahía[cite: 2].

**4. Detección Temprana de Cuellos de Botella (Motor de Alertas):**
* Cada taller (*PV1*, *Lote Comercial*, *Lote Carguero*) evalúa en tiempo de renderizado la cantidad de bahías disponibles[cite: 2].
* Si el número de bahías libres es menor o igual al valor configurado en `umbrales_alerta`, se despliega un mensaje crítico en la parte superior del tablero general, alertando a los operadores antes de que se produzca saturación en rampa[cite: 2].

```

