import weakref
from typing import Callable, Any
from .context import set_current_computation, get_current_computation, clear_current_computation

"""

Decisión                |   Justificación
Ejecución inmediata     |   Igual que Angular: el efecto se ejecuta al crearse para inicializar estado.
Soporte para cleanup    |   "Permite return () => cleanup_fn, útil para WebSockets, timers, etc."
No hereda de Signal     |   Un Effect no es un valor. No debe usarse en expresiones reactivas.
Re-ejecución inmediata  |   Los efectos secundarios deben reflejarse lo antes posible (no lazy).

"""


class Effect:
    def __init__(self, fn: Callable[[], Any]):
        self._fn = fn
        self._dirty = True
        self._last_deps: set[weakref.ref] = set()
        self._run()  # Ejecuta inmediatamente (como en Angular)

    def _run(self) -> None:

        deps = set()
        set_current_computation(deps)
        try:
            result = self._fn()
            if callable(result):
                result()  # Cleanup si se proporciona
        finally:
            clear_current_computation()

        # Registrar dependencias como en Computed
        self._last_deps = get_current_computation().copy()
        for weak_dep in self._last_deps:
            dep = weak_dep()
            if dep:
                dep._add_dependent(self)

        self._dirty = False

    def _schedule_update(self) -> None:
        if not self._dirty:
            self._dirty = True
            self._run()
