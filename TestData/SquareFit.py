import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

data = pd.read_csv("estadisticas.csv")

X = data["promedio"].values.reshape(-1,1)
y = data["dist_real"].values

poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)
model = LinearRegression().fit(X_poly, y)
a, b, c = model.coef_[2], model.coef_[1], model.intercept_
print(f"d_real = {a:.8f} * d_meas² + {b:.8f} * d_meas + {c:.8f}")

pd.DataFrame({
    "coeficiente": ["a", "b", "c"],
    "valor": [a, b, c]
}).to_csv("calibracion_coeffs_cuadratico.csv", index=False)