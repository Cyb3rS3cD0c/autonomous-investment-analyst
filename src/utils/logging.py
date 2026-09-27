"""Consistent, non-secret logging for the application."""
from __future__ import annotations

import logging
import os


def configure_logging(level: str | None = None) -> logging.Logger:
    """Configure the package logger once and return it."""
    logger = logging.getLogger("investment_analyst")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        logger.addHandler(handler)
        logger.propagate = False
    logger.setLevel((level or os.getenv("LOG_LEVEL", "INFO")).upper())
    return logger


def get_logger(name: str) -> logging.Logger:
    """Return a child logger after applying the package configuration."""
    configure_logging()
    return logging.getLogger(f"investment_analyst.{name}")
