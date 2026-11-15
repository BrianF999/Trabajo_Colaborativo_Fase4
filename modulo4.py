# MÓDULO 4: CLASE RESERVA
# Curso: Programación (213023) - UNAD

from datetime import datetime

# SIMULACIÓN DE EXCEPCIONES BASE (Para prueba independiente)
# (En tu proyecto real, estas vienen del Módulo 1)

class ErrorSistemaPersonalizado(Exception):
    pass

def registrar_log(mensaje):
    # Simula el guardado en sistema_logs.txt
    print(f"[LOG] {mensaje}")

# Simulación de entidades (En tu proyecto real, vienen del Módulo 2 y 3)
class Cliente:
    def __init__(self, nombre): self.nombre = nombre

class Servicio:
    def __init__(self, codigo):
        self.codigo = codigo
        self.disponible = True
    def calcular_costo(self, duracion): return duracion * 1000 # Costo genérico de prueba
    def validar_parametros(self, **kwargs): return True


# EXCEPCIONES PROPIAS DEL MÓDULO 4

class ReservaInvalidaError(ErrorSistemaPersonalizado):
    """Se lanza si los datos iniciales de la reserva no son correctos."""
    pass

class EstadoReservaError(ErrorSistemaPersonalizado):
    """Se lanza cuando se intenta una acción no permitida para el estado actual."""
    pass

class ReservaNoProcesableError(ErrorSistemaPersonalizado):
    """Se lanza si ocurre un error durante el cálculo del costo."""
    pass

# CLASE RESERVA

class Reserva:
    """
    Integra cliente, servicio, duración y estado.
    Implementa confirmar, cancelar y procesar con manejo de excepciones.
    """
    _contador = 0

    def __init__(self, cliente, servicio, duracion):
        # 1. VALIDACIÓN INICIAL (Try / Except / Else)
        try:
            if not isinstance(cliente, Cliente):
                raise TypeError("El cliente no es una instancia válida.")
            if not isinstance(servicio, Servicio):
                raise TypeError("El servicio no es una instancia válida.")
            if duracion <= 0:
                raise ValueError("La duración debe ser mayor a 0.")
            
            # Validación polimórfica del servicio
            servicio.validar_parametros(duracion=duracion)

        except Exception as causa:
            # Encadenamiento de excepciones (raise ... from)
            raise ReservaInvalidaError(f"No se pudo crear la reserva: {causa}") from causa
        
        else:
            # 2. INTEGRACIÓN DE DATOS (Si no hubo error)
            Reserva._contador += 1
            self.__id = Reserva._contador
            self.__cliente = cliente
            self.__servicio = servicio
            self.__duracion = duracion
            self.__estado = "Pendiente" # Estado inicial
            self.__costo_final = None
            
            registrar_log(f"[EVENTO] Reserva #{self.__id} creada para {cliente.nombre}.")
        
        finally:
            pass # Se ejecuta siempre

    # --- PROPIEDADES (Encapsulación) ---
    @property
    def id_reserva(self): return self.__id
    @property
    def estado(self): return self.__estado
    @property
    def costo_final(self): return self.__costo_final

    # --- MÉTODOS DE OPERACIÓN ---

    def confirmar(self):
        """Cambia el estado a 'Confirmada' validando el servicio."""
        try:
            if self.__estado not in ["Pendiente", "Fallida"]:
                raise EstadoReservaError(f"No se puede confirmar una reserva en estado '{self.__estado}'.")
            if not self.__servicio.disponible:
                raise ReservaNoProcesableError("El servicio no está disponible actualmente.")
            
        except ErrorSistemaPersonalizado as e:
            self.__estado = "Fallida"
            registrar_log(f"[ERROR] Confirmación fallida #{self.__id}: {e}")
            raise
        else:
            self.__estado = "Confirmada"
            registrar_log(f"[EVENTO] Reserva #{self.__id} CONFIRMADA.")
            return True

    def cancelar(self, motivo="No especificado"):
        """Cambia el estado a 'Cancelada' si no ha sido procesada."""
        try:
            if self.__estado in ["Cancelada", "Procesada"]:
                raise EstadoReservaError(f"No se puede cancelar una reserva en estado '{self.__estado}'.")
            
        except ErrorSistemaPersonalizado as e:
            registrar_log(f"[ERROR] Cancelación fallida #{self.__id}: {e}")
            raise
        else:
            self.__estado = "Cancelada"
            registrar_log(f"[EVENTO] Reserva #{self.__id} CANCELADA. Motivo: {motivo}")
            return True

    def procesar(self):
        """Calcula el costo final y cambia el estado a 'Procesada'."""
        try:
            if self.__estado != "Confirmada":
                raise EstadoReservaError("Regla de negocio: Solo se procesan reservas confirmadas.")
            
            # Cálculo del costo
            costo = self.__servicio.calcular_costo(self.__duracion)
            
            if costo <= 0:
                raise ReservaNoProcesableError("El costo calculado resultó ser inválido.")

        except ErrorSistemaPersonalizado as e:
            self.__estado = "Fallida"
            registrar_log(f"[ERROR] Procesamiento fallido #{self.__id}: {e}")
            raise
        else:
            self.__costo_final = costo
            self.__estado = "Procesada"
            registrar_log(f"[EVENTO] Reserva #{self.__id} PROCESADA. Costo: ${costo:,.2f}")
            return self.__costo_final
        
        finally:
            registrar_log(f"[TRAZA] Operación procesar finalizada para reserva #{self.__id}.")


# PRUEBAS DE LA CLASE RESERVA

if __name__ == "__main__":
    print("--- PRUEBAS DE LA CLASE RESERVA ---")

    # Instanciamos datos simulados
    mi_cliente = Cliente("Yulieth Gómez")
    mi_servicio = Servicio("SAL-001")

    # Caso 1: Creación y procesamiento exitoso
    try:
        r1 = Reserva(mi_cliente, mi_servicio, 3)
        r1.confirmar()
        costo = r1.procesar()
        print(f"✅ Éxito: Reserva #{r1.id_reserva} finalizada. Costo: ${costo}")
    except Exception as e:
        print(f" Falló Caso 1: {e}")

    # Caso 2: Error al procesar sin confirmar
    try:
        r2 = Reserva(mi_cliente, mi_servicio, 2)
        r2.procesar() # Lanzará error
    except Exception as e:
        print(f" Error controlado (Procesar sin confirmar): {e}")

    # Caso 3: Error al crear con duración negativa
    try:
        Reserva(mi_cliente, mi_servicio, -5)
    except Exception as e:
        print(f" Error controlado (Duración inválida): {e}")

    # Caso 4: Error al cancelar una reserva ya procesada
    try:
        r3 = Reserva(mi_cliente, mi_servicio, 1)
        r3.confirmar()
        r3.procesar()
        r3.cancelar("Ya no la quiero") # Lanzará error
    except Exception as e:
        print(f" Error controlado (Cancelar procesada): {e}")