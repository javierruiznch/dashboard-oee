import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard OEE",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
}

@media (max-width: 768px) {
    .block-container {
        padding-left: 0.7rem;
        padding-right: 0.7rem;
        padding-top: 0.5rem;
    }

    h1 {
        font-size: 1.5rem !important;
    }

    h2 {
        font-size: 1.2rem !important;
    }

    h3 {
        font-size: 1rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("Dashboard Operativo OEE")
st.caption("Análisis de OEE, scrap, paros no planificados y costos operativos.")

st.info("La app se desplegó correctamente. Esta es una versión inicial de prueba.")

datos_prueba = {
    "Día": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
    "OEE": [0.82, 0.79, 0.85, 0.77, 0.88],
    "Scrap": [0.018, 0.023, 0.016, 0.028, 0.014],
    "Paros no planificados": [45, 62, 30, 80, 25],
    "Costo operativo": [12500, 18000, 9500, 24000, 8700]
}

df = pd.DataFrame(datos_prueba)

st.subheader("Indicadores principales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("OEE promedio", f"{df['OEE'].mean():.1%}")

with col2:
    st.metric("Scrap promedio", f"{df['Scrap'].mean():.1%}")

with col3:
    st.metric("Paros totales", f"{df['Paros no planificados'].sum()} min")

with col4:
    st.metric("Costo total", f"${df['Costo operativo'].sum():,.0f}")

st.subheader("Tendencia de OEE")

fig_oee = px.line(
    df,
    x="Día",
    y="OEE",
    markers=True,
    title="Tendencia de OEE"
)

fig_oee.update_yaxes(tickformat=".0%")

st.plotly_chart(fig_oee, use_container_width=True)

st.subheader("Costo operativo por día")

fig_costo = px.bar(
    df,
    x="Día",
    y="Costo operativo",
    title="Costo operativo diario"
)

st.plotly_chart(fig_costo, use_container_width=True)

st.subheader("Datos base")

st.dataframe(df, use_container_width=True)
