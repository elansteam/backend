from .config_model import Config


config = Config.load()

__all__ = [
    "config"
]
