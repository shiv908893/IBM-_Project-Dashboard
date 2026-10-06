from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.ai_analyst import AIAnalyst
from src.data_cleaning import DataCleaner
from src.data_loader import DataLoader
from src.kpi_engine import KPIEngine
from src.trend_analysis import TrendAnalyzer


@st.cache_data
def load_dataset():
    df = DataLoader().load()
    cleaned, _ = DataCleaner().clean(df)
    return cleaned


def render_kpi_cards(metrics: dict):
    kpis = [
        ("Revenue", metrics["revenue"], "$"),
        ("Profit", metrics["profit"], "$"),
        ("Growth %", metrics["growth_pct"], "%"),
        ("Orders", metrics["orders"], ""),
        ("Customers", metrics["customers"], ""),
        ("AOV", metrics["aov"], "$"),
    ]
    cols = st.columns(6)
    for col, (label, value, suffix) in zip(cols, kpis):
        if suffix == "$":
            formatted = f"${value:,.2f}"
        elif suffix == "%":
            formatted = f"{value:.2f}%"
        else:
            formatted = f"{value:,.0f}"
        with col:
            st.markdown(
                f"<div style='border:1px solid #dfe3e8; border-radius: 10px; padding: 1rem; background: #f8fbff; min-height: 130px; color: #111827;'>"
                f"<small style='color: #374151;'>{label}</small><br><b style='font-size:1.5rem; color: #111827;'>{formatted}</b></div>",
                unsafe_allow_html=True,
            )


def render_overview_page():
    st.title("Executive Overview")
    df = load_dataset()
    metrics = KPIEngine(df).compute()
    render_kpi_cards(metrics)
    st.caption("Verified KPI layer: revenue, profit, growth, orders, customers, and AOV.")

    monthly = TrendAnalyzer.monthly_trends(df)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.line(monthly, x="period", y="revenue", title="Revenue Trend", markers=True), use_container_width=True)
    with col2:
        st.plotly_chart(px.line(monthly, x="period", y="profit", title="Profit Trend", markers=True), use_container_width=True)

    st.subheader("AI Executive Summary")
    ai_response = AIAnalyst.generate(metrics, [], [])
    st.markdown(
        f"<div style='background: #f6f7ff; border-left: 5px solid #4f46e5; padding: 1rem; border-radius: 8px; color: #111827; line-height: 1.6;'>"
        f"{ai_response['executive_summary']}</div>",
        unsafe_allow_html=True,
    )


render_overview_page()
