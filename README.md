# signal

Signal A ──→ Computed X ──→ Effect Z ↑ (lee A) (lee X) Signal B ──→ (lee A y B)
(imprime, envía WS, etc.)

Flujo de Actualización

1. Signal A.set(10)
2. A.\_notify() → llama a X.\_schedule_update()
3. X marca \_dirty = True
4. Al leer X(), se ejecuta \_eval() → recalcula → notifica a Z
5. Z.\_schedule_update() → ejecuta su función

Reactividad granular: Solo se recalcula lo necesario.
