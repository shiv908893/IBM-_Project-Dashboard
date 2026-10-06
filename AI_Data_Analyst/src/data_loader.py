from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.utils import build_sample_sales_data, ensure_dir, project_root


class DataLoader:
    """Load a sales dataset, creating a sample dataset if missing."""

    def __init__(self, data_path: str | Path | None = None):
        root = project_root()
        self.data_path = Path(data_path) if data_path else root / "data" / "raw" / "sales_data.csv"
        ensure_dir(self.data_path.parent)

    def load(self) -> pd.DataFrame:
        if not self.data_path.exists():
            df = build_sample_sales_data()
            self.data_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(self.data_path, index=False)
        df = pd.read_csv(self.data_path)
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
        return df

    def save_processed(self, df: pd.DataFrame, name: str = "processed_data.csv") -> Path:
        out_dir = project_root() / "data" / "processed"
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / name
        df.to_csv(target, index=False)
        return target
