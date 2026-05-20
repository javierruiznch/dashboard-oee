import streamlit as st
import pandas as pd
import plotly.express as px
import html
import re
import json
import ast

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="AI Operational Command Center",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# LINKS GOOGLE SHEETS
# =========================================================

url_reporte = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQK79g93gSXWRaJyNnjezabtjWCEVfio22rDyt2cEXyVRpw3wmX9mhxD--sEqfFqLohqTbf6WojSsLn/pub?gid=225466432&single=true&output=csv"

url_insights = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQK79g93gSXWRaJyNnjezabtjWCEVfio22rDyt2cEXyVRpw3wmX9mhxD--sEqfFqLohqTbf6WojSsLn/pub?gid=831602632&single=true&output=csv"

# =========================================================
# ESTILO EJECUTIVO
# =========================================================

st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #F3F6FA 0%, #EEF3F8 45%, #F8FAFC 100%);
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

.block-container {
    padding-top: 2.1rem;
    padding-bottom: 2.2rem;
    max-width: 1460px;
}

.hero {
    background: linear-gradient(135deg, #0F172A 0%, #163A5F 48%, #2563EB 100%);
    padding: 34px 38px;
    border-radius: 28px;
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.20);
    margin-bottom: 26px;
}

.hero-title {
    color: #FFFFFF;
    font-size: 38px;
    font-weight: 850;
    letter-spacing: -0.8px;
    margin-bottom: 6px;
}

.hero-subtitle {
    color: #D9EAFD;
    font-size: 16px;
    font-weight: 400;
    line-height: 1.55;
    max-width: 980px;
}

.hero-badge {
    display: inline-block;
    margin-top: 18px;
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.25);
    color: #FFFFFF;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 650;
}

.kpi-card {
    background: rgba(255,255,255,0.98);
    border: 1px solid rgba(226,232,240,0.95);
    border-radius: 22px;
    padding: 22px 22px 20px 22px;
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
    min-height: 142px;
}

.kpi-label {
    color: #64748B;
    font-size: 12.5px;
    font-weight: 760;
    letter-spacing: 0.4px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.kpi-value {
    color: #0F172A;
    font-size: 33px;
    font-weight: 850;
    letter-spacing: -0.8px;
    line-height: 1.0;
}

.kpi-foot {
    color: #64748B;
    font-size: 13px;
    font-weight: 500;
    margin-top: 12px;
}

.kpi-blue { border-top: 5px solid #2563EB; }
.kpi-green { border-top: 5px solid #059669; }
.kpi-amber { border-top: 5px solid #D97706; }
.kpi-red { border-top: 5px solid #DC2626; }
.kpi-purple { border-top: 5px solid #7C3AED; }

.panel {
    background: rgba(255,255,255,0.98);
    border: 1px solid rgba(226,232,240,0.95);
    border-radius: 24px;
    padding: 26px 28px;
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.07);
    margin-bottom: 22px;
}

.panel-highlight {
    background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);
    border-left: 6px solid #2563EB;
}

.genba-brief-card {
    background: linear-gradient(135deg, #EFF6FF 0%, #F8FAFC 100%);
    border: 1px solid rgba(191,219,254,0.95);
    border-left: 6px solid #2563EB;
    border-radius: 24px;
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.07);
}

.panel-action {
    background: linear-gradient(135deg, #FFFFFF 0%, #FFFBEB 100%);
    border-left: 6px solid #D97706;
}

.panel-title {
    color: #0F172A;
    font-size: 21px;
    font-weight: 820;
    letter-spacing: -0.25px;
    margin-bottom: 12px;
}

.panel-subtitle {
    color: #64748B;
    font-size: 13px;
    margin-bottom: 16px;
}

.body-text {
    color: #263445;
    font-size: 15.5px;
    line-height: 1.72;
    font-weight: 430;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

.clean-list {
    color: #263445;
    font-size: 15.5px;
    line-height: 1.55;
    font-weight: 430;
    padding-left: 1.15rem;
    margin-top: 0.35rem;
    margin-bottom: 0;
}

.clean-list li {
    margin-bottom: 0.45rem;
    line-height: 1.55;
    padding-left: 0.15rem;
    text-align: left;
}

.clean-list li::marker {
    color: #2563EB;
    font-weight: 700;
}

.sem-container {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 126px;
    border-radius: 22px;
    font-size: 30px;
    font-weight: 850;
    letter-spacing: -0.4px;
}

.sem-red {
    background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
    color: #991B1B;
    border: 1px solid #FCA5A5;
}

.sem-yellow {
    background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
    color: #92400E;
    border: 1px solid #FCD34D;
}

.sem-green {
    background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
    color: #065F46;
    border: 1px solid #6EE7B7;
}

.dimension-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(120px, 1fr));
    gap: 12px;
    margin: 0 0 26px 0;
}

.dimension-card {
    background: rgba(255,255,255,0.98);
    border: 1px solid rgba(203,213,225,0.95);
    border-radius: 18px;
    padding: 14px 16px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
}

.dimension-label {
    color: #64748B;
    font-size: 11.5px;
    font-weight: 780;
    text-transform: uppercase;
    letter-spacing: 0.35px;
    margin-bottom: 8px;
}

.dimension-value {
    font-size: 16px;
    font-weight: 850;
}

.dim-red { color: #B91C1C; }
.dim-yellow { color: #B45309; }
.dim-green { color: #047857; }

.section-heading {
    color: #0F172A;
    font-size: 24px;
    font-weight: 850;
    letter-spacing: -0.5px;
    margin: 8px 0 18px 0;
}

.small-caption {
    color: #64748B;
    font-size: 12.5px;
    font-weight: 500;
}

div[data-testid="stExpander"] {
    background: white;
    border-radius: 18px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# CARGA DE DATOS
# =========================================================

@st.cache_data(ttl=30)
def cargar_csv(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

try:
    df_reporte = cargar_csv(url_reporte)
    df_insights = cargar_csv(url_insights)
except Exception as e:
    st.error(f"No se pudieron cargar los datos desde Google Sheets: {e}")
    st.stop()

# =========================================================
# NORMALIZACIÓN DE COLUMNAS
# =========================================================

def limpiar_nombre_columna(col):
    nombre = (
        str(col)
        .strip()
        .replace("Máquina", "Maquina")
        .replace("Día_Semana", "Dia_Semana")
        .replace("Min_Paro_NoPlanificado", "Min_Paro_No_Planificado")
        .replace("Min_Paros_NoPlanificados", "Min_Paro_No_Planificado")
    )
    aliases = {
        "Costo_Estimado_Perdidas": "Costo_Estimado_Perdida",
        "Preguntas_GEMBA": "Preguntas_GENBA",
        "Preguntas GEMBA": "Preguntas_GENBA",
        "Preguntas GENBA": "Preguntas_GENBA",
    }
    return aliases.get(nombre, nombre)


def normalizar_columnas_dataframe(df):
    df = df.copy()
    df.columns = [limpiar_nombre_columna(c) for c in df.columns]

    if df.columns.duplicated().any():
        columnas_unicas = []
        for col in pd.unique(df.columns):
            repetidas = df.loc[:, df.columns == col]
            if isinstance(repetidas, pd.Series):
                columnas_unicas.append(repetidas.rename(col))
            else:
                columnas_unicas.append(repetidas.bfill(axis=1).iloc[:, 0].rename(col))
        df = pd.concat(columnas_unicas, axis=1)

    return df

df_reporte = normalizar_columnas_dataframe(df_reporte)
df_insights = normalizar_columnas_dataframe(df_insights)

# =========================================================
# LIMPIEZA PROFUNDA DE TEXTO
# =========================================================

def limpiar_texto_profundo(value):
    """
    Limpia texto proveniente de Google Sheets / Relay / GPT.
    Importante: esta función NO intenta convertir código en análisis.
    Solo sanea texto para evitar que Streamlit renderice HTML, Markdown o fragmentos técnicos.
    """
    if value is None:
        return "Sin información disponible."

    if isinstance(value, (list, tuple, set)):
        value = "\n".join([str(item) for item in value])
    elif isinstance(value, dict):
        value = "\n".join([f"{k}: {v}" for k, v in value.items()])

    try:
        if pd.isna(value):
            return "Sin información disponible."
    except Exception:
        pass

    text = str(value).strip()

    for _ in range(12):
        decoded = html.unescape(text)
        if decoded == text:
            break
        text = decoded

    text = text.replace('\\\"', '"').replace("\\'", "'")
    text = text.replace("\\n", "\n").replace("\\r", "\n")
    text = text.replace("\\u003c", "<").replace("\\u003C", "<")
    text = text.replace("\\u003e", ">").replace("\\u003E", ">")
    text = text.replace("\\u0026", "&").replace("\\t", " ")
    text = text.replace("&nbsp;", " ").replace("\u00a0", " ")

    for _ in range(5):
        decoded = html.unescape(text)
        decoded = decoded.replace('\\\"', '"').replace("\\'", "'")
        if decoded == text:
            break
        text = decoded

    # Elimina cercas de Markdown, pero conserva el contenido para poder leer JSON o texto.
    text = re.sub(r"```(?:json|html|python|text|markdown|css|javascript|js)?\s*", "", text, flags=re.IGNORECASE)
    text = text.replace("```", "")
    text = re.sub(r"~~~(?:json|html|python|text|markdown|css|javascript|js)?\s*", "", text, flags=re.IGNORECASE)
    text = text.replace("~~~", "")

    # Neutraliza HTML/CSS/JS embebido.
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?is)&lt;script.*?&lt;/script&gt;", " ", text)
    text = re.sub(r"(?is)&lt;style.*?&lt;/style&gt;", " ", text)
    text = re.sub(r"(?i)<br\s*/?>", "\n", text)
    text = re.sub(r"(?i)&lt;br\s*/?&gt;", "\n", text)

    for _ in range(5):
        previous = text
        text = re.sub(r"(?is)<[^>]*>", " ", text)
        text = re.sub(r"(?is)&lt;[^&]*?&gt;", " ", text)
        if text == previous:
            break

    residues_patterns = [
        r'&lt;[^&]*?&gt;',
        r'/?\s*div\s+class\s*=\s*["\']?body-text["\']?',
        r'/?\s*div\s+class\s*=\s*["\']?[^"\']*["\']?',
        r'\bclass\s*=\s*["\']?body-text["\']?',
        r'\bclass\s*=\s*["\']?[^"\']*["\']?',
        r'\bstyle\s*=\s*["\']?[^"\']*["\']?',
        r'\bdata-[a-z0-9_-]+\s*=\s*["\']?[^"\']*["\']?',
        r'\bbody-text\b',
        r'\bbr\s*/?\b',
        r'\b/?\s*(section|article|ul|ol|li|strong|em)\s*/?\b',
        r'\s*/\s*div\s*',
        r'\s*/\s*b\s*',
        r'\s*/\s*span\s*',
        r'\s*/\s*p\s*',
    ]

    for pattern_item in residues_patterns:
        text = re.sub(pattern_item, " ", text, flags=re.IGNORECASE)

    text = text.replace("<", " ").replace(">", " ")
    text = re.sub(r'(?i)\b/?\s*div\s+class\s*=\s*["\']?body-text["\']?', " ", text)
    text = re.sub(r'(?i)\b/?\s*div\s+class\s*=\s*["\']?[^"\']*["\']?', " ", text)
    text = re.sub(r'(?i)\bclass\s*=\s*["\']?[^"\']*["\']?', " ", text)
    text = re.sub(r'(?i)\bstyle\s*=\s*["\']?[^"\']*["\']?', " ", text)
    text = re.sub(r'(?i)\bdata-[a-z0-9_-]+\s*=\s*["\']?[^"\']*["\']?', " ", text)
    text = re.sub(r'(?i)\b/?\s*(div|span|p|b|strong|em|section|article|ul|ol|li)\b\s*/?', " ", text)
    text = re.sub(r"(?im)^\s{0,3}#{1,6}\s*", "", text)
    text = re.sub(r"(?i)\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"(?i)__(.*?)__", r"\1", text)
    text = re.sub(r"(?i)`([^`]*)`", r"\1", text)
    text = re.sub(r"(?i)\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^\s*[-–—>]+\s*", "- ", text, flags=re.MULTILINE)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    text = re.sub(r'^[\'"]+|[\'"]+$', "", text)
    text = text.strip()

    if text == "":
        return "Sin información disponible."

    return text


# Limpiar columnas de texto de Insights_IA desde el inicio
columnas_texto_insights = [
    "Resumen_Ejecutivo",
    "Hallazgos_Clave",
    "Riesgos",
    "Prioridades",
    "Preguntas_GENBA",
    "Semaforo",
    "Insight_Ejecutivo_Dia",
    "Brief_Genba",
    "Proxima_Accion_Sugerida",
    "Semaforo_OEE",
    "Semaforo_Scrap",
    "Semaforo_Paros",
    "Semaforo_Produccion",
    "Semaforo_Costo"
]

for col in columnas_texto_insights:
    if col in df_insights.columns:
        df_insights[col] = df_insights[col].apply(limpiar_texto_profundo)

# =========================================================
# LIMPIEZA NUMÉRICA
# =========================================================

def parse_number(value, column_name=""):
    if value is None:
        return pd.NA
    try:
        if pd.isna(value):
            return pd.NA
    except Exception:
        pass

    text = str(value).strip()

    if text == "" or text.lower() in ["nan", "none", "no disponible", "n/d"]:
        return pd.NA

    is_cost = "Costo" in column_name or "Perdida" in column_name or "Perdidas" in column_name
    is_percentage = "%" in column_name or "OEE" in column_name or "Scrap" in column_name or "Disponibilidad" in column_name or "Rendimiento" in column_name or "Calidad" in column_name or "Cumplimiento" in column_name

    text = (
        text.replace("%", "")
        .replace("$", "")
        .replace("MXN", "")
        .replace("mxn", "")
        .replace(" ", "")
    )

    text = re.sub(r"[^0-9,.\-]", "", text)

    if is_cost:
        if "," in text and "." in text:
            text = text.replace(",", "")
        elif "," in text:
            parts = text.split(",")
            if len(parts) == 2 and len(parts[1]) <= 2:
                text = text.replace(",", ".")
            else:
                text = text.replace(",", "")
        elif "." in text:
            parts = text.split(".")
            if len(parts) == 2 and len(parts[1]) == 3:
                text = text.replace(".", "")
            elif len(parts) > 2 and all(len(part) == 3 for part in parts[1:]):
                text = text.replace(".", "")

        try:
            return float(text)
        except Exception:
            return pd.NA

    if "," in text and "." not in text:
        parts = text.split(",")
        if len(parts) == 2 and len(parts[1]) == 3 and not is_percentage:
            text = text.replace(",", "")
        else:
            text = text.replace(",", ".")
    elif "," in text and "." in text:
        text = text.replace(",", "")

    text = re.sub(r"[^0-9.\-]", "", text)

    try:
        return float(text)
    except Exception:
        return pd.NA


def convertir_numericos(df):
    numeric_cols = [
        "OEE_%", "Meta_OEE_%", "Scrap_%", "Meta_Scrap_%",
        "Min_Paro_No_Planificado", "Meta_Max_Paro_Min", "Eventos_Paro",
        "Produccion_Meta", "Produccion_Real", "Cumplimiento_Produccion_%",
        "Disponibilidad_%", "Rendimiento_%", "Calidad_%", "Costo_Estimado_Perdida"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: parse_number(x, col))
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


df_reporte = convertir_numericos(df_reporte)
df_insights = convertir_numericos(df_insights)

percentage_cols = [
    "OEE_%", "Meta_OEE_%", "Scrap_%", "Meta_Scrap_%",
    "Cumplimiento_Produccion_%", "Disponibilidad_%",
    "Rendimiento_%", "Calidad_%"
]

def normalizar_porcentaje_a_100(series):
    valores = series.dropna()
    if len(valores) == 0:
        return series

    max_abs = valores.abs().max()

    # Si viene como 0.83, convertir a 83. Si viene como 8300, convertir a 83.
    if max_abs <= 1.5:
        return series * 100
    if max_abs > 100:
        return series / 100

    return series


for col in percentage_cols:
    if col in df_reporte.columns:
        df_reporte[col] = normalizar_porcentaje_a_100(df_reporte[col])

    if col in df_insights.columns:
        df_insights[col] = normalizar_porcentaje_a_100(df_insights[col])

if "Fecha" in df_reporte.columns:
    df_reporte["Fecha"] = pd.to_datetime(df_reporte["Fecha"], errors="coerce")
    df_reporte = df_reporte.sort_values("Fecha", na_position="first")

if "Fecha_Dato" in df_insights.columns:
    df_insights["Fecha_Dato"] = pd.to_datetime(df_insights["Fecha_Dato"], errors="coerce")
    df_insights = df_insights.sort_values("Fecha_Dato", na_position="first")

df = df_reporte.copy()

if len(df) == 0:
    st.error("La hoja Reporte_Diario_Maquinas no contiene datos.")
    st.stop()

if len(df_insights) == 0:
    df_insights = pd.DataFrame([{
        "Semaforo": "Verde",
        "Resumen_Ejecutivo": "Sin análisis IA registrado todavía.",
        "Hallazgos_Clave": "Sin hallazgos disponibles.",
        "Riesgos": "Sin riesgos disponibles.",
        "Prioridades": "Sin prioridades disponibles.",
        "Preguntas_GENBA": "Sin preguntas disponibles."
    }])

ultimo = df.iloc[-1]
ultimo_insight = df_insights.iloc[-1]

# =========================================================
# FUNCIONES GENERALES
# =========================================================

def safe_value(row, column, default="N/D"):
    try:
        value = row[column]
        if pd.isna(value):
            return default
        return value
    except Exception:
        return default


def format_number(value, decimals=1):
    try:
        if pd.isna(value):
            return "N/D"
        return f"{float(value):,.{decimals}f}"
    except Exception:
        return str(value)


def format_money(value):
    try:
        if pd.isna(value):
            return "N/D"
        return f"${float(value):,.0f}"
    except Exception:
        return str(value)


def format_date(value):
    try:
        if pd.isna(value):
            return "N/D"
        if isinstance(value, pd.Timestamp):
            return value.strftime("%Y-%m-%d")
        return str(value)
    except Exception:
        return str(value)


def render_kpi(label, value, foot, accent):
    st.markdown(
        f'<div class="kpi-card {accent}">'
        f'<div class="kpi-label">{html.escape(str(label))}</div>'
        f'<div class="kpi-value">{html.escape(str(value))}</div>'
        f'<div class="kpi-foot">{html.escape(str(foot))}</div>'
        '</div>',
        unsafe_allow_html=True
    )


def render_panel(title, content, subtitle=None, extra_class=""):
    subtitle_html = f'<div class="panel-subtitle">{html.escape(str(subtitle))}</div>' if subtitle else ""
    clean_content = limpiar_texto_profundo(content)
    clean_content = html.escape(clean_content).replace("\n", "<br>")
    panel_class = "panel"
    if extra_class:
        panel_class = f"panel {html.escape(str(extra_class))}"

    st.markdown(
        f'<div class="{panel_class}">'
        f'<div class="panel-title">{html.escape(str(title))}</div>'
        f'{subtitle_html}'
        f'<div class="body-text">{clean_content}</div>'
        '</div>',
        unsafe_allow_html=True
    )


def render_panel_lines(title, lines, subtitle=None):
    text = "\n".join([str(x) for x in lines])
    render_panel(title, text, subtitle)


def render_optional_panel(title, content, subtitle=None, extra_class=""):
    if not texto_util(content):
        return
    render_panel(title, content, subtitle, extra_class)


def texto_a_items_lista(content):
    clean = limpiar_texto_profundo(content)
    if not texto_util(clean, min_chars=2):
        return []

    clean = clean.replace("\r", "\n")
    clean = re.sub(r"(?i)\s*(?:<br\s*/?>|&lt;br\s*/?&gt;)\s*", "\n", clean)
    clean = re.sub(r"(?m)^\s*(?:[-•●◦▪]+|\d+[\).\-\:]|[a-zA-Z][\).\-\:])\s*", "", clean)
    clean = re.sub(r"\s*[•●◦▪]\s+", "\n", clean)
    clean = re.sub(r"\s+(?=\d+[\).\-\:]\s+)", "\n", clean)
    clean = re.sub(r"\s+(?=[-–—]\s+)", "\n", clean)
    clean = re.sub(r"\n+", "\n", clean)

    raw_items = []
    for line in clean.split("\n"):
        line = line.strip()
        if not line:
            continue

        split_items = re.split(r"\s*(?:;|\|)\s+(?=[A-ZÁÉÍÓÚÑ¿])", line)
        raw_items.extend(split_items if len(split_items) > 1 else [line])

    items = []
    for item in raw_items:
        item = limpiar_texto_profundo(item)
        item = re.sub(r"^\s*(?:[-•●◦▪]+|\d+[\).\-\:]|[a-zA-Z][\).\-\:])\s*", "", item)
        item = re.sub(r"^\s*(?:[-–—]\s*)+", "", item)
        item = re.sub(r"\s+", " ", item).strip(" -–—•●◦▪\t\r\n")
        if item and item.lower() not in ["sin información disponible.", "sin informacion disponible.", "n/d"]:
            items.append(item)

    return items


def render_list_panel(title, content, ordered=False, subtitle=None, extra_class=""):
    items = texto_a_items_lista(content)
    if not items:
        return

    subtitle_html = f'<div class="panel-subtitle">{html.escape(str(subtitle))}</div>' if subtitle else ""
    panel_class = "panel"
    if extra_class:
        panel_class = f"panel {html.escape(str(extra_class))}"

    tag = "ol" if ordered else "ul"
    list_items = "".join(f"<li>{html.escape(item)}</li>" for item in items)

    st.markdown(
        f'<div class="{panel_class}">'
        f'<div class="panel-title">{html.escape(str(title))}</div>'
        f'{subtitle_html}'
        f'<{tag} class="clean-list">{list_items}</{tag}>'
        '</div>',
        unsafe_allow_html=True
    )


def render_dimension_semaforos(insights):
    dimensiones = [
        ("OEE", "Semaforo_OEE"),
        ("Scrap", "Semaforo_Scrap"),
        ("Paros", "Semaforo_Paros"),
        ("Producción", "Semaforo_Produccion"),
        ("Costo", "Semaforo_Costo"),
    ]

    cards = []
    for label, campo in dimensiones:
        if campo not in insights:
            continue
        estado = normalizar_semaforo(insights.get(campo))
        css = "dim-red" if estado == "Rojo" else "dim-yellow" if estado == "Amarillo" else "dim-green"
        cards.append(
            '<div class="dimension-card">'
            f'<div class="dimension-label">{html.escape(label)}</div>'
            f'<div class="dimension-value {css}">{html.escape(estado)}</div>'
            '</div>'
        )

    if cards:
        st.markdown(
            '<div class="section-heading" style="font-size:20px; margin-top:0;">Semáforo por Dimensión</div>'
            '<div class="dimension-grid">' + "".join(cards) + '</div>',
            unsafe_allow_html=True
        )


def existe(dataframe, col):
    return col in dataframe.columns


def construir_tabla_resumen(df_base, grupo):
    agg_dict = {}

    if existe(df_base, "OEE_%"):
        agg_dict["OEE_Promedio"] = ("OEE_%", "mean")
    if existe(df_base, "Scrap_%"):
        agg_dict["Scrap_Promedio"] = ("Scrap_%", "mean")
    if existe(df_base, "Min_Paro_No_Planificado"):
        agg_dict["Paros_Total"] = ("Min_Paro_No_Planificado", "sum")
    if existe(df_base, "Costo_Estimado_Perdida"):
        agg_dict["Costo_Total"] = ("Costo_Estimado_Perdida", "sum")

    if not agg_dict:
        return pd.DataFrame()

    tabla = df_base.groupby(grupo, dropna=False).agg(**agg_dict).reset_index()

    for col in tabla.columns:
        if "Promedio" in col:
            tabla[col] = tabla[col].round(2)
        if "Paros" in col or "Costo" in col:
            tabla[col] = tabla[col].round(0)

    return tabla


def serie_por_turno(df_base, valor_col, agg="mean"):
    columnas = ["Fecha", "Turno", valor_col]
    if not all(c in df_base.columns for c in columnas):
        return pd.DataFrame()

    datos = df_base[columnas].dropna(subset=["Fecha", valor_col])
    if len(datos) == 0:
        return pd.DataFrame(columns=columnas)

    agg_func = "sum" if agg == "sum" else "mean"
    serie = (
        datos.groupby(["Fecha", "Turno"], as_index=False)[valor_col]
        .agg(agg_func)
        .sort_values("Fecha")
    )

    return serie


PALETA_TURNOS = ["#2563EB", "#059669", "#D97706", "#7C3AED", "#DC2626", "#0891B2"]


def aplicar_layout_linea(fig, titulo, eje_y, altura=350):
    fig.update_traces(line=dict(width=2.8), marker=dict(size=5.5))
    fig.update_layout(
        height=altura,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Arial", size=12.5, color="#334155"),
        title=dict(text=titulo, font=dict(size=18, color="#0F172A")),
        margin=dict(l=16, r=16, t=52, b=30),
        legend_title_text="Turno",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified"
    )
    fig.update_xaxes(showgrid=False, title=None, tickformat="%d %b", automargin=True)
    fig.update_yaxes(gridcolor="#E2E8F0", title=eje_y)
    return fig


def evaluar_cambio_indicador(actual, anterior, tolerancia=0, tolerancia_pct=None, mejora_si_sube=True):
    if pd.isna(actual) or pd.isna(anterior):
        return 0

    actual = float(actual)
    anterior = float(anterior)
    delta = actual - anterior

    if tolerancia_pct is not None:
        if anterior == 0:
            if actual == 0:
                return 0
        elif abs(delta) / abs(anterior) < tolerancia_pct:
            return 0
    elif abs(delta) < tolerancia:
        return 0

    if mejora_si_sube:
        return 1 if delta > 0 else -1
    return 1 if delta < 0 else -1


def calcular_tendencia_periodo_anterior(df_base, grupo, elemento):
    if "Fecha" not in df_base.columns or grupo not in df_base.columns:
        return "Sin histórico previo"

    if pd.isna(elemento):
        datos = df_base[df_base[grupo].isna()].copy()
    else:
        datos = df_base[df_base[grupo] == elemento].copy()

    datos = datos.dropna(subset=["Fecha"])
    fechas = sorted(datos["Fecha"].dropna().unique())
    if len(fechas) < 2:
        return "Sin histórico previo"

    fecha_anterior = fechas[-2]
    fecha_actual = fechas[-1]
    actual = datos[datos["Fecha"] == fecha_actual]
    anterior = datos[datos["Fecha"] == fecha_anterior]

    if len(actual) == 0 or len(anterior) == 0:
        return "Sin histórico previo"

    metricas = []
    if "OEE_%" in datos.columns:
        metricas.append((actual["OEE_%"].mean(), anterior["OEE_%"].mean(), 0.5, None, True))
    if "Scrap_%" in datos.columns:
        metricas.append((actual["Scrap_%"].mean(), anterior["Scrap_%"].mean(), 0.2, None, False))
    if "Min_Paro_No_Planificado" in datos.columns:
        metricas.append((actual["Min_Paro_No_Planificado"].sum(), anterior["Min_Paro_No_Planificado"].sum(), 0, 0.05, False))
    if "Costo_Estimado_Perdida" in datos.columns:
        metricas.append((actual["Costo_Estimado_Perdida"].sum(), anterior["Costo_Estimado_Perdida"].sum(), 0, 0.05, False))

    if not metricas:
        return "Sin histórico previo"

    score = sum(
        evaluar_cambio_indicador(valor_actual, valor_anterior, tolerancia_abs, tolerancia_pct, mejora_si_sube)
        for valor_actual, valor_anterior, tolerancia_abs, tolerancia_pct, mejora_si_sube in metricas
    )

    if score > 0:
        return "🟢 ↑ Mejorando"
    if score < 0:
        return "🔴 ↓ Deteriorando"
    return "🟡 → Sin cambio relevante"


def construir_comparativo_ejecutivo(df_base, meta_oee_ref=None, meta_scrap_ref=None):
    tablas = []

    for nivel, grupo in [("Linea", "Linea"), ("Turno", "Turno"), ("Maquina", "Maquina")]:
        if not existe(df_base, grupo):
            continue

        tabla = construir_tabla_resumen(df_base, grupo)
        if len(tabla) == 0:
            continue

        tabla = tabla.rename(columns={grupo: "Elemento"})
        tabla.insert(0, "Nivel", nivel)
        tabla["Tendencia vs Periodo Anterior"] = tabla["Elemento"].apply(
            lambda elemento: calcular_tendencia_periodo_anterior(df_base, grupo, elemento)
        )
        tablas.append(tabla)

    if not tablas:
        return pd.DataFrame()

    comparativo = pd.concat(tablas, ignore_index=True, sort=False)

    for col in ["OEE_Promedio", "Scrap_Promedio", "Paros_Total", "Costo_Total"]:
        if col not in comparativo.columns:
            comparativo[col] = pd.NA

    comparativo = comparativo.sort_values(
        by=["Costo_Total", "Paros_Total"],
        ascending=[False, False],
        na_position="last"
    )

    columnas = ["Nivel", "Elemento", "OEE_Promedio", "Scrap_Promedio", "Paros_Total", "Costo_Total", "Tendencia vs Periodo Anterior"]
    return comparativo[columnas]

# =========================================================
# CONTROL DE CALIDAD DEL TEXTO IA
# =========================================================

INSIGHT_FIELDS = [
    "Resumen_Ejecutivo",
    "Hallazgos_Clave",
    "Riesgos",
    "Prioridades",
    "Preguntas_GENBA",
    "Semaforo"
]

OPTIONAL_INSIGHT_FIELDS = [
    "Insight_Ejecutivo_Dia",
    "Semaforo_OEE",
    "Semaforo_Scrap",
    "Semaforo_Paros",
    "Semaforo_Produccion",
    "Semaforo_Costo",
    "Brief_Genba",
    "Proxima_Accion_Sugerida"
]

CODE_MARKERS = [
    "import streamlit",
    "import pandas",
    "plotly.express",
    "st.markdown",
    "st.dataframe",
    "st.plotly_chart",
    "st.set_page_config",
    "def ",
    "pd.read_csv",
    "unsafe_allow_html",
    "<style",
    "</style>",
    "class=",
    "```python",
    "```html"
]

KEY_ALIASES = {
    "resumen_ejecutivo": ["Resumen_Ejecutivo", "Resumen Ejecutivo", "resumen", "resumen_ejecutivo"],
    "hallazgos_clave": ["Hallazgos_Clave", "Hallazgos Clave", "hallazgos", "hallazgos_clave"],
    "riesgos": ["Riesgos", "riesgos", "Riesgos_Relevantes", "riesgos_relevantes"],
    "prioridades": ["Prioridades", "prioridades", "Prioridades_Analisis", "prioridades_analisis"],
    "preguntas_genba": [
        "Preguntas_GENBA",
        "Preguntas GENBA",
        "preguntas_genba",
        "Preguntas_GEMBA",
        "Preguntas GEMBA",
        "preguntas_gemba",
        "preguntas"
    ],
    "preguntas_gemba": [
        "Preguntas_GENBA",
        "Preguntas GENBA",
        "preguntas_genba",
        "Preguntas_GEMBA",
        "Preguntas GEMBA",
        "preguntas_gemba",
        "preguntas"
    ],
    "semaforo": ["Semaforo", "Semáforo", "semaforo", "semáforo"],
    "insight_ejecutivo_dia": ["Insight_Ejecutivo_Dia", "Insight Ejecutivo Dia", "Insight Ejecutivo Día"],
    "semaforo_oee": ["Semaforo_OEE", "Semáforo_OEE", "semaforo_oee"],
    "semaforo_scrap": ["Semaforo_Scrap", "Semáforo_Scrap", "semaforo_scrap"],
    "semaforo_paros": ["Semaforo_Paros", "Semáforo_Paros", "semaforo_paros"],
    "semaforo_produccion": ["Semaforo_Produccion", "Semáforo_Produccion", "semaforo_produccion"],
    "semaforo_costo": ["Semaforo_Costo", "Semáforo_Costo", "semaforo_costo"],
    "brief_genba": ["Brief_Genba", "Brief GENBA", "Brief_GEMBA", "Brief GEMBA"],
    "proxima_accion_sugerida": ["Proxima_Accion_Sugerida", "Proxima Accion Sugerida", "Próxima Acción Sugerida"]
}


def normalizar_clave(texto):
    txt = str(texto).strip().lower()
    txt = (
        txt.replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
    )
    txt = re.sub(r"[^a-z0-9]+", "_", txt).strip("_")
    return txt


def es_salida_tecnica(value):
    """
    Detecta si una celda trae código, HTML, CSS o instrucciones técnicas en lugar de análisis.
    Cuando esto ocurre, el dashboard NO debe mostrarlo.
    """
    if value is None:
        return False
    try:
        if pd.isna(value):
            return False
    except Exception:
        pass

    raw = str(value).strip()
    if raw == "":
        return False

    lower = raw.lower()
    score = sum(1 for marker in CODE_MARKERS if marker in lower)

    # Código muy largo o con múltiples marcadores técnicos.
    if score >= 2:
        return True

    # Caso típico: GPT devolvió una app completa, un bloque Python o HTML.
    if len(raw) > 1200 and score >= 1:
        return True

    # Caso típico: se pegó CSS/HTML del render.
    if ("{" in raw and "}" in raw and ";" in raw and ("background:" in lower or "font-size:" in lower)):
        return True

    return False


def texto_util(value, min_chars=12):
    if value is None:
        return False

    try:
        if pd.isna(value):
            return False
    except Exception:
        pass

    clean = limpiar_texto_profundo(value)
    if clean.lower() in ["", "n/d", "nan", "none", "sin información disponible."]:
        return False

    if es_salida_tecnica(clean):
        return False

    return len(clean.strip()) >= min_chars


def extraer_json(value):
    """
    Soporta tres casos frecuentes en Relay/GPT:
    1. JSON puro.
    2. JSON dentro de ```json ...```.
    3. JSON guardado como texto escapado en una celda de Sheets.
    """
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass

    text = str(value).strip()

    for _ in range(10):
        decoded = html.unescape(text)
        if decoded == text:
            break
        text = decoded

    text = text.replace("\\n", "\n").replace('\\"', '"').strip()
    text = re.sub(r"```(?:json|text|markdown)?\s*", "", text, flags=re.IGNORECASE)
    text = text.replace("```", "").strip()

    candidates = [text]

    # Intenta extraer el primer objeto JSON grande.
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        candidates.append(match.group(0))

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, list) and parsed:
                parsed = parsed[-1]
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

        try:
            parsed = ast.literal_eval(candidate)
            if isinstance(parsed, list) and parsed:
                parsed = parsed[-1]
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass

    return None


def buscar_en_json(parsed, campo):
    if not isinstance(parsed, dict):
        return None

    objetivo = normalizar_clave(campo)
    posibles = [normalizar_clave(x) for x in KEY_ALIASES.get(objetivo, [campo])]

    normalizado = {normalizar_clave(k): v for k, v in parsed.items()}

    for key in posibles:
        if key in normalizado:
            return normalizado[key]

    return None


def buscar_campo_en_fila(row, campo):
    """
    Busca un campo de insight de forma robusta:
    - primero como columna directa;
    - después como alias;
    - después dentro de un JSON completo pegado en cualquier celda de la fila.
    """
    if row is None or len(row) == 0:
        return None

    posibles = KEY_ALIASES.get(normalizar_clave(campo), [campo])

    for posible in posibles:
        if posible in row.index:
            value = row[posible]
            if texto_util(value, min_chars=3 if str(campo).startswith("Semaforo") else 12):
                return limpiar_texto_profundo(value)

            parsed = extraer_json(value)
            json_value = buscar_en_json(parsed, campo)
            if texto_util(json_value, min_chars=3 if str(campo).startswith("Semaforo") else 12):
                return limpiar_texto_profundo(json_value)

    for col in row.index:
        value = row[col]
        parsed = extraer_json(value)
        json_value = buscar_en_json(parsed, campo)
        if texto_util(json_value, min_chars=3 if str(campo).startswith("Semaforo") else 12):
            return limpiar_texto_profundo(json_value)

    return None


def normalizar_semaforo(value):
    text = limpiar_texto_profundo(value).lower() if value is not None else ""
    if "rojo" in text:
        return "Rojo"
    if "amarillo" in text or "ámbar" in text or "ambar" in text:
        return "Amarillo"
    if "verde" in text:
        return "Verde"
    return "Verde"


def primer_valor_serie(df_base, columna, modo="ultimo"):
    if columna not in df_base.columns:
        return None
    serie = df_base[columna].dropna()
    if len(serie) == 0:
        return None
    if modo == "primero":
        return serie.iloc[0]
    return serie.iloc[-1]


def top_categoria(df_base, grupo, valor, funcion="sum"):
    if grupo not in df_base.columns or valor not in df_base.columns:
        return None, None

    datos = df_base[[grupo, valor]].dropna()
    if len(datos) == 0:
        return None, None

    if funcion == "mean":
        serie = datos.groupby(grupo)[valor].mean()
    else:
        serie = datos.groupby(grupo)[valor].sum()

    if len(serie) == 0:
        return None, None

    serie = serie.sort_values(ascending=False)
    return serie.index[0], serie.iloc[0]


def generar_insights_desde_datos(df_base):
    """
    Fallback ejecutivo: si Relay/GPT manda código o texto inválido,
    el dashboard genera un análisis básico desde los datos operativos.
    Así nunca se muestra código al usuario final.
    """
    registros = len(df_base)

    fecha_inicio = format_date(df_base["Fecha"].min()) if existe(df_base, "Fecha") else "N/D"
    fecha_fin = format_date(df_base["Fecha"].max()) if existe(df_base, "Fecha") else "N/D"

    oee_prom = df_base["OEE_%"].mean() if existe(df_base, "OEE_%") else None
    scrap_prom = df_base["Scrap_%"].mean() if existe(df_base, "Scrap_%") else None
    paros_total = df_base["Min_Paro_No_Planificado"].sum() if existe(df_base, "Min_Paro_No_Planificado") else None
    costo_total = df_base["Costo_Estimado_Perdida"].sum() if existe(df_base, "Costo_Estimado_Perdida") else None

    meta_oee = primer_valor_serie(df_base, "Meta_OEE_%")
    meta_scrap = primer_valor_serie(df_base, "Meta_Scrap_%")

    dias_fuera_oee = int((df_base["OEE_%"] < meta_oee).sum()) if meta_oee is not None and existe(df_base, "OEE_%") else 0
    dias_fuera_scrap = int((df_base["Scrap_%"] > meta_scrap).sum()) if meta_scrap is not None and existe(df_base, "Scrap_%") else 0

    peor_fecha = "N/D"
    peor_oee = None
    if existe(df_base, "OEE_%") and len(df_base["OEE_%"].dropna()) > 0:
        idx_peor = df_base["OEE_%"].idxmin()
        peor_oee = df_base.loc[idx_peor, "OEE_%"]
        peor_fecha = format_date(df_base.loc[idx_peor, "Fecha"]) if existe(df_base, "Fecha") else "N/D"

    top_causa, top_minutos = top_categoria(df_base, "Causa_Principal_Paro", "Min_Paro_No_Planificado")
    top_linea_costo, top_costo_linea = top_categoria(df_base, "Linea", "Costo_Estimado_Perdida")
    top_maquina_costo, top_costo_maquina = top_categoria(df_base, "Maquina", "Costo_Estimado_Perdida")
    top_turno_paros, top_min_turno = top_categoria(df_base, "Turno", "Min_Paro_No_Planificado")

    score = 0
    if oee_prom is not None and meta_oee is not None and oee_prom < meta_oee:
        score += 2
    if scrap_prom is not None and meta_scrap is not None and scrap_prom > meta_scrap:
        score += 2
    if registros > 0 and dias_fuera_oee / registros >= 0.35:
        score += 1
    if registros > 0 and dias_fuera_scrap / registros >= 0.35:
        score += 1
    if paros_total is not None and paros_total > 0:
        score += 1

    semaforo = "Rojo" if score >= 4 else "Amarillo" if score >= 2 else "Verde"

    resumen = (
        f"El periodo analizado comprende {registros:,} registros entre {fecha_inicio} y {fecha_fin}. "
        f"El OEE promedio es {format_number(oee_prom, 1)}% frente a una meta de {format_number(meta_oee, 1)}%, "
        f"con {dias_fuera_oee} registros fuera de meta. El scrap promedio es {format_number(scrap_prom, 2)}% "
        f"frente a una meta de {format_number(meta_scrap, 2)}%, con {dias_fuera_scrap} registros fuera de objetivo. "
        f"Los paros no planificados acumulan {format_number(paros_total, 0)} minutos y el costo estimado de pérdida asciende a {format_money(costo_total)}."
    )

    hallazgos = (
        f"- El peor desempeño de OEE se observa el {peor_fecha}, con {format_number(peor_oee, 1)}%.\n"
        f"- La causa con mayor acumulación de minutos de paro es {top_causa if top_causa else 'N/D'}, "
        f"con {format_number(top_minutos, 0)} minutos.\n"
        f"- La línea con mayor costo estimado acumulado es {top_linea_costo if top_linea_costo else 'N/D'}, "
        f"con {format_money(top_costo_linea)}.\n"
        f"- La máquina con mayor impacto económico estimado es {top_maquina_costo if top_maquina_costo else 'N/D'}, "
        f"con {format_money(top_costo_maquina)}.\n"
        f"- El turno con mayor concentración de paros es {top_turno_paros if top_turno_paros else 'N/D'}, "
        f"con {format_number(top_min_turno, 0)} minutos."
    )

    riesgos = (
        "- Riesgo de inestabilidad operativa si el OEE continúa por debajo de la meta durante varios registros consecutivos.\n"
        "- Riesgo de pérdida económica acumulada por concentración de paros no planificados en causas recurrentes.\n"
        "- Riesgo de deterioro de calidad si el scrap permanece por encima del objetivo y no se valida la relación con máquina, turno y causa de paro.\n"
        "- Riesgo de decisiones reactivas si la operación solo atiende el último registro y no la tendencia histórica."
    )

    prioridades = (
        "- Priorizar la revisión de la causa principal de paro con mayor acumulación de minutos.\n"
        "- Comparar los turnos con mayor y menor desempeño para detectar diferencias de método, disciplina operativa o condiciones de arranque.\n"
        "- Revisar las máquinas con mayor costo estimado para validar si el impacto proviene de paro, scrap o incumplimiento de producción.\n"
        "- Analizar los días fuera de meta de OEE y scrap como patrón, no como eventos aislados.\n"
        "- Validar en piso si la información registrada coincide con la realidad operativa observada."
    )

    preguntas = (
        "- ¿Qué condición específica se repite cuando aparece la principal causa de paro?\n"
        "- ¿Qué diferencia operativa existe entre el turno con mejor desempeño y el turno con mayor pérdida?\n"
        "- ¿El scrap aumenta después de paros, ajustes, arranques o cambios de condición de máquina?\n"
        "- ¿La máquina de mayor costo tiene un estándar de reacción claro ante desviaciones?\n"
        "- ¿Los registros capturan la causa real o solo la consecuencia visible del problema?"
    )

    return {
        "Resumen_Ejecutivo": resumen,
        "Hallazgos_Clave": hallazgos,
        "Riesgos": riesgos,
        "Prioridades": prioridades,
        "Preguntas_GENBA": preguntas,
        "Semaforo": semaforo
    }


def construir_insights_finales(df_base, row_insight):
    fallback = generar_insights_desde_datos(df_base)
    resultado = {}

    for campo in INSIGHT_FIELDS:
        value = buscar_campo_en_fila(row_insight, campo)
        if value is None:
            value = fallback[campo]

        if campo == "Semaforo":
            resultado[campo] = normalizar_semaforo(value)
        else:
            resultado[campo] = limpiar_texto_profundo(value)

    for campo in OPTIONAL_INSIGHT_FIELDS:
        value = buscar_campo_en_fila(row_insight, campo)
        if value is None:
            continue

        if campo.startswith("Semaforo_"):
            resultado[campo] = normalizar_semaforo(value)
        else:
            resultado[campo] = limpiar_texto_profundo(value)

    return resultado


def vista_segura_insights(df_base):
    """
    Evita que el histórico de insights muestre código crudo.
    """
    vista = df_base.copy()

    for col in vista.columns:
        if vista[col].dtype == "object":
            vista[col] = vista[col].apply(
                lambda x: "Contenido técnico omitido: no es análisis IA válido."
                if es_salida_tecnica(x)
                else limpiar_texto_profundo(x)
            )

    return vista


# =========================================================
# FILTROS
# =========================================================

with st.sidebar:
    st.markdown("## Filtros del dashboard")

    if existe(df, "Linea"):
        lineas = sorted(df["Linea"].dropna().unique())
        filtro_linea = st.multiselect("Línea", lineas, default=lineas)
        df = df[df["Linea"].isin(filtro_linea)]

    if existe(df, "Turno"):
        turnos = sorted(df["Turno"].dropna().unique())
        filtro_turno = st.multiselect("Turno", turnos, default=turnos)
        df = df[df["Turno"].isin(filtro_turno)]

    if existe(df, "Maquina"):
        maquinas = sorted(df["Maquina"].dropna().unique())
        filtro_maquina = st.multiselect("Máquina", maquinas, default=maquinas)
        df = df[df["Maquina"].isin(filtro_maquina)]

if len(df) == 0:
    st.error("No hay datos disponibles con los filtros seleccionados.")
    st.stop()

ultimo = df.iloc[-1]

# =========================================================
# MÉTRICAS HISTÓRICAS
# =========================================================

oee_prom = df["OEE_%"].mean() if existe(df, "OEE_%") else None
scrap_prom = df["Scrap_%"].mean() if existe(df, "Scrap_%") else None
paros_total = df["Min_Paro_No_Planificado"].sum() if existe(df, "Min_Paro_No_Planificado") else None
costo_total = df["Costo_Estimado_Perdida"].sum() if existe(df, "Costo_Estimado_Perdida") else None

meta_oee = df["Meta_OEE_%"].dropna().iloc[-1] if existe(df, "Meta_OEE_%") and len(df["Meta_OEE_%"].dropna()) > 0 else None
meta_scrap = df["Meta_Scrap_%"].dropna().iloc[-1] if existe(df, "Meta_Scrap_%") and len(df["Meta_Scrap_%"].dropna()) > 0 else None

dias_fuera_oee = int((df["OEE_%"] < meta_oee).sum()) if meta_oee is not None and existe(df, "OEE_%") else 0
dias_fuera_scrap = int((df["Scrap_%"] > meta_scrap).sum()) if meta_scrap is not None and existe(df, "Scrap_%") else 0

insights_finales = construir_insights_finales(df, ultimo_insight)


# =========================================================
# HEADER
# =========================================================

fecha_actual = format_date(safe_value(ultimo, "Fecha", safe_value(ultimo_insight, "Fecha_Dato")))
linea_actual = safe_value(ultimo, "Linea", safe_value(ultimo_insight, "Linea"))
maquina_actual = safe_value(ultimo, "Maquina", safe_value(ultimo_insight, "Maquina"))
turno_actual = safe_value(ultimo, "Turno", safe_value(ultimo_insight, "Turno"))

st.markdown(f"""
<div class="hero">
    <div class="hero-title">AI Operational Command Center</div>
    <div class="hero-subtitle">
        Centro ejecutivo de monitoreo operativo con análisis histórico, comparación contra metas, alertas inteligentes e insights generados por IA.
    </div>
    <div class="hero-badge">
        Histórico analizado: {len(df):,} registros · Último registro: {fecha_actual} · {linea_actual} · {maquina_actual} · {turno_actual}
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# KPIs HISTÓRICOS
# =========================================================

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    render_kpi(
        "OEE Promedio",
        f"{format_number(oee_prom, 1)}%",
        f"Meta: {format_number(meta_oee, 1)}% · Fuera meta: {dias_fuera_oee}",
        "kpi-blue"
    )

with k2:
    render_kpi(
        "Scrap Promedio",
        f"{format_number(scrap_prom, 2)}%",
        f"Meta: {format_number(meta_scrap, 2)}% · Fuera meta: {dias_fuera_scrap}",
        "kpi-red"
    )

with k3:
    render_kpi(
        "Paros Totales",
        f"{format_number(paros_total, 0)} min",
        "Acumulado histórico filtrado",
        "kpi-amber"
    )

with k4:
    render_kpi(
        "Costo Total",
        format_money(costo_total),
        "Pérdida estimada acumulada",
        "kpi-green"
    )

with k5:
    render_kpi(
        "Registros",
        f"{len(df):,}",
        "Base histórica analizada",
        "kpi-purple"
    )

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# SEMÁFORO IA Y RESUMEN
# =========================================================

left, right = st.columns([0.9, 2.1])

with left:
    semaforo = str(insights_finales.get("Semaforo", "Verde")).strip().lower()

    if "rojo" in semaforo:
        sem_class = "sem-red"
        sem_label = "🔴 ROJO"
    elif "amarillo" in semaforo:
        sem_class = "sem-yellow"
        sem_label = "🟡 AMARILLO"
    else:
        sem_class = "sem-green"
        sem_label = "🟢 VERDE"

    st.markdown(
        '<div class="panel">'
        '<div class="panel-title">Semáforo Ejecutivo IA</div>'
        f'<div class="{sem_class} sem-container">{sem_label}</div>'
        '<div class="small-caption" style="margin-top:14px;">'
        'Clasificación generada por IA según desviaciones, impacto y riesgo operativo.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

with right:
    render_panel(
        "Resumen Ejecutivo IA",
        insights_finales["Resumen_Ejecutivo"],
        "Último análisis generado por Relay + GPT."
    )

if "Insight_Ejecutivo_Dia" in insights_finales:
    render_optional_panel(
        "Insight Ejecutivo del Día",
        insights_finales["Insight_Ejecutivo_Dia"],
        "Lectura ejecutiva del último análisis disponible.",
        "panel-highlight"
    )

render_dimension_semaforos(insights_finales)

# =========================================================
# GRÁFICAS HISTÓRICAS POR TURNO
# =========================================================

st.markdown('<div class="section-heading">Análisis Histórico del Desempeño Operativo</div>', unsafe_allow_html=True)

g1, g2 = st.columns(2)

with g1:
    if existe(df, "Fecha") and existe(df, "OEE_%") and existe(df, "Turno"):
        serie_oee = serie_por_turno(df, "OEE_%")

        fig_oee = px.line(
            serie_oee,
            x="Fecha",
            y="OEE_%",
            color="Turno",
            markers=True,
            title="Tendencia Histórica de OEE por Turno",
            color_discrete_sequence=PALETA_TURNOS
        )

        if meta_oee is not None:
            fig_oee.add_hline(
                y=meta_oee,
                line_dash="dash",
                line_color="#DC2626",
                annotation_text="Meta OEE",
                annotation_position="top left"
            )

        aplicar_layout_linea(fig_oee, "Tendencia Historica de OEE por Turno", "OEE_%")
        st.plotly_chart(fig_oee, use_container_width=True)

with g2:
    if existe(df, "Fecha") and existe(df, "Scrap_%") and existe(df, "Turno"):
        serie_scrap = serie_por_turno(df, "Scrap_%")

        fig_scrap = px.line(
            serie_scrap,
            x="Fecha",
            y="Scrap_%",
            color="Turno",
            markers=True,
            title="Tendencia Histórica de Scrap por Turno",
            color_discrete_sequence=PALETA_TURNOS
        )

        if meta_scrap is not None:
            fig_scrap.add_hline(
                y=meta_scrap,
                line_dash="dash",
                line_color="#DC2626",
                annotation_text="Meta Scrap",
                annotation_position="top left"
            )

        aplicar_layout_linea(fig_scrap, "Tendencia Historica de Scrap por Turno", "Scrap_%")
        st.plotly_chart(fig_scrap, use_container_width=True)

g3, g4 = st.columns(2)

with g3:
    if existe(df, "Fecha") and existe(df, "Min_Paro_No_Planificado") and existe(df, "Turno"):
        serie_paros = serie_por_turno(df, "Min_Paro_No_Planificado", agg="sum")

        fig_paros = px.line(
            serie_paros,
            x="Fecha",
            y="Min_Paro_No_Planificado",
            color="Turno",
            markers=True,
            title="Tendencia de Paros No Planificados por Turno",
            color_discrete_sequence=PALETA_TURNOS
        )

        aplicar_layout_linea(fig_paros, "Tendencia de Paros No Planificados por Turno", "Min_Paro_No_Planificado")
        st.plotly_chart(fig_paros, use_container_width=True)

with g4:
    if existe(df, "Fecha") and existe(df, "Costo_Estimado_Perdida") and existe(df, "Turno"):
        serie_costo = serie_por_turno(df, "Costo_Estimado_Perdida", agg="sum")

        fig_costo = px.line(
            serie_costo,
            x="Fecha",
            y="Costo_Estimado_Perdida",
            color="Turno",
            markers=True,
            title="Tendencia de Costo Estimado de Pérdida por Turno",
            color_discrete_sequence=PALETA_TURNOS
        )

        aplicar_layout_linea(fig_costo, "Tendencia de Costo Estimado de Perdida por Turno", "Costo_Estimado_Perdida")
        st.plotly_chart(fig_costo, use_container_width=True)

# =========================================================
# PARETO DE CAUSAS DE PARO
# =========================================================

if existe(df, "Causa_Principal_Paro") and existe(df, "Min_Paro_No_Planificado"):
    pareto_paros = (
        df.groupby("Causa_Principal_Paro", dropna=False)["Min_Paro_No_Planificado"]
        .sum()
        .reset_index()
        .sort_values("Min_Paro_No_Planificado", ascending=False)
        .head(10)
    )

    pareto_paros["Causa_Principal_Paro"] = pareto_paros["Causa_Principal_Paro"].fillna("Sin causa registrada")
    pareto_paros = pareto_paros.sort_values("Min_Paro_No_Planificado", ascending=True)

    fig_pareto = px.bar(
        pareto_paros,
        x="Min_Paro_No_Planificado",
        y="Causa_Principal_Paro",
        orientation="h",
        title="Pareto Top 10 Causas por Minutos de Paro",
        color_discrete_sequence=["#2563EB"],
        text="Min_Paro_No_Planificado"
    )

    fig_pareto.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        cliponaxis=False
    )
    fig_pareto.update_layout(
        height=430,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Arial", size=13, color="#334155"),
        title=dict(font=dict(size=20, color="#0F172A")),
        margin=dict(l=18, r=42, t=58, b=32),
        showlegend=False
    )
    fig_pareto.update_xaxes(gridcolor="#E2E8F0", title="Minutos de paro")
    fig_pareto.update_yaxes(showgrid=False, title=None, automargin=True)
    st.plotly_chart(fig_pareto, use_container_width=True)

# =========================================================
# COMPARATIVOS EJECUTIVOS
# =========================================================

st.markdown('<div class="section-heading">Comparativo Ejecutivo Operativo</div>', unsafe_allow_html=True)

tabla_comparativo = construir_comparativo_ejecutivo(df, meta_oee, meta_scrap)

if len(tabla_comparativo) > 0:
    tabs = st.tabs(["Línea", "Turno", "Máquina"])
    niveles_tabs = [("Linea", tabs[0]), ("Turno", tabs[1]), ("Maquina", tabs[2])]
    columnas_tabla = ["Elemento", "OEE_Promedio", "Scrap_Promedio", "Paros_Total", "Costo_Total", "Tendencia vs Periodo Anterior"]

    for nivel, tab in niveles_tabs:
        with tab:
            tabla_nivel = tabla_comparativo[tabla_comparativo["Nivel"] == nivel].copy()
            if len(tabla_nivel) == 0:
                st.info(f"No hay datos suficientes para comparar por {nivel.lower()}.")
                continue

            tabla_nivel = tabla_nivel[columnas_tabla]
            st.dataframe(
                tabla_nivel,
                use_container_width=True,
                height=min(420, 92 + (len(tabla_nivel) * 35)),
                hide_index=True
            )
else:
    st.info("No hay columnas suficientes para construir el comparativo ejecutivo operativo.")

# =========================================================
# ANÁLISIS IA
# =========================================================

st.markdown('<div class="section-heading">Análisis Inteligente Generado por IA</div>', unsafe_allow_html=True)

if "Brief_Genba" in insights_finales:
    render_list_panel(
        "Brief para Junta Genba",
        insights_finales["Brief_Genba"],
        ordered=True,
        subtitle="Guía breve para enfocar la conversación diaria en piso.",
        extra_class="genba-brief-card"
    )

ia1, ia2 = st.columns(2)

with ia1:
    render_list_panel(
        "Hallazgos Clave",
        insights_finales["Hallazgos_Clave"],
        ordered=False
    )

with ia2:
    render_list_panel(
        "Riesgos Relevantes",
        insights_finales["Riesgos"],
        ordered=False
    )

ia3, ia4 = st.columns(2)

with ia3:
    render_list_panel(
        "Prioridades de Análisis",
        insights_finales["Prioridades"],
        ordered=False
    )

with ia4:
    preguntas_genba = insights_finales.get("Preguntas_GENBA", insights_finales.get("Preguntas_GEMBA", ""))
    render_list_panel(
        "Preguntas sugeridas para Genba",
        preguntas_genba,
        ordered=False
    )

if "Proxima_Accion_Sugerida" in insights_finales:
    render_optional_panel(
        "Próxima Acción Sugerida",
        insights_finales["Proxima_Accion_Sugerida"],
        "Orientación para el siguiente análisis inmediato.",
        "panel-action"
    )

# =========================================================
# DETALLE DEL ÚLTIMO REGISTRO
# =========================================================

st.markdown('<div class="section-heading">Detalle Operativo del Último Registro</div>', unsafe_allow_html=True)

d1, d2, d3 = st.columns(3)

with d1:
    render_panel_lines(
        "Contexto",
        [
            f"Fecha: {format_date(safe_value(ultimo, 'Fecha'))}",
            f"Semana: {safe_value(ultimo, 'Semana')}",
            f"Día: {safe_value(ultimo, 'Dia_Semana')}",
            f"Turno: {safe_value(ultimo, 'Turno')}",
        ]
    )

with d2:
    render_panel_lines(
        "Activo Operativo",
        [
            f"Línea: {safe_value(ultimo, 'Linea')}",
            f"Máquina: {safe_value(ultimo, 'Maquina')}",
            f"Producción meta: {format_number(safe_value(ultimo, 'Produccion_Meta'), 0)}",
            f"Producción real: {format_number(safe_value(ultimo, 'Produccion_Real'), 0)}",
        ]
    )

with d3:
    render_panel_lines(
        "Estado",
        [
            f"Estado general: {safe_value(ultimo, 'Estado_General')}",
            f"OEE: {format_number(safe_value(ultimo, 'OEE_%'), 1)}%",
            f"Scrap: {format_number(safe_value(ultimo, 'Scrap_%'), 2)}%",
            f"Costo: {format_money(safe_value(ultimo, 'Costo_Estimado_Perdida'))}",
        ]
    )

# =========================================================
# HISTÓRICO
# =========================================================

with st.expander("Ver histórico completo del archivo operativo"):
    st.dataframe(df, use_container_width=True, height=420)

with st.expander("Ver histórico de insights generados por IA"):
    st.dataframe(vista_segura_insights(df_insights), use_container_width=True, height=360)

# =========================================================
# PIE
# =========================================================

st.markdown("""
<div style="text-align:center; color:#64748B; font-size:12.5px; margin-top:28px;">
    AI Operational Command Center · Demo ejecutivo de agente operacional con Google Sheets, Relay, GPT y Streamlit
</div>
""", unsafe_allow_html=True)
