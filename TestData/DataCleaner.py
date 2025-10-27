import pandas as pd
import random
import os

# === Configuración inicial ===
INPUT_FILE = "datos_serial.csv"
OUTPUT_FILE = "Resultados/muestras_filtros.csv"

# === Selección de tipo de datos ===
print("Tipos disponibles: raw | sqr | lin")
tipo = input("Ingrese el tipo de archivo a procesar: ").strip().lower()

tipo_a_columna = {
    "raw": "data_raw",
    "sqr": "data_sqr",
    "lin": "data_lin"
}

if tipo not in tipo_a_columna:
    print("❌ Tipo no válido. Debe ser: raw, sqr o lin.")
    exit()

columna_datos = tipo_a_columna[tipo]

# === Nombre de la columna de salida ===
COLUMN_NAME = input("Nombre de columna para los datos (ej: dist_5cm): ").strip()

# === Leer archivo CSV original ===
try:
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    print(f"❌ No se encontró el archivo {INPUT_FILE}")
    exit()

# === Validar columna seleccionada ===
if columna_datos not in df.columns:
    print(f"❌ La columna '{columna_datos}' no existe en {INPUT_FILE}.")
    exit()

# === Filtrar solo datos numéricos válidos ===
df["valor"] = pd.to_numeric(df[columna_datos], errors="coerce")
df = df.dropna(subset=["valor"])

if len(df) == 0:
    print("❌ No hay datos numéricos válidos en la columna seleccionada.")
    exit()

# === Seleccionar 150 filas aleatorias ===
sample_size = min(150, len(df))
df_sample = df.sample(n=sample_size, random_state=random.randint(0, 9999)).reset_index(drop=True)

# === Crear o actualizar archivo de salida ===
if not os.path.exists(OUTPUT_FILE):
    df_out = pd.DataFrame({
        "n": range(1, len(df_sample) + 1),
        COLUMN_NAME: df_sample["valor"]
    })
else:
    df_out = pd.read_csv(OUTPUT_FILE)

    # Ajustar tamaño si no coincide
    if len(df_out) != len(df_sample):
        print("⚠️ Tamaño de muestra distinto, ajustando filas...")
        df_out = pd.DataFrame({"n": range(1, len(df_sample) + 1)})

    df_out[COLUMN_NAME] = df_sample["valor"].values

# === Guardar resultados ===
df_out.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print(f"✅ Archivo actualizado correctamente: {OUTPUT_FILE}")
print(f"📊 {len(df_sample)} muestras válidas guardadas en la columna '{COLUMN_NAME}'.")
print(f"🔹 Tipo de datos procesado: {tipo.upper()} ({columna_datos})")
