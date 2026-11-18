"""Clase abstracta Servicio y tres servicios especializados (polimorfismo)."""
from abc import abstractmethod

from entidades import Entidad
from excepciones import ServicioInvalidoError, CalculoInconsistenteError
from logger import log


class Servicio(Entidad):
    """Servicio abstracto: define lo que todo servicio debe implementar."""

    def __init__(self, nombre, tarifa_hora):
        # Validaciones comunes a todos los servicios
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El nombre del servicio no puede estar vacío")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa inválida: {tarifa_hora!r} (debe ser > 0)")
        super().__init__()
        self.nombre = nombre.strip()
        self.tarifa_hora = tarifa_hora
        self.disponible = True  # Un servicio nuevo está disponible

    @abstractmethod
    def calcular_costo_base(self, horas):
        """Costo sin impuestos ni descuentos (cada hijo lo sobrescribe)."""

    @abstractmethod
    def validar_parametros(self, horas):
        """Valida la duración solicitada (cada hijo lo sobrescribe)."""

    @abstractmethod
    def describir(self):
        """Descripción del servicio (cada hijo lo sobrescribe)."""

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        """Método 'sobrecargado': se puede llamar con 1, 2 o 3 argumentos.

        calcular_costo(3)              -> costo base
        calcular_costo(3, 0.19)        -> con impuesto
        calcular_costo(3, 0.19, 0.10)  -> con impuesto y descuento
        """
        try:
            if not 0 <= descuento < 1:
                raise ValueError(f"descuento fuera de rango: {descuento}")
            if impuesto < 0:
                raise ValueError(f"impuesto negativo: {impuesto}")
            self.validar_parametros(horas)
            total = self.calcular_costo_base(horas) * (1 - descuento) * (1 + impuesto)
        except (TypeError, ValueError) as error:
            # Encadenamiento: se relanza una excepción propia conservando la causa original
            raise CalculoInconsistenteError(
                f"No se pudo calcular el costo de '{self.nombre}': {error}") from error
        else:
            return round(total, 2)  # Solo se ejecuta si no hubo errores


class ReservaSala(Servicio):
    """Servicio 1: reserva de salas."""

    def __init__(self, nombre, tarifa_hora, capacidad):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}")
        self.capacidad = capacidad

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 8:
            raise ServicioInvalidoError(f"Una sala se reserva de 1 a 8 horas (recibido: {horas!r})")

    def calcular_costo_base(self, horas):
        return self.tarifa_hora * horas

    def describir(self):
        return f"Sala '{self.nombre}' para {self.capacidad} personas, ${self.tarifa_hora}/hora"


class AlquilerEquipo(Servicio):
    """Servicio 2: alquiler de equipos."""

    def __init__(self, nombre, tarifa_hora, cantidad):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ServicioInvalidoError(f"Cantidad inválida: {cantidad!r}")
        self.cantidad = cantidad

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 24:
            raise ServicioInvalidoError(f"Un equipo se alquila de 1 a 24 horas (recibido: {horas!r})")

    def calcular_costo_base(self, horas):
        return self.tarifa_hora * horas * self.cantidad  # Cuesta más según la cantidad

    def describir(self):
        return f"Equipo '{self.nombre}' x{self.cantidad}, ${self.tarifa_hora}/hora c/u"


class Asesoria(Servicio):
    """Servicio 3: asesorías especializadas."""

    def __init__(self, nombre, tarifa_hora, nivel):
        super().__init__(nombre, tarifa_hora)
        if nivel not in ("junior", "senior"):
            raise ServicioInvalidoError(f"Nivel inválido: {nivel!r} (junior o senior)")
        self.nivel = nivel

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 4:
            raise ServicioInvalidoError(f"Una asesoría dura de 1 a 4 horas (recibido: {horas!r})")

    def calcular_costo_base(self, horas):
        recargo = 1.5 if self.nivel == "senior" else 1.0  # El asesor senior cuesta 50% más
        return self.tarifa_hora * horas * recargo

    def describir(self):
        return f"Asesoría '{self.nombre}' nivel {self.nivel}, ${self.tarifa_hora}/hora"
