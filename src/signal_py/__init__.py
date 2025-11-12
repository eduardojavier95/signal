# src/signal_py/__init__.py
from .core import Signal, Computed, Effect  # ← importa desde el submódulo

__all__ = ["Signal", "Computed", "Effect"]
__version__ = "0.1.0"
