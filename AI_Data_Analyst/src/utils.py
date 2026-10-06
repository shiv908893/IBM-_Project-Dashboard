from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


def setup_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_sample_sales_data(n_rows: int = 5000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    regions = ["North", "South", "East", "West", "Central"]
    categories = {
        "Electronics": ["Laptop", "Tablet", "Phone", "Accessories"],
        "Furniture": ["Chair", "Desk", "Storage", "Lighting"],
        "Office Supplies": ["Paper", "Ink", "Binders", "Stationery"],
        "Apparel": ["Shirts", "Jackets", "Accessories", "Footwear"],
    }
    customer_segments = ["New", "Regular", "VIP", "At Risk"]

    rows: list[dict[str, Any]] = []
    for idx in range(n_rows):
        region = rng.choice(regions)
        category = rng.choice(list(categories.keys()))
        product = rng.choice(categories[category])
        segment = rng.choice(customer_segments, p=[0.30, 0.35, 0.20, 0.15])
        order_date = pd.Timestamp("2022-01-01") + pd.Timedelta(days=int(rng.integers(0, 1200)))
        quantity = int(rng.integers(1, 8))
        unit_price = round(float(rng.uniform(20, 220)), 2)
        discount_pct = float(rng.beta(2, 7)) * 0.30
        sales = round(quantity * unit_price * (1 - discount_pct), 2)
        profit = round(sales * float(rng.uniform(0.18, 0.42)), 2)
        customer_id = int(rng.integers(1000, 7000))
        order_id = f"ORD-{100000 + idx}"
        rows.append(
            {
                "order_id": order_id,
                "order_date": order_date,
                "region": region,
                "category": category,
                "sub_category": product,
                "product_name": f"{category} {product}",
                "customer_id": customer_id,
                "customer_segment": segment,
                "quantity": quantity,
                "unit_price": unit_price,
                "discount_pct": round(discount_pct, 4),
                "sales": sales,
                "profit": profit,
                "customer_age": int(rng.integers(21, 72)),
                "channel": rng.choice(["Online", "Retail", "Wholesale"]),
            }
        )

    df = pd.DataFrame(rows)
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
    df["profit"] = pd.to_numeric(df["profit"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    return df


def get_env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    return value
