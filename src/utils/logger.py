import logging
import sys

def setup_logger(name: str = "ConversaSense"):
    """Configura el logger estándar para el proyecto."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Formato de los logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(console_handler)
        
    return logger

# Instancia global para uso rápido
logger = setup_logger()
