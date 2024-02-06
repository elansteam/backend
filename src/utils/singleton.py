"""Definition singleton class"""
from __future__ import annotations
from typing import Any


class Singleton:
    """Base class for singletons"""
    __instance: Singleton | None = None

    def __new__(cls, *args: list[Any], **kwargs: dict[str, Any]) -> Singleton:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance
