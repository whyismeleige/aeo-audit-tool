import logging
import os
from app.config import get_settings

def get_logger(name: str) -> logging.Logger:
    settings = get_settings()
    
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    numeric_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(numeric_level)
    
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    os.makedirs("logs", exist_ok=True)
    file_handler = logging.FileHandler(filename="logs/aeo-audit.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    logger.propagate = False
    
    return logger
