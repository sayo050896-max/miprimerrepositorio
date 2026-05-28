"""
app.py — Dashboard Streamlit: Estadística Descriptiva
Ejecutar: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# ──────────────────────────────────────────────
# Configuración de la página
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Estadística Descriptiva",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Laboratorio: Procesamiento Estadístico con Python")
st.caption("Materia: Estadística Descriptiva — Guía de Laboratorio")

# ──────────────────────────────────────────────
# FASE 1: Ingesta de datos
# ──────────────────────────────────────────────
st.header("📂 Fase 1 — Ingesta de Datos")

archivo = st.file_uploader(
    "Sube tu archivo CSV (o usa el dataset de muestra)",
    type=["csv"],
)

@st.cache_data
def cargar_muestra():
    return pd.read_csv("datos_academicos.csv")

if archivo is not None:
    df = pd.read_csv(archivo)
    st.success(f"✔ Archivo cargado: **{archivo.name}** — {len(df)} registros")
else:
    df = cargar_muestra()
    st.info("ℹ️ Usando el dataset de muestra -------------------------> `datos_academicos.csv`")

st.write(f"**Forma del dataset:** {df.shape[0]} filas × {df.shape[1]} columnas")
st.dataframe(df, use_container_width=True, height=220)

# ──────────────────────────────────────────────
# Selección de columnas (sidebar)
# ──────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuración")

    cols_objeto = [c for c in df.select_dtypes(include="object").columns]
    cols_num    = [c for c in df.select_dtypes(include=["int64", "float64"]).columns]

    if len(cols_objeto) == 0 or len(cols_num) == 0:
        st.error("🚨 El dataset no tiene la estructura adecuada. Asegúrate de incluir al menos una columna categórica (texto) y columnas numéricas.")
        st.stop()

    col_cualitativa = st.selectbox("Variable Cualitativa", options=cols_objeto, index=0)

    col_discreta = st.selectbox(
        "Variable Cuantitativa Discreta",
        options=cols_num,
        index=0,
    )
    col_agrupada = st.selectbox(
        "Variable para Datos Agrupados (Sturges)",
        options=cols_num,
        index=min(1, len(cols_num) - 1),
    )

    PALETA = ["#2563EB", "#7C3AED", "#DC2626", "#D97706", "#16A34A", "#0891B2", "#BE185D"]

st.divider()

# ──────────────────────────────────────────────
# FASE 2: Variables Cualitativas (mejorada con Seaborn)
# ──────────────────────────────────────────────
st.header(f"📋 Fase 2 — Variable Cualitativa: `{col_cualitativa}`")

freq_cual = df[col_cualitativa].value_counts().reset_index()
freq_cual.columns = [col_cualitativa, "Fi"]
freq_cual["hi"]     = (freq_cual["Fi"] / len(df)).round(4)
freq_cual["hi (%)"] = (freq_cual["hi"] * 100).round(2)
freq_cual = freq_cual.sort_values(col_cualitativa).reset_index(drop=True)

col1, col2 = st.columns([1, 1.4])

with col1:
    st.subheader("Tabla de Frecuencias")
    st.dataframe(freq_cual, use_container_width=True)

with col2:
    st.subheader("Gráfico de Barras")

    # Si hay muchas categorías, permitir al usuario filtrar cuántas mostrar
    if len(freq_cual) > 15:
        top_n = st.slider(
            f"Hay muchas categorías ({len(freq_cual)}). Selecciona cuántas mostrar:",
            min_value=5,
            max_value=min(30, len(freq_cual)),
            value=10,
        )
        datos_grafico = freq_cual.sort_values("Fi", ascending=False).head(top_n)
    else:
        datos_grafico = freq_cual

    fig = px.bar(
        datos_grafico,
        x=col_cualitativa,
        y="Fi",
        text="Fi",
        labels={col_cualitativa: col_cualitativa, "Fi": "Frecuencia Absoluta"},
        color_discrete_sequence=["#2563EB"]
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate=f"<b>%{{x}}</b><br>Frecuencia Absoluta: %{{y}}<extra></extra>",
        marker=dict(
            line=dict(width=1, color="#1D4ED8"),
        )
    )
    fig.update_layout(
        title=dict(
            text=f"Distribución de '{col_cualitativa}' (n={len(datos_grafico)} categorías)",
            font=dict(size=14, family="sans-serif", color="#1E293B", weight="bold")
        ),
        plot_bgcolor="#F8FAFC",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(
            title=dict(text=col_cualitativa, font=dict(size=11, color="#475569")),
            gridcolor="rgba(0,0,0,0)",
            tickangle=35
        ),
        yaxis=dict(
            title=dict(text="Frecuencia Absoluta", font=dict(size=11, color="#475569")),
            gridcolor="#E2E8F0"
        ),
        height=380
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ──────────────────────────────────────────────
# FASE 3: Variable Cuantitativa Discreta
# ──────────────────────────────────────────────
st.header(f"📋 Fase 3 — Variable Discreta: `{col_discreta}`")

# Detectamos si la variable es una variable de identificación única
# (cuando el número de categorías únicas es igual al número total de datos)
num_datos = len(df)
num_valores_unicos = df[col_discreta].nunique()

# Red de seguridad: si es un ID, mostramos una advertencia en lugar del gráfico
if num_valores_unicos == num_datos:
    st.warning(
        f"🚨 **¡Atención!** Has seleccionado la columna `{col_discreta}`. "
        f"Esta columna parece ser un identificador único (ID) porque tiene {num_valores_unicos} valores distintos en {num_datos} registros. "
    )
    st.info("💡 **Consejo:** Un gráfico de bastón no es útil para variables de identificación. Ve a la barra lateral y selecciona una variable numérica que tenga valores que se repitan (como `edad`, `nota`, etc.).")
else:
    # SI NO ES UN ID, procedemos con el gráfico normal:
    
    freq_disc = df[col_discreta].value_counts().sort_index().reset_index()
    freq_disc.columns = [col_discreta, "Fi"]
    freq_disc["hi"] = (freq_disc["Fi"] / num_datos).round(4)
    freq_disc["Fi acum."] = freq_disc["Fi"].cumsum()
    freq_disc["hi acum."] = freq_disc["hi"].cumsum().round(4)

    col3, col4 = st.columns([1, 1.4])

    with col3:
        st.subheader("Tabla de Frecuencias")
        # Mostramos un subconjunto de la tabla si es muy grande
        if len(freq_disc) > 20:
             st.info(f"Mostrando los primeros 20 registros de {len(freq_disc)} para la tabla.")
             st.dataframe(freq_disc.head(20), use_container_width=True)
        else:
            st.dataframe(freq_disc, use_container_width=True)

    with col4:
        st.subheader("Gráfico de Bastón")
        
        fig = go.Figure()
        
        # Agregar las líneas de los bastones usando shapes de Plotly
        for index, row in freq_disc.iterrows():
            fig.add_shape(
                type="line",
                x0=row[col_discreta], y0=0,
                x1=row[col_discreta], y1=row["Fi"],
                line=dict(color="#2563EB", width=3)
            )
        
        # Agregar los marcadores superiores
        fig.add_trace(go.Scatter(
            x=freq_disc[col_discreta],
            y=freq_disc["Fi"],
            mode="markers",
            marker=dict(
                color="#DC2626",
                size=10,
                line=dict(color="white", width=1.5)
            ),
            hovertemplate=f"<b>{col_discreta}: %{{x}}</b><br>Frecuencia Absoluta: %{{y}}<extra></extra>",
            name="Frecuencia"
        ))

        # Ajuste de escala dinámica en el eje X
        if len(freq_disc) > 15:
            separacion_tickers = int(len(freq_disc) / 10)
            if separacion_tickers == 0: separacion_tickers = 1
        else:
            separacion_tickers = 1

        fig.update_layout(
            plot_bgcolor="#F8FAFC",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis=dict(
                title=dict(text=col_discreta, font=dict(size=11, color="#475569")),
                gridcolor="rgba(0,0,0,0)",
                dtick=separacion_tickers
            ),
            yaxis=dict(
                title=dict(text="Frecuencia Absoluta", font=dict(size=11, color="#475569")),
                gridcolor="#E2E8F0"
            ),
            showlegend=False,
            height=380
        )
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# ──────────────────────────────────────────────
# FASE 4: Datos Agrupados — Algoritmo de Sturges
# ──────────────────────────────────────────────
st.header(f"📋 Fase 4 — Datos Agrupados (Sturges): `{col_agrupada}`")

n        = len(df)
k        = int(np.ceil(1 + 3.322 * np.log10(n)))
rango    = df[col_agrupada].max() - df[col_agrupada].min()
amplitud = np.ceil(rango / k)

m1, m2, m3, m4 = st.columns(4)
m1.metric("n (datos)", n)
m2.metric("k (intervalos)", k, help="Fórmula: 1 + 3.322 × log₁₀(n)")
m3.metric("Rango", rango)
m4.metric("Amplitud (c)", amplitud)

lim_inf = df[col_agrupada].min()
bins    = np.arange(lim_inf, lim_inf + (k + 1) * amplitud, amplitud)
bins[-1] += 0.0001

df_tmp = df.copy()
df_tmp["intervalo"] = pd.cut(df_tmp[col_agrupada], bins=bins, right=False, include_lowest=True)

tabla = df_tmp.groupby("intervalo", observed=True).size().reset_index(name="Fi")
tabla["Xi"]       = tabla["intervalo"].apply(lambda x: (x.left + x.right) / 2)
tabla["hi"]       = (tabla["Fi"] / n).round(4)
tabla["Fi acum."] = tabla["Fi"].cumsum()
tabla["hi acum."] = tabla["hi"].cumsum().round(4)
tabla["Intervalo"] = tabla["intervalo"].astype(str)
tabla = tabla[["Intervalo", "Xi", "Fi", "hi", "Fi acum.", "hi acum."]]

col5, col6 = st.columns([1, 1.4])

with col5:
    st.subheader("Tabla de Frecuencias")
    st.dataframe(tabla, use_container_width=True)

with col6:
    st.subheader("Histograma + Polígono de Frecuencias")
    fig = go.Figure()
    
    # Histograma (Bar)
    fig.add_trace(go.Bar(
        x=tabla["Intervalo"],
        y=tabla["Fi"],
        name="Histograma",
        marker_color="#7C3AED",
        opacity=0.75,
        hovertemplate="Intervalo: %{x}<br>Frecuencia Absoluta: %{y}<extra></extra>"
    ))
    
    # Polígono (Scatter)
    fig.add_trace(go.Scatter(
        x=tabla["Intervalo"],
        y=tabla["Fi"],
        mode="lines+markers",
        name="Polígono de Frecuencias",
        line=dict(color="#DC2626", width=2.5),
        marker=dict(size=8, color="#DC2626"),
        hovertemplate="Intervalo: %{x}<br>Frecuencia Absoluta: %{y}<extra></extra>"
    ))
    
    fig.update_layout(
        plot_bgcolor="#F8FAFC",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(
            title=dict(text=f"Intervalos ({col_agrupada})", font=dict(size=11, color="#475569")),
            gridcolor="rgba(0,0,0,0)"
        ),
        yaxis=dict(
            title=dict(text="Frecuencia Absoluta", font=dict(size=11, color="#475569")),
            gridcolor="#E2E8F0"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=380
    )
    st.plotly_chart(fig, use_container_width=True)

# Ojiva
st.subheader("Ojiva — Frecuencia Absoluta Acumulada")
fig_ojiva = go.Figure()
fig_ojiva.add_trace(go.Scatter(
    x=tabla["Intervalo"],
    y=tabla["Fi acum."],
    mode="lines+markers",
    name="Ojiva (Fi acum.)",
    line=dict(color="#D97706", width=3),
    marker=dict(size=9, symbol="square", color="#D97706"),
    fill="tozeroy",
    fillcolor="rgba(217, 119, 6, 0.12)",
    hovertemplate="Intervalo: %{x}<br>Frecuencia Acumulada: %{y}<extra></extra>"
))
fig_ojiva.update_layout(
    plot_bgcolor="#F8FAFC",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=30, b=20),
    xaxis=dict(
        title=dict(text=f"Intervalos ({col_agrupada})", font=dict(size=11, color="#475569")),
        gridcolor="rgba(0,0,0,0)"
    ),
    yaxis=dict(
        title=dict(text="Frecuencia Acumulada", font=dict(size=11, color="#475569")),
        gridcolor="#E2E8F0"
    ),
    height=380
)
st.plotly_chart(fig_ojiva, use_container_width=True)

st.divider()

# ──────────────────────────────────────────────
# FASE 5: Gráfico de Torta
# ──────────────────────────────────────────────
st.header(f"📋 Fase 5 — Gráfico de Torta: `{col_cualitativa}`")

col7, col8 = st.columns([1.2, 1])

with col7:
    fig = px.pie(
        freq_cual,
        names=col_cualitativa,
        values="hi",
        color_discrete_sequence=PALETA,
        hole=0.4
    )
    fig.update_traces(
        textinfo="percent+label",
        hovertemplate=f"<b>%{{label}}</b><br>Proporción: %{{value}}<br>Porcentaje: %{{percent}}<extra></extra>",
        marker=dict(line=dict(color="white", width=2))
    )
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with col8:
    st.subheader("Distribución porcentual")
    st.dataframe(
        freq_cual.rename(columns={"hi (%)": "Porcentaje (%)"}),
        use_container_width=True,
    )

st.divider()
st.success("✅ Laboratorio completado — todas las fases ejecutadas correctamente.")
