from __future__ import annotations

from typing import Any

import pandas as pd


class DataCleaner:
    """Clean and validate a raw sales dataset."""

    def clean(self, df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
        if df is None or df.empty:
            raise ValueError("Dataset is empty or missing.")

        cleaned = df.copy()
        initial_shape = cleaned.shape

        for col in ["order_date", "region", "category", "sub_category", "product_name", "customer_id"]:
            if col not in cleaned.columns:
                cleaned[col] = "Unknown"

        for col in ["sales", "profit", "quantity", "unit_price", "discount_pct"]:
            if col not in cleaned.columns:
                cleaned[col] = pd.NA

        cleaned["order_date"] = pd.to_datetime(cleaned["order_date"], errors="coerce")
        cleaned = cleaned.dropna(subset=["order_date"]).copy()

        if "sales" in cleaned.columns:
            cleaned["sales"] = pd.to_numeric(cleaned["sales"], errors="coerce")
        if "profit" in cleaned.columns:
            cleaned["profit"] = pd.to_numeric(cleaned["profit"], errors="coerce")
        if "quantity" in cleaned.columns:
            cleaned["quantity"] = pd.to_numeric(cleaned["quantity"], errors="coerce")
        if "unit_price" in cleaned.columns:
            cleaned["unit_price"] = pd.to_numeric(cleaned["unit_price"], errors="coerce")
        if "discount_pct" in cleaned.columns:
            cleaned["discount_pct"] = pd.to_numeric(cleaned["discount_pct"], errors="coerce")

        numeric_cols = ["sales", "profit", "quantity", "unit_price", "discount_pct"]
        for col in numeric_cols:
            median_value = cleaned[col].median()
            cleaned[col] = cleaned[col].fillna(median_value)

        cleaned["region"] = cleaned["region"].fillna("Unknown").astype(str).str.strip().str.title()
        cleaned["category"] = cleaned["category"].fillna("Unknown").astype(str).str.strip().str.title()
        cleaned["sub_category"] = cleaned["sub_category"].fillna("Unknown").astype(str).str.strip().str.title()
        cleaned["product_name"] = cleaned["product_name"].fillna("Unknown").astype(str).str.strip()

        if "sales" in cleaned.columns and "quantity" in cleaned.columns and "unit_price" in cleaned.columns:
            cleaned["sales"] = cleaned["sales"].where(cleaned["sales"].notna(), cleaned["quantity"] * cleaned["unit_price"])
        if "profit" in cleaned.columns and "sales" in cleaned.columns:
            cleaned["profit"] = cleaned["profit"].where(cleaned["profit"].notna(), cleaned["sales"] * 0.25)

        cleaned = cleaned.drop_duplicates().reset_index(drop=True)

        summary = {
            "initial_rows": int(initial_shape[0]),
            "final_rows": int(cleaned.shape[0]),
            "rows_removed": int(max(initial_shape[0] - cleaned.shape[0], 0)),
            "missing_values": int(cleaned.isna().sum().sum()),
            "duplicate_rows": int(initial_shape[0] - cleaned.drop_duplicates().shape[0]),
            "date_range": {
                "start": cleaned["order_date"].min().strftime("%Y-%m-%d") if not cleaned.empty else None,
                "end": cleaned["order_date"].max().strftime("%Y-%m-%d") if not cleaned.empty else None,
            },
        }
        return cleaned, summary
