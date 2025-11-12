from .context import get_current_computation
from typing import Callable, Any
import weakref


class Signal:

    def __init__(self, value: Any) -> None:
        """
        self._value           # Valor actual del signal
        self._subscribers     # Conjunto de weakrefs a suscriptores (no usado directamente aquí)
        self._dependents      # Conjunto de weakrefs a objetos que dependen de este signal (Computed/Effect)
        """

        self._value = value
        self._subscribers: set[weakref.ref] = set()
        self._dependents: set[weakref.ref] = set()

    def __call__(self) -> Any:
        """
        - Propósito: Permite leer el valor con signal().
        - Reactividad automática: Si se lee dentro de un Computed o Effect, se registra como dependencia en el contexto activo.
        - Uso de threading.local: Permite aislamiento por hilo (seguro en FastAPI con múltiples workers síncronos).
        """
        current = get_current_computation()
        if current is not None:
            current.add(weakref.ref(self))
        return self._value

    def add_subscriber(self, subscriber: Any) -> None:
        self._subscribers.add(weakref.ref(subscriber))

    def add_dependent(self, dependent: Any) -> None:
        self._dependents.add(weakref.ref(dependent))

    def set(self, new_value: Any) -> None:
        """
        - Optimización crítica: Solo notifica si el valor realmente cambió (igualdad estricta ==).
        - Evita bucles infinitos y recomputaciones innecesarias.
        """
        if self._value == new_value:
            return  # Evita notificaciones innecesarias
        self._value = new_value
        self.notify()

    def update(self, fn: Callable[[Any], Any]) -> None:
        """
        - Patrón funcional: Ideal para contadores, listas, etc.
        - Ejemplo: counter.update(lambda x: x + 1)
        """
        new_value = fn(self._value)
        self._value = new_value

    def notify(self) -> None:
        """
        - Usa referencias débiles (weakref) para evitar fugas de memoria.
        - Llama a _schedule_update() en cada dependiente → permite que Computed marque como "dirty" y Effect se ejecute.
        """
        for weak_dep in self._dependents:
            dependent = weak_dep()
            if dependent:
                dependent._schedule_update()
