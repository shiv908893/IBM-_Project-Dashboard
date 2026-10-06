from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.churn_model import ChurnModel
from src.customer_segmentation import CustomerSegmentation
from src.data_cleaning import DataCleaner
from src.data_loader import DataLoader
from src.kpi_engine import KPIEngine
from src.risk_engine import RiskEngine


@st.cache_data
def load_dataset():
    df = DataLoader().load()
    cleaned, _ = DataCleaner().clean(df)
    return cleaned


def render_customer_risk_page():
    st.title("Customer & Risk Analysis")
    df = load_dataset()
    metrics = KPIEngine(df).compute()
    segments = CustomerSegmentation.segment_customers(df)
    churn = ChurnModel().fit(df)
    risks = RiskEngine.detect_risks(df, metrics, churn)

    st.caption("Customer segmentation, churn risk, and risk detection outputs.")

    segment_summary = segments.groupby("segment_label").agg(customers=("customer_id", "count")).reset_index()
    st.plotly_chart(px.bar(segment_summary, x="segment_label", y="customers", title="Customer Segments"), use_container_width=True)

    st.subheader("Churn Risk Distribution")
    st.dataframe(churn[["customer_id", "risk_level", "churn_probability"]].head(15))

    if risks:
        st.subheader("Detected Risks")
        for risk in risks:
            st.warning(f"{risk['title']} — {risk['evidence']}")
    else:
        st.info("No major risk indicators identified in the current dataset window.")


render_customer_risk_page()
