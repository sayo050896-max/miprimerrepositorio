import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ──────────────────────────────────────────────────────────────
# Configuración de la página
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Estadística Descriptiva",
    page_icon="📊",
    layout="wide",
)

# ──────────────────────────────────────────────────────────────
# CSS del sidebar  (compatible con modo oscuro y claro)
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ══════════════════════════════════════════════════════════
   VARIABLES DE COLOR — cambian según el tema de Streamlit
   ══════════════════════════════════════════════════════════ */

/* Modo oscuro (tema por defecto en tu captura) */
[data-theme="dark"] [data-testid="stSidebar"],
.stApp[data-theme="dark"] [data-testid="stSidebar"] {
    --sb-bg:          #1A1F2E;
    --sb-bg-card:     #242938;
    --sb-border:      rgba(255,255,255,0.08);
    --sb-text:        #E2E8F0;
    --sb-text-muted:  #64748B;
    --sb-text-faint:  #475569;
    --sb-accent:      #3B82F6;
    --sb-select-bg:   #2D3347;
    --sb-select-border: rgba(255,255,255,0.12);
    --sb-badge-bg:    rgba(251,191,36,0.15);
    --sb-badge-color: #FCD34D;
    --sb-badge-loaded-bg:    rgba(52,211,153,0.15);
    --sb-badge-loaded-color: #6EE7B7;
    --sb-metric-bg:   #242938;
}

/* Modo claro */
[data-theme="light"] [data-testid="stSidebar"],
.stApp[data-theme="light"] [data-testid="stSidebar"] {
    --sb-bg:          #F8FAFC;
    --sb-bg-card:     #FFFFFF;
    --sb-border:      #E2E8F0;
    --sb-text:        #0F172A;
    --sb-text-muted:  #64748B;
    --sb-text-faint:  #94A3B8;
    --sb-accent:      #2563EB;
    --sb-select-bg:   #FFFFFF;
    --sb-select-border: #E2E8F0;
    --sb-badge-bg:    #FEF3C7;
    --sb-badge-color: #92400E;
    --sb-badge-loaded-bg:    #D1FAE5;
    --sb-badge-loaded-color: #065F46;
    --sb-metric-bg:   #FFFFFF;
}

/* Fallback para cuando Streamlit no pone data-theme todavía
   (cubre el modo oscuro de tu captura) */
[data-testid="stSidebar"] {
    --sb-bg:          #1A1F2E;
    --sb-bg-card:     #242938;
    --sb-border:      rgba(255,255,255,0.08);
    --sb-text:        #E2E8F0;
    --sb-text-muted:  #64748B;
    --sb-text-faint:  #475569;
    --sb-accent:      #3B82F6;
    --sb-select-bg:   #2D3347;
    --sb-select-border: rgba(255,255,255,0.12);
    --sb-badge-bg:    rgba(251,191,36,0.15);
    --sb-badge-color: #FCD34D;
    --sb-badge-loaded-bg:    rgba(52,211,153,0.15);
    --sb-badge-loaded-color: #6EE7B7;
    --sb-metric-bg:   #242938;
}

/* ══════════════════════════════════════════════════════════
   ESTRUCTURA BASE
   ══════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background-color: var(--sb-bg) !important;
    border-right: 1px solid var(--sb-border) !important;
}
[data-testid="stSidebarContent"] {
    padding: 0 !important;
}

/* ── Encabezado ─────────────────────────────────────────── */
.sb-header {
    padding: 20px 18px 14px;
    border-bottom: 1px solid var(--sb-border);
    margin-bottom: 4px;
}
.sb-title {
    font-size: 15px;
    font-weight: 600;
    color: var(--sb-text);
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 2px;
}
.sb-subtitle {
    font-size: 11px;
    color: var(--sb-text-muted);
    margin-left: 24px;
}

/* ── Etiquetas de sección ───────────────────────────────── */
.sb-section {
    font-size: 10px;
    font-weight: 600;
    color: var(--sb-text-faint);
    text-transform: uppercase;
    letter-spacing: 0.07em;
    padding: 14px 18px 4px;
}

/* ── Selectboxes ────────────────────────────────────────── */
[data-testid="stSidebar"] .stSelectbox label {
    font-size: 11px !important;
    color: var(--sb-text-muted) !important;
    font-weight: 500 !important;
    margin-bottom: 2px !important;
}
[data-testid="stSidebar"] .stSelectbox > div[data-baseweb="select"] > div {
    background-color: var(--sb-select-bg) !important;
    border: 1px solid var(--sb-select-border) !important;
    border-radius: 8px !important;
    font-size: 12px !important;
    min-height: 34px !important;
    color: var(--sb-text) !important;
}
[data-testid="stSidebar"] .stSelectbox > div[data-baseweb="select"] > div:focus-within {
    border-color: var(--sb-accent) !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.2) !important;
}
/* Texto seleccionado dentro del selectbox */
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] span {
    color: var(--sb-text) !important;
}
/* Flecha del selectbox */
[data-testid="stSidebar"] .stSelectbox svg {
    fill: var(--sb-text-muted) !important;
}

/* ── File uploader ──────────────────────────────────────── */
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: var(--sb-select-bg) !important;
    border: 1px dashed var(--sb-select-border) !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] label,
[data-testid="stSidebar"] [data-testid="stFileUploader"] span,
[data-testid="stSidebar"] [data-testid="stFileUploader"] p {
    color: var(--sb-text-muted) !important;
    font-size: 12px !important;
}

/* ── Métricas de Sturges ────────────────────────────────── */
[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: var(--sb-metric-bg) !important;
    border: 1px solid var(--sb-border) !important;
    border-radius: 8px !important;
    padding: 8px 10px !important;
}
[data-testid="stSidebar"] [data-testid="stMetric"] label {
    font-size: 10px !important;
    color: var(--sb-text-muted) !important;
}
[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    font-size: 18px !important;
    color: var(--sb-text) !important;
}

/* ── Divisor ────────────────────────────────────────────── */
.sb-divider {
    height: 1px;
    background: var(--sb-border);
    margin: 8px 0;
}

/* ── Dataset pill ───────────────────────────────────────── */
.dataset-pill {
    margin: 0 12px 6px;
    padding: 10px 12px;
    background: var(--sb-bg-card);
    border: 1px solid var(--sb-border);
    border-radius: 10px;
    display: flex;
    align-items: flex-start;
    gap: 8px;
}
.dataset-icon { font-size: 18px; margin-top: 1px; }
.dataset-name {
    font-size: 12px;
    font-weight: 600;
    color: var(--sb-text);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 140px;
}
.dataset-meta { font-size: 11px; color: var(--sb-text-muted); margin-top: 1px; }
.dataset-badge {
    margin-left: auto;
    font-size: 10px;
    padding: 2px 7px;
    border-radius: 999px;
    background: var(--sb-badge-bg);
    color: var(--sb-badge-color);
    font-weight: 600;
    white-space: nowrap;
    align-self: flex-start;
}
.dataset-badge.loaded {
    background: var(--sb-badge-loaded-bg);
    color: var(--sb-badge-loaded-color);
}

</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────
with st.sidebar:

    # ── Encabezado ───────────────────────────────────────────
    st.markdown("""
    <div class="sb-header">
        <div class="sb-title">📊 Estadística</div>
        <div class="sb-subtitle">Dashboard descriptivo</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Carga de datos ───────────────────────────────────────
    st.markdown('<div class="sb-section">Dataset</div>', unsafe_allow_html=True)

    archivo = st.file_uploader(
        "Cargar CSV",
        type=["csv"],
        label_visibility="collapsed",
        help="Sube tu propio CSV o usa el dataset de muestra",
    )

    @st.cache_data
    def cargar_muestra():
        return pd.read_csv("datos_academicos.csv")

    if archivo is not None:
        df = pd.read_csv(archivo)
        badge_html = '<span class="dataset-badge loaded">cargado</span>'
        nombre_archivo = archivo.name
    else:
        df = cargar_muestra()
        badge_html = '<span class="dataset-badge">muestra</span>'
        nombre_archivo = "datos_academicos.csv"

    st.markdown(f"""
    <div class="dataset-pill">
        <div class="dataset-icon">📄</div>
        <div style="flex:1;overflow:hidden">
            <div class="dataset-name">{nombre_archivo}</div>
            <div class="dataset-meta">{df.shape[0]} filas · {df.shape[1]} columnas</div>
        </div>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)

    # Validación de columnas
    cols_objeto = list(df.select_dtypes(include="object").columns)
    cols_num    = list(df.select_dtypes(include=["int64", "float64"]).columns)

    if not cols_objeto or not cols_num:
        st.error("El CSV necesita al menos una columna categórica y una numérica.")
        st.stop()

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    # ── Variables ────────────────────────────────────────────
    st.markdown('<div class="sb-section">Variables</div>', unsafe_allow_html=True)

    col_cualitativa = st.selectbox(
        "Cualitativa (nominal)",
        options=cols_objeto,
        index=0,
        help="Se usa en Fases 2 y 5 (barras y torta)",
    )
    col_discreta = st.selectbox(
        "Cuantitativa discreta",
        options=cols_num,
        index=0,
        help="Se usa en Fase 3 (gráfico de bastón)",
    )
    col_agrupada = st.selectbox(
        "Sturges (datos agrupados)",
        options=cols_num,
        index=min(1, len(cols_num) - 1),
        help="Se usa en Fase 4 (histograma y ojiva)",
    )

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    # ── Parámetros Sturges (solo informativo) ─────────────────
    n_datos  = len(df)
    k_sturges = int(np.ceil(1 + 3.322 * np.log10(n_datos)))
    rango_var = float(df[col_agrupada].max() - df[col_agrupada].min())
    amplitud  = float(np.ceil(rango_var / k_sturges))

    st.markdown('<div class="sb-section">Sturges — parámetros</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.metric("n", n_datos)
    c2.metric("k", k_sturges)
    c1.metric("Rango", f"{rango_var:.0f}")
    c2.metric("Amplitud", f"{amplitud:.0f}")

    st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    # ── Paleta ───────────────────────────────────────────────
    PALETA = ["#2563EB", "#7C3AED", "#DC2626", "#D97706", "#16A34A", "#0891B2", "#BE185D"]


# ──────────────────────────────────────────────────────────────
# CONTENIDO PRINCIPAL (sin cambios funcionales)
# ──────────────────────────────────────────────────────────────
st.title("📊 Procesamiento Estadístico con Python")
st.caption("Estadística Descriptiva")

# ── FASE 1: Ingesta ──────────────────────────────────────────
st.header("📂 Ingesta de Datos")

if archivo is not None:
    st.success(f"✔ Archivo cargado: **{archivo.name}** — {len(df)} registros")
else:
    st.info("ℹ️ Usando el dataset de muestra `datos_academicos.csv`")

st.write(f"**Forma del dataset:** {df.shape[0]} filas × {df.shape[1]} columnas")
st.dataframe(df, use_container_width=True, height=220)

# ── FASE 2: Cualitativa ──────────────────────────────────────
st.divider()
st.header(f"📋 Variable Cualitativa: `{col_cualitativa}`")

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
    datos_grafico = freq_cual
    if len(freq_cual) > 15:
        top_n = st.slider(f"Categorías a mostrar ({len(freq_cual)} totales)", 5, min(30, len(freq_cual)), 10)
        datos_grafico = freq_cual.sort_values("Fi", ascending=False).head(top_n)
    fig = px.bar(datos_grafico, x=col_cualitativa, y="Fi", text="Fi",
                 color_discrete_sequence=["#2563EB"])
    fig.update_traces(textposition="outside",
                      hovertemplate=f"<b>%{{x}}</b><br>Frec. Absoluta: %{{y}}<extra></extra>",
                      marker=dict(line=dict(width=1, color="#1D4ED8")))
    fig.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="rgba(0,0,0,0)",
                      margin=dict(l=20, r=20, t=40, b=20), height=380,
                      xaxis=dict(gridcolor="rgba(0,0,0,0)", tickangle=35),
                      yaxis=dict(gridcolor="#E2E8F0"))
    st.plotly_chart(fig, use_container_width=True)

# ── FASE 3: Discreta ─────────────────────────────────────────
st.divider()
st.header(f"📋 Variable Cuantitativa Discreta: `{col_discreta}`")

n_unicos = df[col_discreta].nunique()
if n_unicos == len(df):
    st.warning(f"**`{col_discreta}`** parece un identificador único ({n_unicos} valores distintos). "
               "Selecciona una variable con valores repetidos en el sidebar.")
    st.info("💡 Ejemplo: `edad`, `nota`, `materias_aprobadas`.")
else:
    freq_disc = df[col_discreta].value_counts().sort_index().reset_index()
    freq_disc.columns = [col_discreta, "Fi"]
    freq_disc["hi"]        = (freq_disc["Fi"] / len(df)).round(4)
    freq_disc["Fi acum."]  = freq_disc["Fi"].cumsum()
    freq_disc["hi acum."]  = freq_disc["hi"].cumsum().round(4)

    col3, col4 = st.columns([1, 1.4])
    with col3:
        st.subheader("Tabla de Frecuencias")
        st.dataframe(freq_disc.head(20) if len(freq_disc) > 20 else freq_disc,
                     use_container_width=True)
    with col4:
        st.subheader("Gráfico de Bastón")
        fig = go.Figure()
        for _, row in freq_disc.iterrows():
            fig.add_shape(type="line", x0=row[col_discreta], y0=0,
                          x1=row[col_discreta], y1=row["Fi"],
                          line=dict(color="#2563EB", width=3))
        fig.add_trace(go.Scatter(x=freq_disc[col_discreta], y=freq_disc["Fi"],
                                 mode="markers",
                                 marker=dict(color="#DC2626", size=10,
                                             line=dict(color="white", width=1.5)),
                                 hovertemplate=f"<b>{col_discreta}: %{{x}}</b><br>Fi: %{{y}}<extra></extra>",
                                 name="Frecuencia"))
        dtick = max(1, len(freq_disc) // 10)
        fig.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="rgba(0,0,0,0)",
                          margin=dict(l=20, r=20, t=30, b=20), showlegend=False, height=380,
                          xaxis=dict(gridcolor="rgba(0,0,0,0)", dtick=dtick),
                          yaxis=dict(gridcolor="#E2E8F0"))
        st.plotly_chart(fig, use_container_width=True)

# ── FASE 4: Sturges ──────────────────────────────────────────
st.divider()
st.header(f"📋 Datos Agrupados (Sturges): `{col_agrupada}`")

lim_inf = df[col_agrupada].min()
bins    = np.arange(lim_inf, lim_inf + (k_sturges + 1) * amplitud, amplitud)
bins[-1] += 0.0001

df_tmp = df.copy()
df_tmp["intervalo"] = pd.cut(df_tmp[col_agrupada], bins=bins, right=False, include_lowest=True)

tabla = df_tmp.groupby("intervalo", observed=True).size().reset_index(name="Fi")
tabla["Xi"]        = tabla["intervalo"].apply(lambda x: (x.left + x.right) / 2)
tabla["hi"]        = (tabla["Fi"] / n_datos).round(4)
tabla["Fi acum."]  = tabla["Fi"].cumsum()
tabla["hi acum."]  = tabla["hi"].cumsum().round(4)
tabla["Intervalo"] = tabla["intervalo"].astype(str)
tabla = tabla[["Intervalo", "Xi", "Fi", "hi", "Fi acum.", "hi acum."]]

col5, col6 = st.columns([1, 1.4])
with col5:
    st.subheader("Tabla de Frecuencias")
    st.dataframe(tabla, use_container_width=True)
with col6:
    st.subheader("Histograma + Polígono de Frecuencias")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=tabla["Intervalo"], y=tabla["Fi"], name="Histograma",
                         marker_color="#7C3AED", opacity=0.75,
                         hovertemplate="Intervalo: %{x}<br>Fi: %{y}<extra></extra>"))
    fig.add_trace(go.Scatter(x=tabla["Intervalo"], y=tabla["Fi"], mode="lines+markers",
                             name="Polígono", line=dict(color="#DC2626", width=2.5),
                             marker=dict(size=8, color="#DC2626")))
    fig.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="rgba(0,0,0,0)",
                      margin=dict(l=20, r=20, t=30, b=20), height=380,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                      xaxis=dict(gridcolor="rgba(0,0,0,0)"),
                      yaxis=dict(gridcolor="#E2E8F0"))
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Ojiva — Frecuencia Absoluta Acumulada")
fig_ojiva = go.Figure()
fig_ojiva.add_trace(go.Scatter(x=tabla["Intervalo"], y=tabla["Fi acum."],
                                mode="lines+markers", name="Ojiva (Fi acum.)",
                                line=dict(color="#D97706", width=3),
                                marker=dict(size=9, symbol="square", color="#D97706"),
                                fill="tozeroy", fillcolor="rgba(217,119,6,0.12)"))
fig_ojiva.update_layout(plot_bgcolor="#F8FAFC", paper_bgcolor="rgba(0,0,0,0)",
                         margin=dict(l=20, r=20, t=30, b=20), height=380,
                         xaxis=dict(gridcolor="rgba(0,0,0,0)"),
                         yaxis=dict(gridcolor="#E2E8F0"))
st.plotly_chart(fig_ojiva, use_container_width=True)

# ── FASE 5: Torta ────────────────────────────────────────────
st.divider()
st.header(f"📋 Gráfico de Torta: `{col_cualitativa}`")

col7, col8 = st.columns([1.2, 1])
with col7:
    fig = px.pie(freq_cual, names=col_cualitativa, values="hi",
                 color_discrete_sequence=PALETA, hole=0.4)
    fig.update_traces(textinfo="percent+label",
                      marker=dict(line=dict(color="white", width=2)))
    fig.update_layout(showlegend=True,
                      legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
                      margin=dict(l=20, r=20, t=20, b=20), height=400)
    st.plotly_chart(fig, use_container_width=True)
with col8:
    st.subheader("Distribución porcentual")
    st.dataframe(freq_cual.rename(columns={"hi (%)": "Porcentaje (%)"}),
                 use_container_width=True)

st.divider()
st.success("✅ Laboratorio completado — todas las fases ejecutadas correctamente.")
