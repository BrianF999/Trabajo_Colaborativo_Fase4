"""
Módulo 2 - Clientes (Software FJ)
Curso: Programación (213023) - UNAD

Contiene:
- Entidad: clase abstracta base (entidades generales del sistema).
- Cliente: encapsulación de datos personales + validaciones estrictas.
- RegistroClientes: lista interna de clientes (sin base de datos).


"""

import re
from abc import ABC, abstractmethod

# ---------------------------------------------------------------------------
# Integración con el Módulo 1 (fase4.py)
# ---------------------------------------------------------------------------
from fase4 import (
    ErrorSistemaPersonalizado,
    ErrorDatoInvalido,
    ErrorOperacionNoPermitida,
    registrar_log,
)


# Excepciones propias del Módulo 2 (heredan de las del Módulo 1)
class ClienteInvalidoError(ErrorDatoInvalido):
    """Datos de cliente inválidos."""


class DocumentoInvalidoError(ClienteInvalidoError):
    """Documento de identidad inválido."""


class CorreoInvalidoError(ClienteInvalidoError):
    """Correo electrónico inválido."""


class ClienteDuplicadoError(ErrorOperacionNoPermitida):
    """Intento de registrar un cliente que ya existe."""


def registrar_evento(mensaje):
    registrar_log(f"[EVENTO] {mensaje}")


def registrar_error(mensaje):
    registrar_log(f"[ERROR] {mensaje}")


# ---------------------------------------------------------------------------
# Clase abstracta general
# ---------------------------------------------------------------------------
class Entidad(ABC):
    """Abstracción de cualquier entidad del sistema (cliente, servicio, reserva)."""

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción legible de la entidad."""


# ---------------------------------------------------------------------------
# Cliente
# ---------------------------------------------------------------------------
class Cliente(Entidad):
    _contador = 0  # genera ids automáticos

    _PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?: [A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*$")
    _PATRON_DOCUMENTO = re.compile(r"^\d{6,10}$")  # cédula colombiana: 6 a 10 dígitos
    _PATRON_CORREO = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")
    _PATRON_TELEFONO = re.compile(r"^3\d{9}$")  # celular colombiano

    def __init__(self, nombre, documento, correo, telefono=None):
        try:
            # Se asignan mediante los setters para forzar las validaciones
            self.nombre = nombre
            self.documento = documento
            self.correo = correo
            self.telefono = telefono
        except ClienteInvalidoError as e:
            registrar_error(f"No se pudo crear el cliente: {e}")
            raise
        else:
            Cliente._contador += 1
            self.__id = Cliente._contador
            registrar_evento(f"Cliente creado: {self.__nombre} (ID {self.__id})")
        finally:
            # Se ejecuta siempre, con o sin error
            pass

    # ---- Propiedades (encapsulación) ----
    @property
    def id_cliente(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ClienteInvalidoError("El nombre es obligatorio.")
        valor = " ".join(valor.split())  # limpia espacios repetidos
        if len(valor) < 3 or not self._PATRON_NOMBRE.match(valor):
            raise ClienteInvalidoError(
                f"Nombre inválido '{valor}': solo letras y mínimo 3 caracteres."
            )
        self.__nombre = valor.title()

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        try:
            if valor is None:
                raise ValueError("documento vacío")
            texto = str(valor).strip().replace(".", "")  # acepta 1.234.567
            if not self._PATRON_DOCUMENTO.match(texto):
                raise ValueError("debe tener solo dígitos (6 a 10)")
            if len(set(texto)) == 1:
                raise ValueError("no puede ser un mismo dígito repetido")
        except ValueError as causa:
            # Encadenamiento de excepciones
            raise DocumentoInvalidoError(
                f"Documento inválido '{valor}'."
            ) from causa
        self.__documento = texto

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise CorreoInvalidoError("El correo es obligatorio.")
        valor = valor.strip().lower()
        if len(valor) > 254 or ".." in valor or not self._PATRON_CORREO.match(valor):
            raise CorreoInvalidoError(f"Correo inválido '{valor}'.")
        self.__correo = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None or str(valor).strip() == "":
            self.__telefono = None  # opcional
            return
        texto = str(valor).strip().replace(" ", "")
        if not self._PATRON_TELEFONO.match(texto):
            raise ClienteInvalidoError(
                f"Teléfono inválido '{valor}': debe ser celular de 10 dígitos (inicia en 3)."
            )
        self.__telefono = texto

    # ---- Métodos ----
    def describir(self) -> str:
        tel = self.__telefono if self.__telefono else "sin teléfono"
        return (f"Cliente #{self.__id}: {self.__nombre} | "
                f"Doc: {self.__documento} | {self.__correo} | {tel}")

    def a_diccionario(self) -> dict:
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "documento": self.__documento,
            "correo": self.__correo,
            "telefono": self.__telefono,
        }

    def __str__(self):
        return self.describir()

    def __repr__(self):
        return f"Cliente(id={self.__id}, nombre='{self.__nombre}')"


# ---------------------------------------------------------------------------
# Registro interno (lista en memoria, sin base de datos)
# ---------------------------------------------------------------------------
class RegistroClientes:
    def __init__(self):
        self._clientes = []

    def registrar(self, nombre, documento, correo, telefono=None):
        """Crea y guarda un cliente; evita documentos o correos duplicados."""
        try:
            nuevo = Cliente(nombre, documento, correo, telefono)
            for c in self._clientes:
                if c.documento == nuevo.documento:
                    raise ClienteDuplicadoError(
                        f"Ya existe un cliente con el documento {nuevo.documento}."
                    )
                if c.correo == nuevo.correo:
                    raise ClienteDuplicadoError(
                        f"Ya existe un cliente con el correo {nuevo.correo}."
                    )
        except ErrorSistemaPersonalizado as e:
            registrar_error(f"Registro de cliente rechazado: {e}")
            raise
        else:
            self._clientes.append(nuevo)
            registrar_evento(f"Cliente registrado en el sistema: {nuevo.nombre}")
            return nuevo

    def buscar_por_documento(self, documento):
        doc = str(documento).strip().replace(".", "")
        for c in self._clientes:
            if c.documento == doc:
                return c
        raise ClienteInvalidoError(f"No existe cliente con documento {documento}.")

    def listar(self):
        return list(self._clientes)  # copia: protege la lista interna

    def __len__(self):
        return len(self._clientes)


# ---------------------------------------------------------------------------
# Prueba rápida del módulo (python cliente.py)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    registro = RegistroClientes()
    casos = [
        ("Yulieth Gómez", "1.234.567.89", "yulieth@correo.com", "3101234567"),  # válido
        ("Ana", "12ab", "ana@correo.com", None),                                # documento inválido
        ("Carlos Pérez", "987654321", "carlos@correo", None),                   # correo inválido
        ("Luis Mora", "1234567890", "luis@correo.com", "12345"),                # teléfono inválido
        ("Otra Persona", "123456789", "yulieth@correo.com", None),              # correo duplicado
    ]
    for datos in casos:
        try:
            c = registro.registrar(*datos)
        except ErrorSistemaPersonalizado as e:
            print(f"  -> Rechazado: {e} (causa: {e.__cause__})")
        else:
            print(f"  -> OK: {c}")
    print(f"Clientes registrados: {len(registro)}")
