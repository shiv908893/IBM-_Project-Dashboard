from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_cleaning import DataCleaner
from src.data_loader import DataLoader


@st.cache_data
def load_dataset():
    df = DataLoader().load()
    cleaned, _ = DataCleaner().clean(df)
    return cleaned


def render_sales_product_page():
    st.title("Sales & Product Analysis")
    df = load_dataset()

    category_summary = df.groupby("category")["sales"].sum().sort_values(ascending=False).reset_index()
    product_summary = df.groupby("product_name")["sales"].sum().sort_values(ascending=False).head(10).reset_index()

    st.caption("Revenue, margin, category mix, and product profitability insights.")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.bar(category_summary, x="category", y="sales", title="Revenue by Category"), use_container_width=True)
    with col2:
        st.plotly_chart(px.bar(product_summary, x="product_name", y="sales", title="Top 10 Products by Sales"), use_container_width=True)

    st.subheader("Product Sales Table")
    st.dataframe(product_summary.rename(columns={"sales": "total_sales"}), use_container_width=True)


render_sales_product_page()
