from __future__ import annotations

from typing import Any

import pandas as pd


class KPIEngine:
    """Compute executive KPIs and verified metrics."""

    def __init__(self, df: pd.DataFrame | None = None):
        self.df = df.copy() if df is not None else pd.DataFrame()

    def compute(self_or_df, df: pd.DataFrame | None = None) -> dict[str, Any]:
        frame = self_or_df.df if isinstance(self_or_df, KPIEngine) else self_or_df
        if df is not None:
            frame = df

        if frame.empty:
            raise ValueError("No data to compute KPIs.")

        revenue = float(frame["sales"].sum())
        profit = float(frame["profit"].sum())
        orders = int(frame["order_id"].nunique()) if "order_id" in frame.columns else int(len(frame))
        customers = int(frame["customer_id"].nunique()) if "customer_id" in frame.columns else 0
        aov = float(revenue / orders) if orders else 0.0
        margin = float((profit / revenue) * 100) if revenue else 0.0

        monthly = (
            frame.assign(order_month=frame["order_date"].dt.to_period("M").astype(str))
            .groupby("order_month", as_index=False)
            .agg(revenue=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique"))
            .sort_values("order_month")
            .reset_index(drop=True)
        )

        current_month = monthly.iloc[-1] if not monthly.empty else pd.Series({"revenue": 0.0, "profit": 0.0})
        previous_month = monthly.iloc[-2] if len(monthly) > 1 else pd.Series({"revenue": 0.0, "profit": 0.0})
        growth = float(((current_month["revenue"] - previous_month["revenue"]) / previous_month["revenue"]) * 100) if previous_month["revenue"] else 0.0

        top_category = frame.groupby("category")["sales"].sum().idxmax() if "category" in frame.columns else "Unknown"
        top_region = frame.groupby("region")["sales"].sum().idxmax() if "region" in frame.columns else "Unknown"

        returning = 0
        if "customer_id" in frame.columns and "order_date" in frame.columns:
            cust = frame.groupby("customer_id")["order_date"].nunique()
            returning = int((cust > 1).sum())
        retention = float((returning / customers) * 100) if customers else 0.0

        return {
            "revenue": round(revenue, 2),
            "profit": round(profit, 2),
            "growth_pct": round(growth, 2),
            "orders": orders,
            "customers": customers,
            "aov": round(aov, 2),
            "profit_margin": round(margin, 2),
            "retention_rate": round(retention, 2),
            "top_category": top_category,
            "top_region": top_region,
            "monthly_table": monthly.rename(columns={"order_month": "period"}),
        }
