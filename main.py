"""
Módulo 5 - Simulación (Software FJ)
Curso: Programación (213023) - UNAD

Flujo principal del sistema. Ejecuta 14 operaciones de prueba (válidas e
inválidas) sobre clientes, servicios y reservas, y demuestra que el programa
sigue funcionando aunque ocurran errores. Todo queda registrado en
sistema_logs.txt.

Uso:  python main.py   (ejecutar desde la carpeta del proyecto)
"""

# ---------------------------------------------------------------------------
# Integración con los demás módulos
# ---------------------------------------------------------------------------
from fase4 import ErrorSistemaPersonalizado, registrar_log      # Módulo 1
from cliente import RegistroClientes                             # Módulo 2
from servicios import (                                          # Módulo 3
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
    ErrorServicio,
)
from reserva import Reserva                                      # Módulo 4

# Errores que el sistema considera "controlados" (esperados y manejados).
# Se incluye ErrorServicio por si el Módulo 3 aún no hereda de la base común.
ERRORES_CONTROLADOS = (ErrorSistemaPersonalizado, ErrorServicio)

# Aquí se guarda el resultado de cada operación para el resumen final.
resultados = []


def ejecutar_operacion(numero, titulo, funcion, debe_fallar):
    """
    Ejecuta una operación de forma segura.
    - Si termina bien            -> 'exitosa'
    - Si lanza un error del sistema -> 'error controlado' (se registra y continúa)
    - Si lanza cualquier otro error -> 'error inesperado' (se registra y continúa)
    El bloque finally siempre deja una traza en el log.
    """
    print(f"\n[{numero:02d}] {titulo}")
    registrar_log(f"[EVENTO] Operación {numero}: {titulo}")
    resultado_real = None

    try:
        funcion()
    except ERRORES_CONTROLADOS as error:
        resultado_real = "error controlado"
        print(f"     ✗ Error controlado ({type(error).__name__}): {error}")
        # Si la excepción viene encadenada, se muestra la causa original
        if error.__cause__ is not None:
            causa = error.__cause__
            print(f"       Causa original: {type(causa).__name__}: {causa}")
        registrar_log(f"[ERROR] Operación {numero} rechazada: {error}")
    except Exception as error:  # cualquier fallo no previsto
        resultado_real = "error inesperado"
        print(f"     ✗ Error INESPERADO ({type(error).__name__}): {error}")
        registrar_log(
            f"[ERROR] Operación {numero} con error inesperado: "
            f"{type(error).__name__}: {error}"
        )
    else:
        resultado_real = "exitosa"
        registrar_log(f"[EVENTO] Operación {numero} exitosa.")
    finally:
        registrar_log(f"[TRAZA] Operación {numero} finalizada.")

    esperado = "error controlado" if debe_fallar else "exitosa"
    resultados.append((numero, titulo, esperado, resultado_real))


def ejecutar_simulacion():
    """Define y ejecuta las 14 operaciones de prueba."""
    registro = RegistroClientes()  # lista interna de clientes (sin base de datos)
    ctx = {}                       # datos compartidos entre operaciones

    # ======================= CLIENTES (operaciones 1 a 3) ====================
    def op01():
        ctx["cliente"] = registro.registrar(
            "Yulieth Gómez", "1032456789", "yulieth@correo.com", "3101234567"
        )
        print(f"     ✓ {ctx['cliente']}")

    def op02():
        # Documento con letras: debe fallar y mostrar el error encadenado
        registro.registrar("Ana Torres", "12ab", "ana@correo.com")

    def op03():
        # Documento distinto pero correo ya registrado: duplicado
        registro.registrar("Otra Persona", "1098765432", "yulieth@correo.com")

    # ======================= SERVICIOS (operaciones 4 a 6) ===================
    def op04():
        ctx["sala"] = ReservaSala(
            "SAL-001", "Sala Ejecutiva Norte", 85000, capacidad=12, tiene_proyector=True
        )
        ctx["equipo"] = AlquilerEquipo(
            "EQP-015", "Laptop Dell XPS 15", 45000, tipo_equipo="laptop", stock=5
        )
        ctx["asesoria"] = AsesoriaEspecializada(
            "ASE-007", "Arquitectura de Software", 120000,
            especialidad="Arquitectura", nivel="avanzado",
        )
        for servicio in (ctx["sala"], ctx["equipo"], ctx["asesoria"]):
            print(f"     ✓ {servicio}")
        # Polimorfismo: el mismo método describir() se comporta distinto en cada clase
        print(f"       {ctx['sala'].describir()}")
        print(f"       {ctx['equipo'].describir()}")
        print(f"       {ctx['asesoria'].describir()}")

    def op05():
        # Precio negativo y capacidad menor a 2
        ReservaSala("SAL-002", "Sala Pequeña", -50000, capacidad=1)

    def op06():
        # Tipo de equipo que no existe en la lista permitida
        AlquilerEquipo("EQP-020", "Equipo desconocido", 30000, tipo_equipo="nave espacial")

    # ======================= RESERVAS (operaciones 7 a 14) ===================
    def op07():
        # Sala con parámetros opcionales (personas y descuento): sobrecarga
        r = Reserva(ctx["cliente"], ctx["sala"], 3, personas=8, descuento=0.10)
        r.confirmar()
        costo = r.procesar()
        print(f"     ✓ Reserva #{r.id_reserva} {r.estado}. Costo: ${costo:,.0f}")

    def op08():
        # Asesoría urgente (recargo del 25 %)
        r = Reserva(ctx["cliente"], ctx["asesoria"], 2, urgente=True)
        r.confirmar()
        costo = r.procesar()
        print(f"     ✓ Reserva #{r.id_reserva} {r.estado}. Costo: ${costo:,.0f}")

    def op09():
        # Alquiler de 2 equipos por 5 días
        r = Reserva(ctx["cliente"], ctx["equipo"], 5, cantidad=2)
        r.confirmar()
        costo = r.procesar()
        print(f"     ✓ Reserva #{r.id_reserva} {r.estado}. Costo: ${costo:,.0f}")

    def op10():
        # 50 personas en una sala con capacidad para 12
        r = Reserva(ctx["cliente"], ctx["sala"], 2, personas=50)
        r.confirmar()
        r.procesar()

    def op11():
        # Servicio desactivado: no se puede confirmar la reserva
        asesoria_inactiva = AsesoriaEspecializada(
            "ASE-099", "Asesoría de Redes", 90000, especialidad="Redes"
        )
        asesoria_inactiva.desactivar()
        r = Reserva(ctx["cliente"], asesoria_inactiva, 1)
        r.confirmar()

    def op12():
        # Regla de negocio: solo se procesan reservas confirmadas
        r = Reserva(ctx["cliente"], ctx["sala"], 2, personas=4)
        r.procesar()

    def op13():
        # Cancelar una reserva dos veces: la segunda no está permitida
        r = Reserva(ctx["cliente"], ctx["sala"], 1, personas=3)
        r.cancelar("El cliente cambió de planes")
        print(f"     ✓ Reserva #{r.id_reserva} {r.estado} (primera cancelación)")
        r.cancelar("Segundo intento")

    def op14():
        # Pide 10 equipos y solo hay 5 en stock
        r = Reserva(ctx["cliente"], ctx["equipo"], 3, cantidad=10)
        r.confirmar()
        r.procesar()

    # Cada tupla: (número, descripción, función, ¿debe fallar?)
    operaciones = [
        (1,  "Registrar cliente válido",                          op01, False),
        (2,  "Registrar cliente con documento inválido",          op02, True),
        (3,  "Registrar cliente con correo duplicado",            op03, True),
        (4,  "Crear los tres tipos de servicio (válidos)",        op04, False),
        (5,  "Crear sala con precio negativo y capacidad baja",   op05, True),
        (6,  "Crear equipo con tipo inexistente",                 op06, True),
        (7,  "Reserva de sala exitosa (con descuento)",           op07, False),
        (8,  "Reserva de asesoría urgente exitosa",               op08, False),
        (9,  "Reserva de equipos exitosa",                        op09, False),
        (10, "Reserva con más personas que la capacidad",         op10, True),
        (11, "Reserva de un servicio no disponible",              op11, True),
        (12, "Procesar una reserva sin confirmarla",              op12, True),
        (13, "Cancelar una reserva dos veces",                    op13, True),
        (14, "Reserva de equipos con stock insuficiente",         op14, True),
    ]

    for numero, titulo, funcion, debe_fallar in operaciones:
        ejecutar_operacion(numero, titulo, funcion, debe_fallar)


def mostrar_resumen():
    """Imprime el resumen final y lo deja también en el log."""
    print("\n" + "=" * 72)
    print("RESUMEN DE LA SIMULACIÓN")
    print("=" * 72)
    print(f"{'N°':<4}{'Esperado':<18}{'Obtenido':<18}{'':<4}Operación")
    print("-" * 72)

    coinciden = 0
    for numero, titulo, esperado, obtenido in resultados:
        ok = esperado == obtenido
        coinciden += ok
        marca = "✓" if ok else "✗"
        print(f"{numero:<4}{esperado:<18}{obtenido:<18}{marca:<4}{titulo}")

    exitosas = sum(1 for r in resultados if r[3] == "exitosa")
    controlados = sum(1 for r in resultados if r[3] == "error controlado")
    inesperados = sum(1 for r in resultados if r[3] == "error inesperado")

    print("-" * 72)
    print(f"Operaciones ejecutadas : {len(resultados)}")
    print(f"Exitosas               : {exitosas}")
    print(f"Errores controlados    : {controlados}")
    print(f"Errores inesperados    : {inesperados}")
    print(f"Resultados esperados   : {coinciden} de {len(resultados)}")
    print("El programa terminó sin interrumpirse. Revise sistema_logs.txt")

    registrar_log(
        f"[EVENTO] Simulación finalizada: {exitosas} exitosas, "
        f"{controlados} errores controlados, {inesperados} inesperados."
    )


if __name__ == "__main__":
    registrar_log("[EVENTO] Inicio de la simulación de Software FJ.")
    print("=" * 72)
    print("SOFTWARE FJ - SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")
    print("=" * 72)
    try:
        ejecutar_simulacion()
    finally:
        # Aunque algo fallara a nivel global, siempre se muestra el resumen
        mostrar_resumen()
