"""UUID validation utilities for area loop tools."""

import inspect
import logging
import uuid
from functools import wraps
from typing import Callable

logger = logging.getLogger(__name__)


def _str_to_uuid(value: str | None) -> uuid.UUID | None:
    if value is None:
        return None
    return uuid.UUID(value)


def _validate_uuid(value: str | None, name: str) -> None:
    if value is None:
        return
    try:
        uuid.UUID(value)
    except ValueError as exc:
        logger.warning("Invalid UUID input", extra={"param": name})
        raise ValueError(f"Invalid UUID for {name}: {value}") from exc


def validate_uuid_args(*param_names: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        sig = inspect.signature(func)
        param_list = list(sig.parameters.keys())

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Validate keyword arguments
            for name in param_names:
                if name in kwargs:
                    _validate_uuid(kwargs[name], name)

            # Validate positional arguments
            for i, arg in enumerate(args):
                if i < len(param_list) and param_list[i] in param_names:
                    _validate_uuid(arg, param_list[i])

            return func(*args, **kwargs)

        return wrapper

    return decorator
