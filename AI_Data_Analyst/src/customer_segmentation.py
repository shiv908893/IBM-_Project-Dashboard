from __future__ import annotations

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class CustomerSegmentation:
    """Compute RFM-based customer segmentation with K-Means clustering."""

    @staticmethod
    def build_rfm(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            raise ValueError("Customer segmentation requires data.")

        snapshot_date = df["order_date"].max() + pd.Timedelta(days=1)
        rfm = df.groupby("customer_id").agg(
            recency_days=("order_date", lambda x: (snapshot_date - x.max()).days),
            frequency=("order_id", "nunique"),
            monetary=("sales", "sum"),
            avg_order_value=("sales", "mean"),
        ).reset_index()
        rfm["recency_score"] = rfm["recency_days"].rank(ascending=True, method="dense")
        rfm["frequency_score"] = rfm["frequency"].rank(ascending=False, method="dense")
        rfm["monetary_score"] = rfm["monetary"].rank(ascending=False, method="dense")
        return rfm

    @staticmethod
    def segment_customers(df: pd.DataFrame, clusters: int = 4) -> pd.DataFrame:
        rfm = CustomerSegmentation.build_rfm(df)
        features = ["recency_days", "frequency", "monetary"]
        scaler = StandardScaler()
        scaled = scaler.fit_transform(rfm[features])

        model = KMeans(n_clusters=min(clusters, max(2, len(rfm))), random_state=42, n_init=10)
        labels = model.fit_predict(scaled)
        rfm["segment_id"] = labels

        cluster_summary = (
            rfm.groupby("segment_id")
            .agg(
                customers=("customer_id", "count"),
                avg_recency=("recency_days", "mean"),
                avg_frequency=("frequency", "mean"),
                avg_monetary=("monetary", "mean"),
            )
            .reset_index()
            .sort_values("avg_monetary", ascending=False)
        )
        rfm["segment_label"] = rfm["segment_id"].map({
            cluster_summary["segment_id"].iloc[i]: ["VIP", "Loyal", "Growing", "At Risk"][i % 4]
            for i in range(len(cluster_summary))
        })
        return rfm
