# 📊 Laboratorio: Procesamiento Estadístico con Python

**Materia:** Estadística Descriptiva  
**Archivos del proyecto:**
```
estadistica_lab/
│
├── datos_academicos.csv   ← Datos de 50 estudiantes
├── laboratorio.py         ← Script principal (5 fases)
├── README.md              ← Este archivo
└── graficos/              ← Se crea al ejecutar (5 gráficos PNG)
```

---

## ⚙️ PASO 0 — Configurar el entorno virtual

Abre una terminal **dentro de la carpeta `estadistica_lab`** y ejecuta:

```bash
# 1. Crear el entorno virtual
python -m venv venv

# 2. Activar el entorno
#    En Windows (PowerShell):
.\venv\Scripts\Activate.ps1
#    En Linux / macOS:
source venv/bin/activate

# 3. Instalar las librerías necesarias
pip install pandas numpy matplotlib
```

> ⚠️ Sabrás que está activado porque verás `(venv)` al inicio de tu terminal.

---

## ▶️ PASO 1 — Ejecutar el laboratorio

```bash
python laboratorio.py
```

---

## 📈 Gráficos que se generan

| Archivo | Tipo | Variable |
|---|---|---|
| `1_barras_carrera.png` | Barras | Carrera (cualitativa) |
| `2_baston_materias.png` | Bastón | Materias aprobadas (discreta) |
| `3_histograma_poligono_edad.png` | Histograma + Polígono | Edad (agrupada) |
| `4_ojiva_edad.png` | Ojiva | Edad (acumulada) |
| `5_torta_carrera.png` | Torta | Carrera (% relativo) |

---

## 📋 Resumen de las 5 Fases

| Fase | Descripción |
|---|---|
| **Fase 1** | Carga del CSV con `pandas` |
| **Fase 2** | Frecuencias de variables **cualitativas** (`carrera`, `estado`) |
| **Fase 3** | Frecuencias acumuladas de variables **discretas** (`materias_aprobadas`) |
| **Fase 4** | Algoritmo de **Sturges** para datos agrupados (`edad`) |
| **Fase 5** | Visualización con **Matplotlib** (5 gráficos) |
