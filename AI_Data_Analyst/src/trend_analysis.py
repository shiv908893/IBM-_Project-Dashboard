from __future__ import annotations

import pandas as pd


class TrendAnalyzer:
    """Compute trend insights across time, region, and category."""

    @staticmethod
    def monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            raise ValueError("Trend analysis requires data.")
        monthly = (
            df.assign(period=df["order_date"].dt.to_period("M").astype(str))
            .groupby("period", as_index=False)
            .agg(
                revenue=("sales", "sum"),
                profit=("profit", "sum"),
                orders=("order_id", "nunique"),
                customers=("customer_id", "nunique"),
            )
            .sort_values("period")
            .reset_index(drop=True)
        )
        monthly["period"] = pd.PeriodIndex(monthly["period"], freq="M").to_timestamp()
        return monthly

    @staticmethod
    def category_trends(df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.groupby("category")
            .agg(revenue=("sales", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique"))
            .reset_index()
            .sort_values("revenue", ascending=False)
        )

    @staticmethod
    def region_trends(df: pd.DataFrame) -> pd.DataFrame:
        return (
            df.groupby("region")
            .agg(revenue=("sales", "sum"), profit=("profit", "sum"), customers=("customer_id", "nunique"))
            .reset_index()
            .sort_values("revenue", ascending=False)
        )
