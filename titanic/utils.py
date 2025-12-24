"""
titanic.utils

Сейчас здесь находятся утилиты для логирования и другие вспомогательные функции.
"""

from contextlib import contextmanager
from functools import wraps
from time import time

from loguru import logger


# Декоратор для логирования функций
def log_execution(func):
    """Логирует выполнение функции с временем и результатом."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Starting: {func.__name__}")
        start = time()
        try:
            result = func(*args, **kwargs)
            elapsed = time() - start
            logger.info(f"Completed: {func.__name__} ({elapsed:.2f}s)")
            return result
        except Exception as e:
            logger.error(f"Failed: {func.__name__} - {e}")
            raise

    return wrapper


# Контекстный менеджер для логирования блоков кода
@contextmanager
def log_stage(stage_name: str):
    """Логирует начало и конец этапа обработки."""
    logger.info(f"🔄 Stage: {stage_name}")
    start = time()
    try:
        yield
        elapsed = time() - start
        logger.info(f"✓ {stage_name} completed ({elapsed:.2f}s)")
    except Exception as e:
        logger.error(f"✗ {stage_name} failed: {e}")
        raise
