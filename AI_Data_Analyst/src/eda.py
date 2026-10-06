from __future__ import annotations

from typing import Any

import pandas as pd


class EDAReport:
    """Compute a concise EDA summary for executive analysis."""

    @staticmethod
    def summarize(df: pd.DataFrame) -> dict[str, Any]:
        if df is None or df.empty:
            raise ValueError("Cannot summarize an empty dataframe.")

        summary = {
            "shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
            "missing_values": df.isna().sum().to_dict(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "date_range": {
                "start": df["order_date"].min().strftime("%Y-%m-%d") if "order_date" in df.columns else None,
                "end": df["order_date"].max().strftime("%Y-%m-%d") if "order_date" in df.columns else None,
            },
            "duplicate_rows": int(df.duplicated().sum()),
            "top_categories": df["category"].value_counts().head(5).to_dict() if "category" in df.columns else {},
            "top_regions": df["region"].value_counts().head(5).to_dict() if "region" in df.columns else {},
        }
        return summary
