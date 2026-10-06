from __future__ import annotations

import pandas as pd
from sklearn.linear_model import LogisticRegression


class ChurnModel:
    """Predict customer churn using interpretable RFM features."""

    def __init__(self):
        self.model = LogisticRegression(max_iter=2000, random_state=42)
        self.features = ["recency_days", "frequency", "monetary", "avg_order_value"]
        self.df = pd.DataFrame()

    def fit(self_or_df, df: pd.DataFrame | None = None) -> pd.DataFrame:
        frame = self_or_df.df if isinstance(self_or_df, ChurnModel) else self_or_df
        if df is not None:
            frame = df

        if frame.empty:
            raise ValueError("Churn modeling requires customer data.")

        features = ["recency_days", "frequency", "monetary", "avg_order_value"]
        if isinstance(self_or_df, ChurnModel):
            features = self_or_df.features

        snapshot = frame.groupby("customer_id").agg(
            recency_days=("order_date", lambda x: (frame["order_date"].max() - x.max()).days),
            frequency=("order_id", "nunique"),
            monetary=("sales", "sum"),
            avg_order_value=("sales", "mean"),
        ).reset_index()

        snapshot["churn_label"] = (snapshot["recency_days"] > snapshot["recency_days"].quantile(0.75)).astype(int)
        X = snapshot[features]
        y = snapshot["churn_label"]

        model = LogisticRegression(max_iter=2000, random_state=42)
        model.fit(X, y)
        if isinstance(self_or_df, ChurnModel):
            self_or_df.model = model
            self_or_df.df = frame.copy()

        snapshot["churn_probability"] = model.predict_proba(X)[:, 1]
        snapshot["risk_level"] = snapshot["churn_probability"].apply(
            lambda p: "High" if p > 0.7 else "Medium" if p > 0.4 else "Low"
        )
        snapshot["important_features"] = snapshot[features].apply(
            lambda row: {k: round(float(v), 3) for k, v in row.items()}, axis=1
        )
        return snapshot
