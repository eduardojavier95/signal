from .context import clear_current_computation, set_current_computation
from .signal import Signal
import weakref
from typing import Callable, Any


class Computed(Signal):

    def __init__(self, fn: Callable[[], Any]) -> None:
        """
        self._fn          # Función que calcula el valor
        self._dirty       # Bandera: ¿necesita recalcularse?
        self._last_deps   # Conjunto de weakrefs a señales leídas en la última evaluación
        """
        super().__init__(None)

        self._fn = fn
        self._dirty = True
        self._last_deps: set[weakref.ref] = set()
        self._eval()

    def __call__(self) -> Any:
        """
        - Lazy evaluation: Solo se recalcula si está "sucio".
        - Garantiza que el valor esté siempre actualizado al leerlo.
        """

        if self._dirty:
            self._eval()
        return super().__call__()

    def _eval(self) -> None:
        """
        Limpiar dependencias previas
        """

        # 1. Limpiar dependencias antiguas
        for weak_dep in self._last_deps:
            dep = weak_dep()
            if dep:
                dep._remove_dependent(self)

        # 2. Preparar nuevo conjunto de dependencias
        deps: set[weakref.ref] = set()
        set_current_computation(deps)  # ← ¡Pasa deps!
        try:
            new_value = self._fn()
        finally:
            clear_current_computation()

        # 3. Registrar nuevas dependencias
        self._last_deps = deps.copy()
        for weak_dep in self._last_deps:
            dep = weak_dep()
            if dep:
                dep.add_dependent(self)
        # 4. Actualizar valor
        super().set(new_value)
        self._dirty = False

    def _schedule_update(self) -> None:
        self._dirty = True
