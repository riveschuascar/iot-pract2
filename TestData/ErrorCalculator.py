import pandas as pd
import re
import numpy as np
import os 

INPUT_FILE = "Resultados/muestras_filtros.csv"

try:
    # 1. Cargar el archivo
    df = pd.read_csv(INPUT_FILE)
except FileNotFoundError:
    print(f"❌ No se encontró el archivo {INPUT_FILE}")
    exit()

# Eliminar columna 'n' si existe
if "n" in df.columns:
    df = df.drop(columns=["n"])

# 2. Buscar TODAS las columnas de medición (Ej. 5cm_raw, 5cm_sqr, 10cm_lin, etc.)
# El patrón ahora busca dígitos al inicio seguidos de 'cm_' y cualquier otro sufijo
measurement_columns = [c for c in df.columns if re.match(r"^\d+cm_.+$", c)]

if not measurement_columns:
    print("❌ No se encontraron columnas con formato 'Xcm_sufijo' (Ej: 5cm_raw, 10cm_lin).")
    exit()

resultados = []
errores_cuadraticos_combinados = []
all_stats = []

for col in measurement_columns:
    # 3. Extraer la distancia real X (Ej. '5' de '5cm_raw')
    # Buscamos el primer grupo de dígitos al inicio de la columna
    match = re.search(r"^(\d+)", col)
    if not match:
        continue
    x_real = float(match.group(1)) # La distancia real en cm

    # 4. Obtener los valores medidos
    valores = df[col].dropna().astype(float)
    if valores.empty:
        print(f"Advertencia: La columna '{col}' está vacía. Se omite.")
        continue

    # --- Cálculos de Error (MSE y RMSE) ---
    
    # MSE y RMSE específicos para esta columna/tipo
    mse = np.mean((valores - x_real) ** 2)
    rmse = np.sqrt(mse)

    # Error relativo (%) respecto a la distancia real
    err_rel = (rmse / x_real) * 100

    # Guardar resultados de error por columna/tipo
    resultados.append({
        "columna": col,
        "dist_real_cm": x_real,
        "MSE": mse,
        "RMSE": rmse,
        "Error_relativo_%": err_rel
    })

    # Acumular los errores cuadráticos para el cálculo del total combinado
    # Esto combina los errores de *todos* los tipos de medición
    errores_cuadraticos_combinados.extend((valores - x_real) ** 2)
    
    # --- Cálculos de Estadísticas (Promedio y Desviación) ---
    
    # Guardar estadísticas por columna/tipo
    all_stats.append({
        "columna": col,
        "dist_real_cm": x_real,
        "promedio": valores.mean(),
        "desviacion_estandar": valores.std(),
        "error_medio_cm": valores.mean() - x_real,
        "error_relativo_promedio_%": (abs(valores.mean() - x_real) / x_real) * 100
    })


# --- Cálculo de totales combinados (Combinando TODOS los errores de todas las columnas) ---
mse_total_comb = np.mean(errores_cuadraticos_combinados)
rmse_total_comb = np.sqrt(mse_total_comb)

# Error relativo promedio (promedio simple de todos los errores relativos por columna)
relativos = [r["Error_relativo_%"] for r in resultados]
error_relativo_promedio_total = np.mean(relativos)

# --- Mostrar resultados de error ---
print("\n📊 Resultados de Error (MSE, RMSE y %):")
print("-" * 80)
print(f"{'COLUMNA':15s} | {'DIST. REAL':12s} | {'MSE':8s} | {'RMSE (cm)':10s} | {'ERROR (%)':8s}")
print("-" * 80)
for r in resultados:
    print(f"{r['columna']:15s} | {r['dist_real_cm']:12.0f} | {r['MSE']:.4f} | {r['RMSE']:.3f} | {r['Error_relativo_%']:.2f}%")
print("-" * 80)
print(f"🔹 **MSE total combinado** : {mse_total_comb:.4f}")
print(f"🔹 **RMSE total combinado**: {rmse_total_comb:.3f} cm")
print(f"🔹 **Error relativo promedio**: {error_relativo_promedio_total:.2f}% (Promedio simple de los errores por columna)")
print("-" * 80)

# --- Guardar CSV de Errores ---
df_out_errores = pd.DataFrame(resultados)
df_out_errores.loc[len(df_out_errores)] = {
    "columna": "TOTAL COMBINADO",
    "dist_real_cm": np.nan,
    "MSE": mse_total_comb,
    "RMSE": rmse_total_comb,
    "Error_relativo_%": error_relativo_promedio_total
}

new_file_errores = "Resultados/errores_rmse_todos.csv"
df_out_errores.to_csv(new_file_errores, index=False)
print(f"\n✅ Resultados de error guardados en '{new_file_errores}'")

# --- Guardar CSV de Estadísticas ---
new_file_stats = "Resultados/estadisticas_todos.csv"
df_out_stats = pd.DataFrame(all_stats)
df_out_stats.to_csv(new_file_stats, index=False)
print(f"✅ Estadísticas de promedio y desviación guardadas en '{new_file_stats}'")