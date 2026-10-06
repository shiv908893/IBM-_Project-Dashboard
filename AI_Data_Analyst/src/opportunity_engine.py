from __future__ import annotations

from typing import Any

import pandas as pd


class OpportunityEngine:
    """Detect growth and revenue expansion opportunities from the dataset."""

    @staticmethod
    def detect(df: pd.DataFrame, metrics: dict[str, Any]) -> list[dict[str, str]]:
        opportunities: list[dict[str, str]] = []

        category_growth = (
            df.groupby("category")["sales"].sum().sort_values(ascending=False)
            if "category" in df.columns
            else pd.Series(dtype=float)
        )
        if not category_growth.empty:
            opportunities.append(
                {
                    "title": "High-growth category",
                    "evidence": f"{category_growth.index[0]} contributes the largest sales share.",
                    "potential_impact": "High",
                    "reason": "This category shows the strongest current revenue contribution and could justify additional marketing investment.",
                }
            )

        region_growth = (
            df.groupby("region")["sales"].sum().sort_values(ascending=False)
            if "region" in df.columns
            else pd.Series(dtype=float)
        )
        if not region_growth.empty:
            opportunities.append(
                {
                    "title": "Regional growth opportunity",
                    "evidence": f"{region_growth.index[0]} produces the strongest regional revenue performance.",
                    "potential_impact": "Medium",
                    "reason": "The leading region can absorb targeted marketing and upsell programs to accelerate additional sales.",
                }
            )

        if "profit" in df.columns and "sales" in df.columns:
            high_margin_products = df.assign(margin_ratio=df["profit"] / df["sales"]).groupby("product_name")["margin_ratio"].mean().sort_values(ascending=False)
            if not high_margin_products.empty:
                top_product = high_margin_products.index[0]
                opportunities.append(
                    {
                        "title": "High-margin product",
                        "evidence": f"{top_product} offers the strongest unit margin profile in the portfolio.",
                        "potential_impact": "Medium",
                        "reason": "Promoting the highest-margin products can lift blended profitability without a proportional sales increase.",
                    }
                )

        return opportunities
