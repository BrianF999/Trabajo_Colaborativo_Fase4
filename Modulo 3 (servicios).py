# ============================================================
# MÓDULO 3: SERVICIOS
# Sistema Integral de Gestión - Software FJ
# Curso: Programación (213023) Unad

from abc import ABC, abstractmethod
from datetime import datetime
import logging

# ------------------------------------------------------------
# Configuración del logger (archivo de logs)
# ------------------------------------------------------------
logging.basicConfig(
    filename="logs_sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# ------------------------------------------------------------
# Excepciones personalizadas
# ------------------------------------------------------------
class ErrorServicio(Exception):
    """Excepción base para errores relacionados con servicios."""
    pass

class ParametroInvalidoError(ErrorServicio):
    """Se lanza cuando un parámetro no es válido."""
    pass

class ServicioNoDisponibleError(ErrorServicio):
    """Se lanza cuando el servicio no está disponible."""
    pass

class CostoInconsistenteError(ErrorServicio):
    """Se lanza cuando el cálculo del costo genera inconsistencias."""
    pass

# ------------------------------------------------------------
# Clase abstracta Servicio
# ------------------------------------------------------------
class Servicio(ABC):
    """
    Clase abstracta que representa un servicio genérico
    ofrecido por Software FJ.
    """

    def __init__(self, codigo: str, nombre: str, precio_base: float, disponible: bool = True):
        self._codigo = None
        self._nombre = None
        self._precio_base = None
        self._disponible = disponible

        self.codigo = codigo
        self.nombre = nombre
        self.precio_base = precio_base

    # ---------- Propiedades con encapsulación ----------
    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ParametroInvalidoError("El código del servicio debe tener al menos 3 caracteres.")
        self._codigo = valor.strip().upper()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 5:
            raise ParametroInvalidoError("El nombre del servicio debe tener al menos 5 caracteres.")
        self._nombre = valor.strip()

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor: float):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ParametroInvalidoError("El precio base debe ser un número positivo.")
        self._precio_base = float(valor)

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        if not isinstance(valor, bool):
            raise ParametroInvalidoError("El estado de disponibilidad debe ser booleano.")
        self._disponible = valor

    # ---------- Métodos abstractos (polimorfismo) ----------
    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """Calcula el costo del servicio (debe ser implementado por las subclases)."""
        pass

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción detallada del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self, **parametros) -> bool:
        """Valida los parámetros específicos del servicio."""
        pass

    # ---------- Métodos comunes ----------
    def activar(self):
        self.disponible = True
        logging.info(f"Servicio {self.codigo} activado.")

    def desactivar(self):
        self.disponible = False
        logging.info(f"Servicio {self.codigo} desactivado.")

    def __str__(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"[{self.codigo}] {self.nombre} - ${self.precio_base:,.0f} ({estado})"

# ------------------------------------------------------------
# Subclase 1: ReservaSala
# ------------------------------------------------------------
class ReservaSala(Servicio):
    """
    Servicio de reserva de salas de reuniones / coworking.
    """

    def __init__(self, codigo: str, nombre: str, precio_base: float,
                 capacidad: int, tiene_proyector: bool = True, disponible: bool = True):
        super().__init__(codigo, nombre, precio_base, disponible)
        self._capacidad = None
        self._tiene_proyector = tiene_proyector
        self.capacidad = capacidad

    @property
    def capacidad(self) -> int:
        return self._capacidad

    @capacidad.setter
    def capacidad(self, valor: int):
        if not isinstance(valor, int) or valor < 2:
            raise ParametroInvalidoError("La capacidad de la sala debe ser un entero mayor o igual a 2.")
        self._capacidad = valor

    @property
    def tiene_proyector(self) -> bool:
        return self._tiene_proyector

    def validar_parametros(self, **parametros) -> bool:
        horas = parametros.get("horas")
        personas = parametros.get("personas")

        if horas is None or not isinstance(horas, (int, float)) or horas <= 0:
            raise ParametroInvalidoError("Debe indicar un número de horas válido (mayor a 0).")
        if personas is None or not isinstance(personas, int) or personas < 1:
            raise ParametroInvalidoError("Debe indicar un número de personas válido.")
        if personas > self.capacidad:
            raise ParametroInvalidoError(f"La sala solo admite hasta {self.capacidad} personas.")
        return True

    def calcular_costo(self, horas: float = 1, personas: int = 1,
                       aplicar_impuesto: bool = True, descuento: float = 0.0) -> float:
        """
        Método sobrecargado:
        - calcular_costo(horas)
        - calcular_costo(horas, personas)
        - calcular_costo(horas, personas, aplicar_impuesto=True/False)
        - calcular_costo(..., descuento=0.15)
        """
        try:
            if not self.disponible:
                raise ServicioNoDisponibleError(f"El servicio {self.codigo} no está disponible.")

            self.validar_parametros(horas=horas, personas=personas)

            if descuento < 0 or descuento > 0.5:
                raise ParametroInvalidoError("El descuento debe estar entre 0 y 50%.")

            costo = self.precio_base * horas

            # Extra por proyector (si aplica)
            if self.tiene_proyector and horas >= 2:
                costo += 15000

            # Descuento
            costo -= costo * descuento

            # Impuesto (19% IVA)
            if aplicar_impuesto:
                costo *= 1.19

            if costo <= 0:
                raise CostoInconsistenteError("El costo calculado no puede ser menor o igual a cero.")

            logging.info(f"Costo calculado para {self.codigo}: ${costo:,.0f}")
            return round(costo, 2)

        except ErrorServicio as e:
            logging.error(f"Error en calcular_costo de ReservaSala: {e}")
            raise

    def describir(self) -> str:
        proyector = "con proyector" if self.tiene_proyector else "sin proyector"
        return (f"Reserva de sala '{self.nombre}' (código {self.codigo}). "
                f"Capacidad: {self.capacidad} personas, {proyector}. "
                f"Precio base por hora: ${self.precio_base:,.0f}.")

# ------------------------------------------------------------
# Subclase 2: AlquilerEquipo
# ------------------------------------------------------------
class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de equipos tecnológicos.
    """

    def __init__(self, codigo: str, nombre: str, precio_base: float,
                 tipo_equipo: str, stock: int = 1, disponible: bool = True):
        super().__init__(codigo, nombre, precio_base, disponible)
        self._tipo_equipo = None
        self._stock = None
        self.tipo_equipo = tipo_equipo
        self.stock = stock

    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo

    @tipo_equipo.setter
    def tipo_equipo(self, valor: str):
        tipos_validos = ["laptop", "proyector", "monitor", "impresora", "camara", "otro"]
        if not valor or valor.lower() not in tipos_validos:
            raise ParametroInvalidoError(f"Tipo de equipo no válido. Opciones: {', '.join(tipos_validos)}")
        self._tipo_equipo = valor.lower()

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int):
        if not isinstance(valor, int) or valor < 0:
            raise ParametroInvalidoError("El stock debe ser un entero mayor o igual a 0.")
        self._stock = valor
        if self._stock == 0:
            self.disponible = False

    def validar_parametros(self, **parametros) -> bool:
        dias = parametros.get("dias")
        cantidad = parametros.get("cantidad", 1)

        if dias is None or not isinstance(dias, (int, float)) or dias <= 0:
            raise ParametroInvalidoError("Debe indicar un número de días válido.")
        if not isinstance(cantidad, int) or cantidad < 1:
            raise ParametroInvalidoError("La cantidad debe ser un entero positivo.")
        if cantidad > self.stock:
            raise ServicioNoDisponibleError(f"Solo hay {self.stock} unidades disponibles de este equipo.")
        return True

    def calcular_costo(self, dias: float = 1, cantidad: int = 1,
                       aplicar_impuesto: bool = True, descuento: float = 0.0) -> float:
        try:
            if not self.disponible:
                raise ServicioNoDisponibleError(f"El servicio {self.codigo} no está disponible.")

            self.validar_parametros(dias=dias, cantidad=cantidad)

            if descuento < 0 or descuento > 0.4:
                raise ParametroInvalidoError("El descuento máximo para equipos es del 40%.")

            costo = self.precio_base * dias * cantidad

            # Descuento por alquiler largo
            if dias >= 7:
                costo *= 0.90  # 10% de descuento automático

            costo -= costo * descuento

            if aplicar_impuesto:
                costo *= 1.19

            if costo <= 0:
                raise CostoInconsistenteError("Costo inconsistente detectado.")

            logging.info(f"Costo calculado para {self.codigo}: ${costo:,.0f}")
            return round(costo, 2)

        except ErrorServicio as e:
            logging.error(f"Error en calcular_costo de AlquilerEquipo: {e}")
            raise

    def describir(self) -> str:
        return (f"Alquiler de equipo: {self.nombre} ({self.tipo_equipo}). "
                f"Código: {self.codigo}. Stock actual: {self.stock}. "
                f"Precio por día: ${self.precio_base:,.0f}.")

# ------------------------------------------------------------
# Subclase 3: AsesoriaEspecializada
# ------------------------------------------------------------
class AsesoriaEspecializada(Servicio):
    """
    Servicio de asesorías especializadas (software, arquitectura, etc.).
    """

    def __init__(self, codigo: str, nombre: str, precio_base: float,
                 especialidad: str, nivel: str = "intermedio", disponible: bool = True):
        super().__init__(codigo, nombre, precio_base, disponible)
        self._especialidad = None
        self._nivel = None
        self.especialidad = especialidad
        self.nivel = nivel

    @property
    def especialidad(self) -> str:
        return self._especialidad

    @especialidad.setter
    def especialidad(self, valor: str):
        if not valor or len(valor.strip()) < 4:
            raise ParametroInvalidoError("La especialidad debe tener al menos 4 caracteres.")
        self._especialidad = valor.strip().title()

    @property
    def nivel(self) -> str:
        return self._nivel

    @nivel.setter
    def nivel(self, valor: str):
        niveles_validos = ["basico", "intermedio", "avanzado", "experto"]
        if valor.lower() not in niveles_validos:
            raise ParametroInvalidoError(f"Nivel no válido. Opciones: {', '.join(niveles_validos)}")
        self._nivel = valor.lower()

    def validar_parametros(self, **parametros) -> bool:
        horas = parametros.get("horas")
        if horas is None or not isinstance(horas, (int, float)) or horas < 1:
            raise ParametroInvalidoError("Las horas de asesoría deben ser al menos 1.")
        return True

    def calcular_costo(self, horas: float = 1, aplicar_impuesto: bool = True,
                       descuento: float = 0.0, urgente: bool = False) -> float:
        """
        Sobrecarga de parámetros:
        - urgente=True → recargo del 25%
        """
        try:
            if not self.disponible:
                raise ServicioNoDisponibleError(f"La asesoría {self.codigo} no está disponible.")

            self.validar_parametros(horas=horas)

            if descuento < 0 or descuento > 0.3:
                raise ParametroInvalidoError("El descuento máximo para asesorías es del 30%.")

            # Multiplicador según nivel
            multiplicadores = {
                "basico": 1.0,
                "intermedio": 1.25,
                "avanzado": 1.6,
                "experto": 2.0
            }
            costo = self.precio_base * horas * multiplicadores[self.nivel]

            if urgente:
                costo *= 1.25  # Recargo por urgencia

            costo -= costo * descuento

            if aplicar_impuesto:
                costo *= 1.19

            if costo <= 0:
                raise CostoInconsistenteError("El costo de la asesoría resultó inconsistente.")

            logging.info(f"Costo calculado para {self.codigo}: ${costo:,.0f}")
            return round(costo, 2)

        except ErrorServicio as e:
            logging.error(f"Error en calcular_costo de AsesoriaEspecializada: {e}")
            raise

    def describir(self) -> str:
        return (f"Asesoría especializada en {self.especialidad} "
                f"(nivel {self.nivel}). Código: {self.codigo}. "
                f"Precio base por hora: ${self.precio_base:,.0f}.")

# ============================================================
# Ejemplo de uso / pruebas del módulo (puedes borrar o comentar)
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("PRUEBAS DEL MÓDULO DE SERVICIOS - Software FJ")
    print("=" * 60)

    try:
        # Creación correcta de servicios
        sala = ReservaSala("SAL-001", "Sala Ejecutiva Norte", 85000, capacidad=12, tiene_proyector=True)
        equipo = AlquilerEquipo("EQP-015", "Laptop Dell XPS 15", 45000, tipo_equipo="laptop", stock=5)
        asesoria = AsesoriaEspecializada("ASE-007", "Arquitectura de Software", 120000,
                                         especialidad="Arquitectura", nivel="avanzado")

        print("\n--- Servicios creados correctamente ---")
        print(sala)
        print(equipo)
        print(asesoria)

        print("\n--- Descripciones ---")
        print(sala.describir())
        print(equipo.describir())
        print(asesoria.describir())

        print("\n--- Cálculos de costo (polimorfismo + sobrecarga) ---")
        print(f"Sala 3 horas: ${sala.calcular_costo(3):,.0f}")
        print(f"Sala 4 horas con 10% descuento: ${sala.calcular_costo(4, descuento=0.10):,.0f}")
        print(f"Equipo 5 días x 2 unidades: ${equipo.calcular_costo(5, cantidad=2):,.0f}")
        print(f"Asesoría 2 horas urgente: ${asesoria.calcular_costo(2, urgente=True):,.0f}")

    except ErrorServicio as e:
        print(f"\nError controlado: {e}")
        logging.error(f"Error en prueba principal: {e}")

    # Pruebas de errores (el sistema no se cae)
    print("\n--- Pruebas de manejo de errores ---")
    try:
        sala_invalida = ReservaSala("S1", "Sala", -50000, capacidad=1)
    except ErrorServicio as e:
        print(f"Error esperado al crear sala inválida: {e}")

    try:
        print(equipo.calcular_costo(dias=3, cantidad=10))  # stock insuficiente
    except ErrorServicio as e:
        print(f"Error esperado por stock: {e}")

    try:
        asesoria.desactivar()
        print(asesoria.calcular_costo(2))
    except ErrorServicio as e:
        print(f"Error esperado por servicio no disponible: {e}")

    print("\nMódulo de servicios ejecutado correctamente. Revisa el archivo logs_sistema.log")