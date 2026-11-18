"""Configuración del archivo de logs (único archivo que usa el sistema)."""
import logging  # Módulo estándar de Python para registrar eventos
import os       # Para construir rutas de archivos

# Ruta del log: carpeta "logs" junto a este archivo
RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "eventos.log")


def obtener_logger():
    """Crea (una sola vez) el logger que escribe en logs/eventos.log."""
    os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)  # Crea la carpeta si no existe
    logger = logging.getLogger("software_fj")              # Logger con nombre propio
    if not logger.handlers:                                # Evita duplicar manejadores
        logger.setLevel(logging.INFO)                      # Registra INFO, WARNING, ERROR...
        # mode="w": cada ejecución empieza con un log limpio (evidencia clara)
        manejador = logging.FileHandler(RUTA_LOG, mode="w", encoding="utf-8")
        manejador.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(manejador)                       # Conecta el formato al archivo
    return logger


log = obtener_logger()  # Logger compartido por todos los módulos
