# main.py
from signal_py import Signal, Computed, Effect  # ¡Ahora sí!
import time

print("=== SISTEMA DE SEÑALES REACTIVAS EN ACCIÓN ===\n")

# --- Estado reactivo ---
temperature = Signal(20)  # °C
humidity = Signal(50)  # %
is_raining = Signal(False)

# --- Valores derivados ---
heat_index = Computed(lambda: temperature() + (0.5 * humidity() if humidity() > 40 else 0))

comfort_level = Computed(lambda: "Cómodo" if 18 <= temperature() <= 25 and not is_raining() else "Incómodo")

# --- Efectos secundarios ---
Effect(lambda: print(f"🌡️  Temperatura: {temperature()}°C"))
Effect(lambda: print(f"💧 Humedad: {humidity()}%"))
Effect(lambda: print(f"☂️  {'Lluvia' if is_raining() else 'Seco'}"))

Effect(lambda: print(f"🔥 Índice de calor: {heat_index():.1f}"))

Effect(lambda: print(f"😊 Nivel de confort: {comfort_level()}"))

# --- Simulación de cambios en el tiempo ---
print("\n--- Iniciando simulación ---\n")
time.sleep(1)

print("→ Subiendo temperatura a 28°C")
temperature.set(28)
time.sleep(1)

print("→ Aumentando humedad a 70%")
humidity.set(70)
time.sleep(1)

print("→ ¡Comienza a llover!")
is_raining.set(True)
time.sleep(1)

print("→ Temperatura baja a 22°C")
temperature.set(22)
time.sleep(1)

print("→ Lluvia cesa")
is_raining.set(False)

print("\n=== FIN DE LA SIMULACIÓN ===")
