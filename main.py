"""Simulación de 12 operaciones: válidas e inválidas. El programa nunca se detiene."""
from excepciones import SoftwareFJError
from logger import log, RUTA_LOG
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reservas import GestorReservas

gestor = GestorReservas()  # Almacén en memoria (listas)
ctx = {}                   # Guarda objetos entre operaciones


def ejecutar(numero, titulo, accion):
    """Ejecuta una operación capturando cualquier error para no detener el programa."""
    print(f"\n[{numero}] {titulo}")
    try:
        resultado = accion()
    except SoftwareFJError as error:
        log.error(f"Operación {numero} ({titulo}): {error}")
        print(f"   ❌ Error controlado: {error}")
        if error.__cause__:  # Muestra la causa original si hubo encadenamiento
            print(f"      Causa: {error.__cause__}")
    except Exception as error:  # Cualquier error inesperado también se controla
        log.critical(f"Operación {numero} ({titulo}) error inesperado: {error!r}")
        print(f"   ⚠️ Error inesperado controlado: {error!r}")
    else:
        log.info(f"Operación {numero} ({titulo}) exitosa")
        print(f"   ✅ {resultado}")
    finally:
        log.info(f"Fin de la operación {numero}")


def op1():
    ctx["ana"] = gestor.registrar_cliente("Ana Torres", "ana@correo.com", "3001234567")
    return ctx["ana"].describir()


def op2():  # Correo inválido
    return gestor.registrar_cliente("Luis Pérez", "luis-sin-arroba", "3109876543")


def op3():  # Datos vacíos / faltantes
    return gestor.registrar_cliente("", "x@correo.com", "3001112233")


def op4():
    ctx["sala"] = gestor.registrar_servicio(ReservaSala("Sala Innovación", 50000, 12))
    return ctx["sala"].describir()


def op5():  # Tarifa negativa
    return gestor.registrar_servicio(ReservaSala("Sala Fantasma", -5000, 10))


def op6():
    ctx["equipo"] = gestor.registrar_servicio(AlquilerEquipo("Proyector HD", 15000, 2))
    ctx["asesoria"] = gestor.registrar_servicio(Asesoria("Asesoría en Python", 80000, "senior"))
    return f"{ctx['equipo'].describir()} | {ctx['asesoria'].describir()}"


def op7():  # Reserva exitosa
    ctx["r1"] = gestor.crear_reserva(ctx["ana"], ctx["sala"], 3)
    costo = ctx["r1"].procesar(impuesto=0.19)
    return f"{ctx['r1'].describir()} | Costo con IVA: ${costo}"


def op8():  # Servicio no disponible
    ctx["equipo"].disponible = False
    reserva = gestor.crear_reserva(ctx["ana"], ctx["equipo"], 5)
    return reserva.procesar()


def op9():  # Cancelar dos veces
    ctx["r1"].cancelar()
    ctx["r1"].cancelar()
    return "No debería llegar aquí"


def op10():  # Costo con descuento válido
    costo = ctx["asesoria"].calcular_costo(2, 0.19, 0.10)
    return f"Asesoría senior 2 h con IVA y 10% descuento: ${costo}"


def op11():  # Descuento inválido (encadenamiento ValueError -> CalculoInconsistenteError)
    return ctx["asesoria"].calcular_costo(2, 0.19, 1.5)


def op12():  # Duración inválida para una asesoría
    reserva = gestor.crear_reserva(ctx["ana"], ctx["asesoria"], 10)
    return reserva.procesar()


if __name__ == "__main__":
    print("=== Software FJ: Sistema de Gestión de Clientes, Servicios y Reservas ===")
    operaciones = [
        ("Registrar cliente válido", op1), ("Cliente con correo inválido", op2),
        ("Cliente con datos vacíos", op3), ("Crear servicio de sala válido", op4),
        ("Servicio con tarifa negativa", op5), ("Crear equipo y asesoría válidos", op6),
        ("Reserva exitosa", op7), ("Reserva con servicio no disponible", op8),
        ("Cancelar una reserva ya cancelada", op9), ("Costo con descuento válido", op10),
        ("Costo con descuento inválido", op11), ("Reserva con duración inválida", op12),
    ]
    for i, (titulo, funcion) in enumerate(operaciones, start=1):
        ejecutar(i, titulo, funcion)
    print(f"\n=== Fin: el programa terminó sin interrupciones. Log en: {RUTA_LOG} ===")
    print(f"Clientes: {len(gestor.clientes)} | Servicios: {len(gestor.servicios)} | "
          f"Reservas: {len(gestor.reservas)}")
