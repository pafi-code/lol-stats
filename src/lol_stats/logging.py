"""Module for logging in this package."""

import logging

import colorlog


def create_colored_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """
    Create a logger with colored logs.

    Parameters
    ----------
    name
        Name of the logger.
    level
        The log level of the logger.


    Returns
    -------
    logging.Logger
        The corresponding logger.
    """
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s %(levelname)s: %(name)s: %(message)s",
        ),
    )
    logger = colorlog.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger
