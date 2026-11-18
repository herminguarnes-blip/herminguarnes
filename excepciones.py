"""Excepciones personalizadas del sistema Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base: todas las demás heredan de ella."""


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no son válidos."""


class ServicioInvalidoError(SoftwareFJError):
    """Se lanza cuando los parámetros de un servicio no son válidos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio no disponible."""


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza ante operaciones de reserva incorrectas o no permitidas."""


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo de costo produce datos inconsistentes."""
