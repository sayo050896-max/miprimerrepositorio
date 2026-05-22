# =============================================================================
#  GUÍA DE LABORATORIO: Procesamiento Estadístico con Python
#  Materia: Estadística Descriptiva
# =============================================================================

# ─────────────────────────────────────────────────────────────────────────────
# FASE 1: Preparación del Entorno e Ingesta de Datos
# ─────────────────────────────────────────────────────────────────────────────

# 1.1 Carga de Librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

print("=" * 60)
print("  LABORATORIO: PROCESAMIENTO ESTADÍSTICO CON PYTHON")
print("=" * 60)

# 1.2 Carga de Datos desde CSV
ruta_csv = "datos_academicos.csv"
df = pd.read_csv(ruta_csv)

print("\n📂 FASE 1: Ingesta de Datos")
print(f"  ✔ Archivo cargado: {ruta_csv}")
print(f"  ✔ Registros encontrados: {len(df)}")
print(f"  ✔ Columnas: {list(df.columns)}")
print("\nPrimeras 5 filas del dataset:")
print(df.head().to_string(index=False))

# Crear carpeta para guardar los gráficos
os.makedirs("graficos", exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# FASE 2: Variables Cualitativas (Nominales) — Método de Conteo
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  FASE 2: Variables Cualitativas — 'carrera' y 'estado'")
print("=" * 60)

# Tabla de frecuencias para 'carrera'
freq_carrera = df["carrera"].value_counts().reset_index()
freq_carrera.columns = ["Carrera", "Frec. Absoluta"]
freq_carrera["Frec. Relativa"] = freq_carrera["Frec. Absoluta"] / len(df)
freq_carrera["Frec. Porcentual (%)"] = (freq_carrera["Frec. Relativa"] * 100).round(2)
freq_carrera = freq_carrera.sort_values("Carrera").reset_index(drop=True)

print("\n📊 Tabla de Frecuencias — Variable: CARRERA")
print(freq_carrera.to_string(index=False))

# Tabla de frecuencias para 'estado'
freq_estado = df["estado"].value_counts().reset_index()
freq_estado.columns = ["Estado", "Frec. Absoluta"]
freq_estado["Frec. Relativa"] = freq_estado["Frec. Absoluta"] / len(df)
freq_estado["Frec. Porcentual (%)"] = (freq_estado["Frec. Relativa"] * 100).round(2)

print("\n📊 Tabla de Frecuencias — Variable: ESTADO")
print(freq_estado.to_string(index=False))

# ─────────────────────────────────────────────────────────────────────────────
# FASE 3: Variables Cuantitativas Discretas — Lógica de Acumulación
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  FASE 3: Variables Cuantitativas Discretas — 'materias_aprobadas'")
print("=" * 60)

freq_materias = df["materias_aprobadas"].value_counts().sort_index().reset_index()
freq_materias.columns = ["Materias Aprobadas", "Frec. Absoluta"]
freq_materias["Frec. Relativa"] = freq_materias["Frec. Absoluta"] / len(df)
freq_materias["Frec. Abs. Acumulada"] = freq_materias["Frec. Absoluta"].cumsum()
freq_materias["Frec. Rel. Acumulada"] = freq_materias["Frec. Relativa"].cumsum().round(4)

print("\n📊 Tabla de Frecuencias — Variable: MATERIAS APROBADAS")
print(freq_materias.to_string(index=False))

# ─────────────────────────────────────────────────────────────────────────────
# FASE 4: Datos Agrupados — Algoritmo de Sturges (variable: 'edad')
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  FASE 4: Datos Agrupados — Algoritmo de Sturges (edad)")
print("=" * 60)

# PASO A: Cálculo de Parámetros Críticos
n        = len(df)
k        = int(np.ceil(1 + 3.322 * np.log10(n)))   # Regla de Sturges
rango    = df["edad"].max() - df["edad"].min()
amplitud = np.ceil(rango / k)

print(f"\n  n (total datos)   = {n}")
print(f"  k (# intervalos)  = {k}  →  1 + 3.322 × log10({n})")
print(f"  Rango             = {rango}  ({df['edad'].max()} − {df['edad'].min()})")
print(f"  Amplitud (c)      = {amplitud}  →  ⌈{rango}/{k}⌉")

# PASO B: Segmentación y Marca de Clase con pd.cut
lim_inf  = df["edad"].min()
lim_sup  = lim_inf + k * amplitud
bins     = np.arange(lim_inf, lim_sup + amplitud, amplitud)

df["intervalo"] = pd.cut(df["edad"], bins=bins, right=False, include_lowest=True)
df["marca_clase"] = df["intervalo"].apply(lambda x: (x.left + x.right) / 2)

tabla_sturges = df.groupby("intervalo", observed=True).size().reset_index(name="Frec. Absoluta")
tabla_sturges["Marca de Clase"] = tabla_sturges["intervalo"].apply(
    lambda x: (x.left + x.right) / 2
)
tabla_sturges["Frec. Relativa"]      = (tabla_sturges["Frec. Absoluta"] / n).round(4)
tabla_sturges["Frec. Abs. Acum."]   = tabla_sturges["Frec. Absoluta"].cumsum()
tabla_sturges["Frec. Rel. Acum."]   = tabla_sturges["Frec. Relativa"].cumsum().round(4)
tabla_sturges.columns = ["Intervalo", "Fi", "Xi", "hi", "Fi acum.", "hi acum."]

print("\n📊 Tabla de Frecuencias por Intervalos — Variable: EDAD")
print(tabla_sturges.to_string(index=False))

# ─────────────────────────────────────────────────────────────────────────────
# FASE 5: Visualización con Matplotlib
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  FASE 5: Generando gráficos...")
print("=" * 60)

# Paleta de colores
COLORES = ["#2563EB", "#7C3AED", "#DC2626", "#D97706", "#16A34A"]

# ── Figura 1: Gráfico de Barras (carrera — cualitativa) ──────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(
    freq_carrera["Carrera"],
    freq_carrera["Frec. Absoluta"],
    color=COLORES[:len(freq_carrera)],
    edgecolor="white",
    linewidth=1.2,
    width=0.55,
)
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.2,
        str(int(bar.get_height())),
        ha="center", va="bottom", fontsize=11, fontweight="bold"
    )
ax.set_title("Distribución por Carrera\n(Variable Cualitativa Nominal)", fontsize=13, fontweight="bold")
ax.set_xlabel("Carrera", fontsize=11)
ax.set_ylabel("Frecuencia Absoluta", fontsize=11)
ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
ax.grid(axis="y", linestyle="--", alpha=0.5)
ax.set_facecolor("#F8FAFC")
fig.patch.set_facecolor("white")
plt.tight_layout()
plt.savefig("graficos/1_barras_carrera.png", dpi=150)
print("  ✔ graficos/1_barras_carrera.png")
plt.close()

# ── Figura 2: Gráfico de Bastón (materias_aprobadas — discreta) ──────────────
fig, ax = plt.subplots(figsize=(10, 5))
x = freq_materias["Materias Aprobadas"]
y = freq_materias["Frec. Absoluta"]
ax.vlines(x, 0, y, color="#2563EB", linewidth=2.5)
ax.plot(x, y, "o", color="#DC2626", markersize=9, zorder=5)
ax.set_title("Frecuencia de Materias Aprobadas\n(Variable Cuantitativa Discreta — Gráfico de Bastón)", fontsize=13, fontweight="bold")
ax.set_xlabel("Nº de Materias Aprobadas", fontsize=11)
ax.set_ylabel("Frecuencia Absoluta", fontsize=11)
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax.grid(axis="y", linestyle="--", alpha=0.5)
ax.set_facecolor("#F8FAFC")
fig.patch.set_facecolor("white")
plt.tight_layout()
plt.savefig("graficos/2_baston_materias.png", dpi=150)
print("  ✔ graficos/2_baston_materias.png")
plt.close()

# ── Figura 3: Histograma + Polígono de Frecuencias (edad — agrupada) ─────────
marcas = tabla_sturges["Xi"]
fi     = tabla_sturges["Fi"]
ancho  = amplitud

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(
    marcas, fi,
    width=ancho * 0.95,
    color="#7C3AED", alpha=0.75,
    edgecolor="white", linewidth=1.2,
    label="Histograma"
)
ax.plot(marcas, fi, "o-", color="#DC2626", linewidth=2, markersize=7, label="Polígono de Frecuencias")
ax.set_title("Histograma y Polígono de Frecuencias — Edad\n(Variable Cuantitativa Continua — Datos Agrupados)", fontsize=13, fontweight="bold")
ax.set_xlabel("Marca de Clase (Edad)", fontsize=11)
ax.set_ylabel("Frecuencia Absoluta", fontsize=11)
ax.legend(fontsize=10)
ax.grid(axis="y", linestyle="--", alpha=0.5)
ax.set_facecolor("#F8FAFC")
fig.patch.set_facecolor("white")
plt.tight_layout()
plt.savefig("graficos/3_histograma_poligono_edad.png", dpi=150)
print("  ✔ graficos/3_histograma_poligono_edad.png")
plt.close()

# ── Figura 4: Ojiva (frecuencia absoluta acumulada — edad) ───────────────────
fi_acum = tabla_sturges["Fi acum."]

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(marcas, fi_acum, "s-", color="#D97706", linewidth=2.5, markersize=8, label="Ojiva (Fi acum.)")
ax.fill_between(marcas, fi_acum, alpha=0.15, color="#D97706")
ax.set_title("Ojiva — Frecuencia Absoluta Acumulada (Edad)", fontsize=13, fontweight="bold")
ax.set_xlabel("Marca de Clase (Edad)", fontsize=11)
ax.set_ylabel("Frecuencia Absoluta Acumulada", fontsize=11)
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.legend(fontsize=10)
ax.grid(linestyle="--", alpha=0.5)
ax.set_facecolor("#F8FAFC")
fig.patch.set_facecolor("white")
plt.tight_layout()
plt.savefig("graficos/4_ojiva_edad.png", dpi=150)
print("  ✔ graficos/4_ojiva_edad.png")
plt.close()

# ── Figura 5: Gráfico de Torta (carrera — frecuencia relativa) ───────────────
fig, ax = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax.pie(
    freq_carrera["Frec. Relativa"],
    labels=freq_carrera["Carrera"],
    colors=COLORES[:len(freq_carrera)],
    autopct="%1.1f%%",
    startangle=140,
    pctdistance=0.75,
    wedgeprops={"edgecolor": "white", "linewidth": 2},
)
for autotext in autotexts:
    autotext.set_fontsize(11)
    autotext.set_fontweight("bold")
ax.set_title("Distribución Porcentual por Carrera\n(Gráfico de Torta — Frecuencia Relativa)", fontsize=13, fontweight="bold")
fig.patch.set_facecolor("white")
plt.tight_layout()
plt.savefig("graficos/5_torta_carrera.png", dpi=150)
print("  ✔ graficos/5_torta_carrera.png")
plt.close()

# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  ✅ LABORATORIO COMPLETADO")
print("  📁 Gráficos guardados en la carpeta: graficos/")
print("=" * 60)
