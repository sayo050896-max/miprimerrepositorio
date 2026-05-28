# 📊 Laboratorio: Procesamiento Estadístico con Python

**Materia:** Estadística Descriptiva  

Este proyecto contiene una guía práctica de laboratorio diseñada para realizar el procesamiento y análisis estadístico descriptivo de datos académicos. Cuenta con dos modalidades de visualización: un script automatizado en consola (`laboratorio.py`) y un dashboard interactivo en tiempo real (`app.py`).

## 📁 Archivos del Proyecto

```text
estadistica_lab/
│
├── datos_academicos.csv   ← Base de datos de muestra (50 estudiantes)
├── laboratorio.py         ← Script de consola (procesa las 5 fases y guarda reportes)
├── app.py                 ← Dashboard interactivo web de Streamlit (con Plotly)
├── README.md              ← Este archivo guía
└── graficos/              ← Carpeta local creada por laboratorio.py (5 imágenes PNG)
```

---

## ⚙️ Configuración del Entorno Virtual

Sigue estos pasos para preparar tu entorno de trabajo antes de ejecutar el proyecto:

Abre una terminal **dentro de la carpeta `estadistica_lab`** y ejecuta:

```bash
# 1. Crear el entorno virtual
python -m venv venv

# 2. Activar el entorno
#    En Windows (PowerShell):
.\venv\Scripts\Activate.ps1
#    En Linux / macOS:
source venv/bin/activate

# 3. Instalar todas las librerías necesarias
pip install pandas numpy matplotlib plotly seaborn streamlit
```

> ⚠️ Sabrás que el entorno está activado correctamente si visualizas el prefijo `(venv)` al inicio de tu terminal.

---

## ▶️ Modalidades de Ejecución

El proyecto te permite explorar los datos mediante dos opciones:

### 🖥️ Opcion A — Script en Consola (Reportes Estáticos)
Procesa las frecuencias, calcula el algoritmo de Sturges y guarda 5 gráficos estáticos en alta calidad.
```bash
python laboratorio.py
```
> *Los gráficos se guardarán automáticamente en formato PNG dentro de la carpeta `graficos/`.*

### 🌐 Opción B — Dashboard Interactivo (Streamlit Web)
Carga un panel interactivo que dibuja los gráficos dinámicamente en tiempo real.
```bash
streamlit run app.py
```
* Se abrirá automáticamente en tu navegador en `http://localhost:8501`.
* **Nota:** Esta aplicación dibuja los gráficos dinámicamente en la memoria del navegador usando **Plotly**, por lo que **no necesita ni depende** de la carpeta local `graficos/` para funcionar.

---

## 📈 Resumen de Gráficos y Fases

### Gráficos Generados en Consola (`laboratorio.py`)
| Archivo PNG | Tipo de Gráfico | Variable Analizada |
|---|---|---|
| `1_barras_carrera.png` | Barras | Carrera (Cualitativa nominal) |
| `2_baston_materias.png` | Bastón | Materias aprobadas (Cuantitativa discreta) |
| `3_histograma_poligono_edad.png` | Histograma + Polígono | Edad (Datos agrupados con marcas de clase) |
| `4_ojiva_edad.png` | Ojiva | Edad (Frecuencia absoluta acumulada) |
| `5_torta_carrera.png` | Torta | Carrera (Distribución porcentual relativa) |

### Fases del Procesamiento Estadístico
1. **Fase 1:** Ingesta y lectura del CSV con `pandas`.
2. **Fase 2:** Distribución y tabla de frecuencias de variables **cualitativas** (`carrera`, `estado`).
3. **Fase 3:** Frecuencias absolutas y relativas acumuladas de variables **discretas** (`materias_aprobadas`).
4. **Fase 4:** Aplicación del **Algoritmo de Sturges** para la agrupación de variables en intervalos continuos (`edad`).
5. **Fase 5:** Visualización y reporte gráfico (usando **Matplotlib** en consola y **Plotly** en el dashboard).
