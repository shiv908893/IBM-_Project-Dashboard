from __future__ import annotations

from typing import Any

import pandas as pd


class RiskEngine:
    """Detect business risks and return structured evidence."""

    @staticmethod
    def detect_risks(df: pd.DataFrame, metrics: dict[str, Any], churn_df: pd.DataFrame | None = None) -> list[dict[str, str]]:
        risks: list[dict[str, str]] = []

        if df.empty:
            return risks

        monthly = (
            df.assign(period=df["order_date"].dt.to_period("M").astype(str))
            .groupby("period", as_index=False)
            .agg(revenue=("sales", "sum"), profit=("profit", "sum"))
            .sort_values("period")
            .reset_index(drop=True)
        )

        if len(monthly) > 1:
            current = monthly.iloc[-1]
            previous = monthly.iloc[-2]
            decline_pct = ((previous["revenue"] - current["revenue"]) / previous["revenue"]) * 100 if previous["revenue"] else 0
            if decline_pct > 8:
                risks.append(
                    {
                        "title": "Revenue decline",
                        "severity": "High",
                        "evidence": f"Revenue dropped {decline_pct:.1f}% from the previous month.",
                        "metric": "revenue",
                        "explanation": "Recent sales underperformed versus the immediate prior period, which may reduce cash generation and demand momentum.",
                    }
                )

        category_profit = df.groupby("category")["profit"].sum() / df.groupby("category")["sales"].sum()
        low_margin = category_profit.idxmin() if not category_profit.empty else "Unknown"
        if low_margin != "Unknown":
            risks.append(
                {
                    "title": "Low-margin category",
                    "severity": "Medium",
                    "evidence": f"{low_margin} has the lowest margin in the portfolio.",
                    "metric": "profit_margin",
                    "explanation": "The category is consuming more sales volume than it contributes in profit and may need pricing or mix intervention.",
                }
            )

        if churn_df is not None and not churn_df.empty:
            high_risk = churn_df[churn_df["risk_level"] == "High"]
            if len(high_risk) > 0:
                risks.append(
                    {
                        "title": "High churn risk",
                        "severity": "High",
                        "evidence": f"{len(high_risk)} customers are at high churn risk.",
                        "metric": "churn_probability",
                        "explanation": "Customer retention risk is elevated and may reduce future lifetime value and repeat orders.",
                    }
                )

        return risks
