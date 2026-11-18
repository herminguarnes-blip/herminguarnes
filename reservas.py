"""Clase Reserva y gestor general (todo se guarda en listas, sin base de datos)."""
from entidades import Entidad, Cliente
from servicios import Servicio
from excepciones import (ReservaInvalidaError, ServicioNoDisponibleError,
                         ServicioInvalidoError)
from logger import log


class Reserva(Entidad):
    """Integra cliente, servicio, duración y estado."""

    PENDIENTE, CONFIRMADA, CANCELADA = "PENDIENTE", "CONFIRMADA", "CANCELADA"

    def __init__(self, cliente, servicio, horas):
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un cliente válido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un servicio válido")
        super().__init__()
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = Reserva.PENDIENTE  # Toda reserva nace pendiente

    def confirmar(self):
        """Confirma la reserva usando try/except/else/finally."""
        try:
            if self.estado != Reserva.PENDIENTE:
                raise ReservaInvalidaError(
                    f"Reserva #{self.id} no se puede confirmar (estado: {self.estado})")
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self.servicio.nombre}' no está disponible")
            self.servicio.validar_parametros(self.horas)
        except ServicioInvalidoError as error:
            # Encadenamiento: error de servicio -> error de reserva (conserva la causa)
            raise ReservaInvalidaError(f"Reserva #{self.id} con parámetros inválidos") from error
        else:
            self.estado = Reserva.CONFIRMADA  # Solo si todo salió bien
            log.info(f"Reserva #{self.id} CONFIRMADA")
        finally:
            log.info(f"Intento de confirmación de reserva #{self.id} finalizado")

    def cancelar(self):
        """Cancela la reserva (no se puede cancelar dos veces)."""
        try:
            if self.estado == Reserva.CANCELADA:
                raise ReservaInvalidaError(f"Reserva #{self.id} ya estaba cancelada")
        except ReservaInvalidaError:
            raise  # Se relanza para que lo maneje quien la llamó
        else:
            self.estado = Reserva.CANCELADA
            log.info(f"Reserva #{self.id} CANCELADA")
        finally:
            log.info(f"Intento de cancelación de reserva #{self.id} finalizado")

    def procesar(self, impuesto=0.19, descuento=0.0):
        """Confirma la reserva y devuelve su costo final."""
        self.confirmar()
        costo = self.servicio.calcular_costo(self.horas, impuesto, descuento)
        log.info(f"Reserva #{self.id} procesada. Costo total: ${costo}")
        return costo

    def describir(self):
        return (f"Reserva #{self.id} [{self.estado}] {self.cliente.nombre} -> "
                f"{self.servicio.nombre} ({self.horas} h)")


class GestorReservas:
    """Administra las listas internas de clientes, servicios y reservas."""

    def __init__(self):
        self.clientes, self.servicios, self.reservas = [], [], []

    def registrar_cliente(self, nombre, correo, telefono):
        cliente = Cliente(nombre, correo, telefono)  # Puede lanzar ClienteInvalidoError
        self.clientes.append(cliente)
        return cliente

    def registrar_servicio(self, servicio):
        self.servicios.append(servicio)
        log.info(f"Servicio registrado: {servicio.describir()}")
        return servicio

    def crear_reserva(self, cliente, servicio, horas):
        reserva = Reserva(cliente, servicio, horas)
        self.reservas.append(reserva)
        log.info(f"Reserva creada: {reserva.describir()}")
        return reserva
