from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


class SalesForecaster:
    """Generate a practical monthly sales forecast using a linear trend model."""

    @staticmethod
    def forecast(df: pd.DataFrame, periods: int = 6) -> pd.DataFrame:
        if df.empty:
            raise ValueError("Forecasting requires data.")

        monthly = (
            df.assign(period=df["order_date"].dt.to_period("M").astype(str))
            .groupby("period", as_index=False)
            .agg(revenue=("sales", "sum"))
            .sort_values("period")
            .reset_index(drop=True)
        )
        monthly["period"] = pd.PeriodIndex(monthly["period"], freq="M").to_timestamp()

        if len(monthly) < 2:
            raise ValueError("Insufficient monthly history for forecasting.")

        X = np.arange(len(monthly)).reshape(-1, 1)
        y = monthly["revenue"].values
        model = LinearRegression()
        model.fit(X, y)

        future_x = np.arange(len(monthly), len(monthly) + periods).reshape(-1, 1)
        future_pred = model.predict(future_x)
        future_dates = pd.date_range(start=monthly["period"].max() + pd.offsets.MonthBegin(1), periods=periods, freq="MS")

        forecast = pd.DataFrame({"period": future_dates, "forecast_revenue": future_pred})
        historical = monthly[["period", "revenue"]].rename(columns={"revenue": "actual_revenue"})
        return pd.concat([historical, forecast], ignore_index=True)
