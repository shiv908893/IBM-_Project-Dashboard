from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

try:
    from app.components.charts import bar_chart, line_chart, scatter_chart
except ModuleNotFoundError:
    from components.charts import bar_chart, line_chart, scatter_chart

from src.ai_analyst import AIAnalyst
from src.churn_model import ChurnModel
from src.customer_segmentation import CustomerSegmentation
from src.data_cleaning import DataCleaner
from src.data_loader import DataLoader
from src.forecasting import SalesForecaster
from src.kpi_engine import KPIEngine
from src.opportunity_engine import OpportunityEngine
from src.risk_engine import RiskEngine
from src.trend_analysis import TrendAnalyzer


st.set_page_config(page_title="AI Data Analyst Dashboard", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #07111f 0%, #0d1729 45%, #101b2f 100%);
            color: #edf3ff;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1500px;
        }
        h1 {
            font-size: 3.2rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.05em;
            color: #f5f7ff !important;
            margin-bottom: 0.5rem !important;
        }
        h3 {
            font-size: 2rem !important;
            color: #edf3ff !important;
            margin-top: 2rem !important;
            margin-bottom: 1rem !important;
        }
        .stSidebar {
            background: rgba(18, 26, 38, 0.9);
            border-right: 1px solid rgba(140, 160, 200, 0.18);
        }
        .stSidebar .st-bd {
            background: rgba(18, 26, 38, 0.9);
        }
        .stSelectbox > div, .stDateInput > div, .stTextInput > div {
            background: rgba(21, 31, 45, 0.9);
            border: 1px solid rgba(156, 174, 212, 0.28);
            border-radius: 12px;
        }
        .card {
            background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(238,242,255,0.94));
            border: 1px solid rgba(255,255,255,0.16);
            border-radius: 18px;
            padding: 1.2rem 1.1rem;
            min-height: 130px;
            box-shadow: 0 10px 30px rgba(5, 10, 20, 0.22);
            color: #0f172a;
        }
        .card-label {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #475569;
            display: block;
            margin-bottom: 0.7rem;
        }
        .card-value {
            font-size: 1.9rem;
            font-weight: 700;
            color: #0f172a;
        }
        .eco-box {
            background: linear-gradient(135deg, rgba(14, 165, 233, 0.18), rgba(59, 130, 246, 0.12));
            border: 1px solid rgba(96, 165, 250, 0.45);
            border-radius: 16px;
            padding: 1rem 1.2rem;
            margin-top: 0.8rem;
        }
        .caption {
            color: #b6c2db !important;
            font-size: 1.05rem !important;
        }
        .stAlert {
            border-radius: 14px;
            border: 1px solid rgba(148, 163, 184, 0.2);
        }
        .stDataFrame, .stPlotlyChart {
            border-radius: 18px;
            overflow: hidden;
            box-shadow: 0 12px 28px rgba(15, 23, 42, 0.18);
        }
        [data-testid="stMetric"] {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(148,163,184,0.16);
            border-radius: 16px;
            padding: 0.75rem 0.85rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_dataset():
    loader = DataLoader()
    df = loader.load()
    cleaner = DataCleaner()
    cleaned, _ = cleaner.clean(df)
    return cleaned


def apply_filters(df: pd.DataFrame):
    st.sidebar.header("Interactive Filters")
    date_min, date_max = df["order_date"].min(), df["order_date"].max()
    start_date = st.sidebar.date_input("Start date", value=pd.Timestamp(date_min).date())
    end_date = st.sidebar.date_input("End date", value=pd.Timestamp(date_max).date())

    regions = sorted(df["region"].dropna().unique().tolist())
    categories = sorted(df["category"].dropna().unique().tolist())
    sub_categories = sorted(df["sub_category"].dropna().unique().tolist())
    products = sorted(df["product_name"].dropna().unique().tolist())
    segments = sorted(df["customer_segment"].dropna().unique().tolist()) if "customer_segment" in df.columns else []

    region = st.sidebar.selectbox("Region", ["All"] + regions)
    category = st.sidebar.selectbox("Category", ["All"] + categories)
    sub_category = st.sidebar.selectbox("Sub-category", ["All"] + sub_categories)
    product = st.sidebar.selectbox("Product", ["All"] + products)
    customer_segment = st.sidebar.selectbox("Customer segment", ["All"] + segments)

    filtered = df[
        (df["order_date"] >= pd.Timestamp(start_date)) & (df["order_date"] <= pd.Timestamp(end_date))
    ].copy()

    if region != "All":
        filtered = filtered[filtered["region"] == region]
    if category != "All":
        filtered = filtered[filtered["category"] == category]
    if sub_category != "All":
        filtered = filtered[filtered["sub_category"] == sub_category]
    if product != "All":
        filtered = filtered[filtered["product_name"] == product]
    if customer_segment != "All" and "customer_segment" in filtered.columns:
        filtered = filtered[filtered["customer_segment"] == customer_segment]

    return filtered


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
                f"<div class='card'><span class='card-label'>{label}</span><span class='card-value'>{formatted}</span></div>",
                unsafe_allow_html=True,
            )


def render_overview(df: pd.DataFrame):
    st.subheader("Executive Overview")
    st.caption("Verified KPI layer: revenue, profit, growth, orders, customers, and AOV.", unsafe_allow_html=True)
    metrics = KPIEngine(df).compute()
    render_kpi_cards(metrics)


def render_sales_product(df: pd.DataFrame):
    st.subheader("Sales & Product Analysis")
    st.caption("Revenue, margin, category mix, and product profitability insights.")
    category_summary = df.groupby("category")["sales"].sum().sort_values(ascending=False).reset_index()
    product_summary = df.groupby("product_name")["sales"].sum().sort_values(ascending=False).head(10).reset_index()
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.bar(category_summary, x="category", y="sales", title="Revenue by Category"), use_container_width=True)
    with col2:
        st.plotly_chart(px.bar(product_summary, x="product_name", y="sales", title="Top 10 Products by Sales"), use_container_width=True)


def render_customer_risk(df: pd.DataFrame):
    st.subheader("Customer & Risk Analysis")
    st.caption("Customer segmentation, churn risk, and risk detection outputs.")
    metrics = KPIEngine(df).compute()
    segments = CustomerSegmentation.segment_customers(df)
    churn = ChurnModel().fit(df)
    risks = RiskEngine.detect_risks(df, metrics, churn)
    if risks:
        for risk in risks[:5]:
            st.warning(f"{risk['title']} — {risk['evidence']}")
    segment_summary = segments.groupby("segment_label").agg(customers=("customer_id", "count")).reset_index()
    st.plotly_chart(px.bar(segment_summary, x="segment_label", y="customers", title="Customer Segments"), use_container_width=True)


def answer_question(question: str, filtered: pd.DataFrame, metrics: dict, risks: list, opportunities: list, churn_predictions: pd.DataFrame) -> str:
    q = question.lower()

    if "why did revenue decline" in q or "revenue decline" in q:
        if risks:
            first_risk = risks[0]
            return f"Revenue decline is linked to: {first_risk['title']} — {first_risk['evidence']}."
        return f"The current selected window shows revenue of ${metrics['revenue']:,.2f}, so there is no confirmed revenue decline in this view."

    if "region performs best" in q or "best region" in q:
        region_summary = filtered.groupby("region")["sales"].sum().sort_values(ascending=False)
        best = region_summary.index[0]
        value = region_summary.iloc[0]
        return f"The top-performing region is {best} with ${value:,.2f} in revenue."

    if "most profitable" in q or "profitable products" in q:
        product_profit = (filtered.assign(margin_ratio=filtered["profit"] / filtered["sales"]).groupby("product_name")["margin_ratio"].mean().sort_values(ascending=False))
        top = product_profit.index[0]
        return f"The most profitable product in this view is {top}, with the strongest average margin contribution."

    if "customers are at risk" in q or "at risk" in q:
        high_risk = churn_predictions[churn_predictions["risk_level"] == "High"]
        if high_risk.empty:
            return "There are no high-risk customers in the current selection."
        customers = high_risk["customer_id"].head(5).tolist()
        return f"The highest-risk customers are {customers}. Review retention actions for these accounts first."

    if "what is driving revenue" in q or "driving revenue" in q:
        category_summary = filtered.groupby("category")["sales"].sum().sort_values(ascending=False)
        top_category = category_summary.index[0]
        region_summary = filtered.groupby("region")["sales"].sum().sort_values(ascending=False)
        top_region = region_summary.index[0]
        return f"Revenue is mainly driven by {top_category} in {top_region}, which contributes the largest sales share in the current filter set."

    if "marketing investment" in q or "where should marketing" in q:
        region_summary = filtered.groupby("region")["sales"].sum().sort_values(ascending=False)
        best_region = region_summary.index[0]
        return f"Marketing investment should increase in {best_region}, since it delivers the highest revenue contribution in the selected data."

    if "biggest business risks" in q or "business risks" in q:
        if risks:
            risk_titles = "; ".join(r["title"] for r in risks[:3])
            return f"The main business risks are: {risk_titles}."
        return "No major risks are currently detected in the selected data window."

    return (
        f"Verified figures in this view: Revenue ${metrics['revenue']:,.2f}, Profit ${metrics['profit']:,.2f}, "
        f"Growth {metrics['growth_pct']:.2f}%, Orders {metrics['orders']}, Customers {metrics['customers']}."
    )


def main():
    st.title("AI-Powered Data Analyst & Executive Decision Intelligence Dashboard")
    df = load_dataset()
    filtered = apply_filters(df)

    if filtered.empty:
        st.warning("No data matches the selected filters. Please adjust the date or dimension filters.")
        return

    metrics = KPIEngine(filtered).compute()
    render_overview(filtered)
    render_kpi_cards(metrics)

    col1, col2 = st.columns(2)
    with col1:
        monthly = TrendAnalyzer.monthly_trends(filtered)
        st.plotly_chart(line_chart(monthly, "period", "revenue", "Revenue Trend"), use_container_width=True)
    with col2:
        st.plotly_chart(line_chart(monthly, "period", "profit", "Profit Trend"), use_container_width=True)

    region_chart = TrendAnalyzer.region_trends(filtered)
    category_chart = TrendAnalyzer.category_trends(filtered)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(bar_chart(region_chart, "region", "revenue", "Revenue by Region"), use_container_width=True)
    with col4:
        st.plotly_chart(bar_chart(category_chart, "category", "revenue", "Revenue by Category"), use_container_width=True)

    top_products = filtered.groupby("product_name")["sales"].sum().sort_values(ascending=False).head(10).reset_index()
    bottom_products = filtered.groupby("product_name")["sales"].sum().sort_values(ascending=True).head(10).reset_index()

    col5, col6 = st.columns(2)
    with col5:
        st.plotly_chart(bar_chart(top_products, "product_name", "sales", "Top 10 Products"), use_container_width=True)
    with col6:
        st.plotly_chart(bar_chart(bottom_products, "product_name", "sales", "Bottom 10 Products"), use_container_width=True)

    render_sales_product(filtered)
    render_customer_risk(filtered)

    customer_segments = CustomerSegmentation.segment_customers(filtered)
    churn_predictions = ChurnModel().fit(filtered)
    risks = RiskEngine.detect_risks(filtered, metrics, churn_predictions)
    opportunities = OpportunityEngine.detect(filtered, metrics)
    forecast = SalesForecaster.forecast(filtered)
    ai_response = AIAnalyst.generate(metrics, risks, opportunities)

    st.subheader("Risk Indicators")
    if risks:
        for risk in risks[:5]:
            st.warning(f"{risk['title']} — {risk['evidence']}")
    else:
        st.info("No major risk indicators identified within the current dataset window.")

    st.subheader("Opportunities")
    if opportunities:
        for opp in opportunities[:5]:
            st.success(f"{opp['title']} — {opp['evidence']}")
    else:
        st.info("No strong opportunities were detected in the selected dataset slice.")

    st.subheader("AI Executive Summary")
    st.markdown(
        f"<div style='background: #f6f7ff; border-left: 5px solid #4f46e5; padding: 1rem; border-radius: 8px; color: #111827; line-height: 1.6;'>"
        f"{ai_response['executive_summary']}</div>",
        unsafe_allow_html=True,
    )

    st.subheader("AI Findings")
    for item in ai_response["key_findings"]:
        st.write(item)

    st.subheader("Ask Your Data")
    question = st.text_input("Ask a business question", placeholder="Example: Which region performs best?")
    if question:
        answer = answer_question(question, filtered, metrics, risks, opportunities, churn_predictions)
        st.info(answer)

    st.subheader("Forecast")
    forecast_chart = forecast.copy()
    forecast_chart["actual_revenue"] = forecast_chart["actual_revenue"].ffill()
    st.plotly_chart(line_chart(forecast_chart, "period", "actual_revenue", "Historical and Forecasted Revenue"), use_container_width=True)

    st.subheader("Customer Segments")
    segment_summary = customer_segments.groupby("segment_label").agg(customers=("customer_id", "count")).reset_index()
    st.plotly_chart(bar_chart(segment_summary, "segment_label", "customers", "Customer Segments"), use_container_width=True)

    st.subheader("Risk and Opportunity Engine")
    with st.expander("AI Response JSON"):
        st.json(ai_response)

    st.sidebar.caption("This dashboard uses verified Python metrics only. No fabricated business statistics are displayed.")


if __name__ == "__main__":
    main()
