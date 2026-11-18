"""Clase abstracta base y clase Cliente (con encapsulación y validaciones)."""
import re                      # Expresiones regulares para validar el correo
from abc import ABC, abstractmethod

from excepciones import ClienteInvalidoError
from logger import log


class Entidad(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    _contador = 0  # Contador compartido para asignar identificadores únicos

    def __init__(self):
        Entidad._contador += 1       # Incrementa el contador global
        self._id = Entidad._contador  # Asigna el id a esta entidad

    @property
    def id(self):
        """Identificador de solo lectura."""
        return self._id

    @abstractmethod
    def describir(self):
        """Cada entidad debe describirse a sí misma (método abstracto)."""


class Cliente(Entidad):
    """Cliente de Software FJ con datos personales encapsulados."""

    def __init__(self, nombre, correo, telefono):
        # Se validan los datos ANTES de crear el id, así un cliente inválido no consume id
        self.nombre = nombre      # Usa el setter con validación
        self.correo = correo      # Usa el setter con validación
        self.telefono = telefono  # Usa el setter con validación
        super().__init__()
        log.info(f"Cliente creado: id={self.id}, nombre={self.__nombre}")

    # ---- Atributos privados (__) accesibles solo mediante propiedades ----
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(f"Nombre inválido: {valor!r} (mínimo 3 caracteres)")
        self.__nombre = valor.strip()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        patron = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"  # Formato básico usuario@dominio.ext
        if not isinstance(valor, str) or not re.match(patron, valor):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")
        self.__correo = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not isinstance(valor, str) or not valor.isdigit() or not 7 <= len(valor) <= 10:
            raise ClienteInvalidoError(f"Teléfono inválido: {valor!r} (7 a 10 dígitos)")
        self.__telefono = valor

    def describir(self):
        """Implementación del método abstracto de Entidad."""
        return f"Cliente #{self.id}: {self.__nombre} <{self.__correo}> Tel: {self.__telefono}"
