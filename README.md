# Software FJ: Sistema Integral de Gestión de Clientes, Servicios y Reservas

**Universidad Nacional Abierta y a Distancia (UNAD)**
Escuela de Ciencias Básicas, Tecnología e Ingeniería (ECBTI)
Programa: Ingeniería de Sistemas
Curso: Programación (213023)
Actividad: Fase 4, Prácticas simuladas (trabajo colaborativo)

---

## Descripción

Aplicación en **Python** desarrollada con **Programación Orientada a Objetos** para la empresa ficticia **Software FJ**, que ofrece reservas de salas, alquiler de equipos y asesorías especializadas.

El sistema gestiona **clientes, servicios y reservas** sin usar bases de datos: toda la información se maneja en memoria mediante objetos y listas. Los archivos se usan únicamente para el **registro de eventos y errores** en `sistema_logs.txt`.

El objetivo es construir una aplicación **estable, modular y extensible**, que siga funcionando aun cuando ocurran errores durante su ejecución.

## Conceptos aplicados

- **Abstracción:** clases abstractas `Entidad` y `Servicio`.
- **Herencia:** `Cliente` hereda de `Entidad`; `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada` heredan de `Servicio`.
- **Polimorfismo:** métodos `calcular_costo`, `describir` y `validar_parametros` sobrescritos en cada servicio.
- **Encapsulación:** atributos privados o protegidos con propiedades y validaciones.
- **Sobrecarga de métodos:** `calcular_costo` admite parámetros opcionales (horas, personas, días, cantidad, impuesto, descuento y urgencia). Como Python no tiene sobrecarga real, se simula con parámetros opcionales.
- **Manejo avanzado de excepciones:**
  - Excepciones personalizadas organizadas en jerarquías.
  - Bloques `try/except`, `try/except/else` y `try/except/finally`.
  - Encadenamiento de excepciones (`raise ... from ...`).
- **Registro de logs** de errores y eventos relevantes.

## Estructura del proyecto

```
.
├── README.md
├── fase4.py        # Módulo 1: logs y excepciones base
├── cliente.py      # Módulo 2: clase Entidad, Cliente y RegistroClientes
├── servicios.py    # Módulo 3: clase Servicio y servicios especializados
├── reserva.py      # Módulo 4: clase Reserva
├── main.py         # Módulo 5: flujo principal y simulación
└── sistema_logs.txt   # Archivo de logs (se genera al ejecutar)
```

## Módulos

| Módulo | Archivo | Contenido |
|---|---|---|
| 1. Logs y excepciones | `fase4.py` | `registrar_log`, `ErrorSistemaPersonalizado`, `ErrorDatoInvalido`, `ErrorOperacionNoPermitida` |
| 2. Clientes | `cliente.py` | `Entidad` (abstracta), `Cliente` (validación de documento, correo, nombre y teléfono), `RegistroClientes` |
| 3. Servicios | `servicios.py` | `Servicio` (abstracta), `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| 4. Reservas | `reserva.py` | `Reserva` con confirmación, cancelación y procesamiento |
| 5. Simulación | `main.py` | Flujo principal y operaciones de prueba |

## Diseño de clases

| Clase | Tipo | Responsabilidad |
|---|---|---|
| `Entidad` | Abstracta | Representa entidades generales del sistema |
| `Cliente` | Hereda de `Entidad` | Datos personales encapsulados con validaciones estrictas |
| `RegistroClientes` | Concreta | Lista interna de clientes; evita documentos y correos duplicados |
| `Servicio` | Abstracta | Define costo, descripción y validación de parámetros |
| `ReservaSala` | Hija de `Servicio` | Reserva de salas por horas, con capacidad y proyector |
| `AlquilerEquipo` | Hija de `Servicio` | Alquiler de equipos por días, con control de stock |
| `AsesoriaEspecializada` | Hija de `Servicio` | Asesorías por horas, con nivel y recargo por urgencia |
| `Reserva` | Concreta | Integra cliente, servicio, duración y estado |

## Excepciones personalizadas

| Archivo | Excepciones |
|---|---|
| `fase4.py` | `ErrorSistemaPersonalizado` (base), `ErrorDatoInvalido`, `ErrorOperacionNoPermitida` |
| `cliente.py` | `ClienteInvalidoError`, `DocumentoInvalidoError`, `CorreoInvalidoError`, `ClienteDuplicadoError` |
| `servicios.py` | `ErrorServicio` (base), `ParametroInvalidoError`, `ServicioNoDisponibleError`, `CostoInconsistenteError` |
| `reserva.py` | `ReservaInvalidaError`, `EstadoReservaError`, `ReservaNoProcesableError` |

## Requisitos

- Python 3.8 o superior
- No requiere librerías externas ni bases de datos

## Cómo ejecutar

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/BrianF999/Trabajo_Colaborativo_Fase4.git
   cd Trabajo_Colaborativo_Fase4
   ```
2. Ejecutar la simulación desde la carpeta del proyecto:
   ```bash
   python main.py
   ```
3. Revisar el archivo de logs `sistema_logs.txt`, generado en la misma carpeta.

## Simulación

`main.py` ejecuta **14 operaciones completas** (el anexo exige mínimo 10):

| N° | Operación |
|---|---|
| 1 | Registrar cliente válido |
| 2 | Registrar cliente con documento inválido |
| 3 | Registrar cliente con correo duplicado |
| 4 | Crear los tres tipos de servicio (válidos) |
| 5 | Crear sala con precio negativo y capacidad baja |
| 6 | Crear equipo con tipo inexistente |
| 7 | Reserva de sala exitosa (con descuento) |
| 8 | Reserva de asesoría urgente exitosa |
| 9 | Reserva de equipos exitosa |
| 10 | Reserva con más personas que la capacidad |
| 11 | Reserva de un servicio no disponible |
| 12 | Procesar una reserva sin confirmarla |
| 13 | Cancelar una reserva dos veces |
| 14 | Reserva de equipos con stock insuficiente |

Cada error detectado se registra en el log y el programa continúa su ejecución sin interrumpirse. Al final se muestra un resumen con las operaciones exitosas y los errores controlados.

## Integrantes y aportes

| Integrante | Usuario de GitHub | Módulo |
|---|---|---|
| Brian Felipe Penha Ortiz | [`@BrianF999`](https://github.com/BrianF999) | Módulo 1: logs y excepciones |
| Heidy Yulieth Torres Céspedes | [`@yulieth2007`](https://github.com/yulieth2007) | Módulo 2: clientes |
| Jeyson Fabian Martínez Horta | [`@yeisonfabianmartinezhorta-ui`](https://github.com/yeisonfabianmartinezhorta-ui) | Módulo 3: servicios |
| Nataly Ortega Higuita | [`@nalyinmidahiguita-svg`](https://github.com/nalyinmidahiguita-svg) | Módulo 4: reservas |
| Juan David Jiménez Correa | [`@juand42`](https://github.com/juand42) | Módulo 5: simulación |
