# guardar como calibrate.py y ejecutar con python3 calibrate.py tus_datos.csv
import numpy as np
import pandas as pd
import sys

fn = sys.argv[1] if len(sys.argv)>1 else "Resultados/muestras.csv"
df = pd.read_csv(fn)

# Define aquí las distancias reales (en el mismo orden que las columnas)
# Si tus columnas se llaman dist_5cm, dist_10cm,... extraemos el número
cols = [c for c in df.columns if c.startswith('dist_')]
meas = []
true = []
for c in cols:
    # parsea 5 de 'dist_5cm'
    cm = int(''.join(ch for ch in c if ch.isdigit()))
    # toma la media ignorando NaN
    m = df[c].replace(-1, np.nan).dropna().astype(float)
    if len(m)==0: continue
    # agregamos pares para cada lectura (meas, true)
    meas.extend(m.values.tolist())
    true.extend([cm]*len(m))

meas = np.array(meas)
true = np.array(true)

# Ajuste lineal por mínimos cuadrados
A = np.vstack([meas, np.ones_like(meas)]).T
a, b = np.linalg.lstsq(A, true, rcond=None)[0]
pred = a*meas + b
mse_total = np.mean((pred - true)**2)

print(f"a = {a:.6f}, b = {b:.6f}, MSE = {mse_total:.6f}")

pd.DataFrame({
    "coeficiente": ["a", "b"],
    "valor": [a, b]
}).to_csv("calibracion_coeffs_lineal.csv", index=False)
