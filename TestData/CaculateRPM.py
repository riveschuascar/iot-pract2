import pandas as pd
import numpy as np

# === Configuración ===
INPUT_FILE = "Resultados/tiempos_30vueltas.csv"     # Archivo original
OUTPUT_FILE = "Resultados/servo_rpm_stats.csv"
CRONO_PRECISION = 0.01             # Precisión del cronómetro (segundos)

# === Leer CSV ===
try:
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    print(f"❌ No se encontró el archivo {INPUT_FILE}")
    exit()

# Verificar columnas mínimas necesarias
if not {"n", "vueltas"}.issubset(df.columns):
    print("❌ El archivo debe contener las columnas 'n' y 'vueltas'.")
    exit()

# === Detectar columnas de tiempo ===
time_columns = [c for c in df.columns if c.startswith("t_s_")]
if not time_columns:
    print("❌ No se encontraron columnas con formato 't_s_xxx'.")
    exit()

# === Calcular promedios de tiempo, RPS, RPM y errores ===
results = []

for col in time_columns:
    label = col.replace("t_s_", "")  # ej: "t_s_500" → "500"

    vueltas = df["vueltas"].mean()
    t_mean = df[col].mean()

    # RPS y RPM promedio
    rps = vueltas / t_mean
    rpm = rps * 60

    # Errores por propagación
    rps_error = vueltas / (t_mean ** 2) * CRONO_PRECISION
    rpm_error = rps_error * 60

    results.append({
        "test": label,
        "vueltas_prom": vueltas,
        "t_prom_s": t_mean,
        "rps": rps,
        "rps_error": rps_error,
        "rpm": rpm,
        "rpm_error": rpm_error
    })

# === Guardar resultados ===
df_out = pd.DataFrame(results)
df_out.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

# === Mostrar en consola ===
print("📊 Resultados promedios (basado en tiempos medios y Δt=0.01 s):\n")
print(df_out.round(4))
print(f"\n✅ Archivo generado: {OUTPUT_FILE}")
