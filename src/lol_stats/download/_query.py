"""Module to query till request is complete."""

import time
from collections.abc import Callable
from typing import Any

from requests import exceptions

from lol_stats import logging

_LOGGER = logging.create_colored_logger(__name__)


def query(
    command: Callable,
    args: list[Any] = [],  # noqa: B006
    kwargs: dict[Any, Any] = {},  # noqa: B006
) -> dict:
    while True:
        try:
            return command(*args, **kwargs)
        except exceptions.HTTPError as error:
            _LOGGER.info(
                msg=(
                    "Waiting for 120 seconds for the next request.\n"
                    "This is likely required because because you exceeded your limit."
                ),
            )
            _LOGGER.debug(str(error))
            time.sleep(120)
