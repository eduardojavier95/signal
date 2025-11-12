import threading
import weakref


_local = threading.local()


def get_current_computation() -> set[weakref.ref]:
    return getattr(_local, "current_computation", set())


def set_current_computation(computation: set[weakref.ref]) -> None:
    _local.current_computation = computation


def clear_current_computation() -> None:
    if hasattr(_local, "current_computation"):
        del _local.current_computation
